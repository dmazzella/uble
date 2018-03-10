# -*- coding: utf-8 -*-
import gc
gc.threshold(4096)
import os
import ustruct
import urandom
import utime
import binascii
import _thread

from bluetooth_low_energy.api.characteristic import Characteristic
from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.descriptor import Descriptor
from bluetooth_low_energy.api.peripheral import Peripheral
from bluetooth_low_energy.api.service import Service
from bluetooth_low_energy.api.uuid import UUID
from bluetooth_low_energy.api.util import format_advertisement

import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("hid_over_gatt")

CONNECTED = False

BATTERY_LEVEL = b'\x64'

SYSTEM_ID = b"0000000000"
MODEL_NUMBER = b"HID over GATT"
SERIAL_NUMBER = b"1234567890"
FIRMWARE_REVISION = b"v0.1b"
HARDWARE_REVISION = b"v0.1b"
SOFTWARE_REVISION = b"v0.1b"
MANUFACTURER_NAME = b"dmazzella"
PNP_ID = b"\x01\x20\x00\x01\x22\x00\x00"

RESPONSE_HID_INFORMATION = b"\x11\x01\x00\x03"
RESPONSE_HID_CONTROL_POINT = b"\x00"
RESPONSE_HID_PROTOCOL_MODE = b"\x01"
RESPONSE_HID_EMPTY_BYTES = b"\x00\x00\x00\x00\x00\x00\x00\x00"

REPORT_ID = 0x00

REPORT_MAP = bytes([
    0x05, 0x01,    # Usage Page (Generic Desktop)
    0x09, 0x06,    # Usage (Keyboard)
    0xA1, 0x01,    # Collection (Application)
    # 0x85, REPORT_ID,  # Report Id (1) ???
    0x05, 0x07,  # Usage Page (Key Codes)
    0x19, 0xe0,  # Usage Minimum (224)
    0x29, 0xe7,  # Usage Maximum (231)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x01,  # Logical Maximum (1)
    0x75, 0x01,  # Report Size (1)
    0x95, 0x08,  # Report Count (8)
    0x81, 0x02,  # Input (Data, Variable, Absolute)
    0x95, 0x01,  # Report Count (1)
    0x75, 0x08,  # Report Size (8)
    0x81, 0x01,  # Input (Constant) reserved byte(1)
    0x95, 0x05,  # Report Count (5)
    0x75, 0x01,  # Report Size (1)
    0x05, 0x08,  # Usage Page (Page# for LEDs)
    0x19, 0x01,  # Usage Minimum (1)
    0x29, 0x05,  # Usage Maximum (5)
    0x91, 0x02,  # Output (Data, Variable, Absolute), Led report
    0x95, 0x01,  # Report Count (1)
    0x75, 0x03,  # Report Size (3)
    0x91, 0x01,  # Output (Data, Variable, Absolute), Led report padding
    0x95, 0x06,  # Report Count (6)
    0x75, 0x08,  # Report Size (8)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x65,  # Logical Maximum (101)
    0x05, 0x07,  # Usage Page (Key codes)
    0x19, 0x00,  # Usage Minimum (0)
    0x29, 0x65,  # Usage Maximum (101)
    0x81, 0x00,  # Input (Data, Array) Key array(6 bytes)
    0x09, 0x05,  # Usage (Vendor Defined)
    0x15, 0x00,  # Logical Minimum (0)
    0x26, 0xFF, 0x00,  # Logical Maximum (255)
    0x75, 0x08,  # Report Count (2)
    0x95, 0x02,  # Report Size (8 bit)
    0xB1, 0x02,  # Feature (Data, Variable, Absolute)
    0xC0           # End Collection (Application)
])

MODIFIER_KEY = {
    0b00000001: "left control",
    0b00000010: "left shift",
    0b00000100: "left alt",
    0b00001000: "left GUI (Win/Apple/Meta key)",
    0b00010000: "right control",
    0b00100000: "right shift",
    0b01000000: "right alt",
    0b10000000: "right GUI (Win/Apple/Meta key)"
}

LOOKUP_TABLE = {
    0x21: [True,  0x1E],
    0x22: [True,  0x34],
    0x23: [True,  0x20],
    0x24: [True,  0x21],
    0x25: [True,  0x22],
    0x26: [True,  0x24],
    0x27: [False, 0x34],
    0x28: [True,  0x26],
    0x29: [True,  0x27],
    0x2A: [True,  0x25],
    0x2B: [True,  0x2E],
    0x2C: [False, 0x36],
    0x2D: [False, 0x2D],
    0x2E: [False, 0x37],
    0x2F: [False, 0x38],
    0x3A: [True,  0x33],
    0x3B: [False, 0x33],
    0x3C: [True,  0x36],
    0x3D: [False, 0x2E],
    0x3E: [True,  0x37],
    0x3F: [True,  0x38],
    0x40: [True,  0x1F],
    0x5B: [False, 0x2F],
    0x5C: [False, 0x31],
    0x5D: [False, 0x30],
    0x5E: [True,  0x23],
    0x5F: [True,  0x2D],
    0x60: [False, 0x35],
    0x7B: [True,  0x2F],
    0x7C: [True,  0x31],
    0x7D: [True,  0x30],
    0x7E: [True,  0x35],
    0x7F: [False, 0x4C],
}

NUM_0 = 0x30
NUM_9 = 0x39
CHAR_A = 0x41
CHAR_Z = 0x5A
CHAR_a = 0x61
CHAR_z = 0x7A
RETURN = 0x0D
BACKSPACE = 0x08
TAB = 0x09
SPACE = 0x20


######################## Device Information Service #######################
SERVICE_DEVICE_INFORMATION_UUID = UUID('180A')
CHARACTERISTIC_SYSTEM_ID_UUID = UUID('2A23')
CHARACTERISTIC_MODEL_NUMBER_UUID = UUID('2A24')
CHARACTERISTIC_SERIAL_NUMBER_UUID = UUID('2A25')
CHARACTERISTIC_FIRMWARE_REVISION_STRING_UUID = UUID('2A26')
CHARACTERISTIC_HARDWARE_REVISION_STRING_UUID = UUID('2A27')
CHARACTERISTIC_SOFTWARE_REVISION_STRING_UUID = UUID('2A28')
CHARACTERISTIC_MANUFACTURER_NAME_UUID = UUID('2A29')
CHARACTERISTIC_REGULATORY_CERTIFICATION_DATA_LIST_UUID = UUID('2A2A')
CHARACTERISTIC_PNP_ID_UUID = UUID('2A50')
############################# Battery Service #############################
SERVICE_BATTERY_UUID = UUID('180F')
CHARACTERISTIC_BATTERY_LEVEL_UUID = UUID('2A19')
DESCRIPTOR_CHARACTERISTIC_PRESENTATION_FORMAT_UUID = UUID('2904')
############################### HID Service ###############################
SERVICE_BLE_HID_UUID = UUID('1812')
CHARACTERISTIC_HID_INFORMATION_UUID = UUID('2A4A')
CHARACTERISTIC_REPORT_MAP_UUID = UUID('2A4B')
CHARACTERISTIC_HID_CONTROL_POINT_UUID = UUID('2A4C')
CHARACTERISTIC_REPORT_UUID = UUID('2A4D')
CHARACTERISTIC_PROTOCOL_MODE_UUID = UUID('2A4E')
DESCRIPTOR_REPORT_REFERENCE_UUID = UUID('2908')
############################# Scan Parameters #############################
SERVICE_SCAN_PARAMETERS_UUID = UUID('1813')
CHARACTERISTIC_SCAN_INTERVAL_WINDOW_UUID = UUID('2A4F')
CHARACTERISTIC_SCAN_REFRESH_UUID = UUID('2A31')
############################# Common Elements #############################
DESCRIPTOR_CLIENT_CHARACTERISTIC_CONFIGURATION_UUID = UUID('2902')


def hid_keyboard_map(charac):
    hid_value = 0
    is_upper_case = False

    if charac >= NUM_0 and charac <= NUM_9:
        hid_value = charac - 0x30
        if hid_value == 0:
            hid_value = 0x27
        else:
            hid_value += 0x1D
    elif charac >= CHAR_A and charac <= CHAR_Z:
        hid_value = charac - 0x41 + 0x04
        is_upper_case = True
    elif charac >= CHAR_a and charac <= CHAR_z:
        hid_value = charac - 0x61 + 0x04
        is_upper_case = False
    elif charac == RETURN:
        hid_value = 0x28
    elif charac == BACKSPACE:
        hid_value = 0x02A
    elif charac == SPACE:
        hid_value = 0x2C
    elif charac == TAB:
        hid_value = 0x2B
    elif charac in LOOKUP_TABLE:
        is_upper_case, hid_value = LOOKUP_TABLE[charac]

    return hid_value, is_upper_case


def main():
    """ HID over GATT """

    ######################## Device Information Service #######################

    characteristic_model = Characteristic(
        CHARACTERISTIC_SYSTEM_ID_UUID,
        char_value_len=20,
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_model_number = Characteristic(
        CHARACTERISTIC_MODEL_NUMBER_UUID,
        char_value_len=20,
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_serial_number = Characteristic(
        CHARACTERISTIC_SERIAL_NUMBER_UUID,
        char_value_len=20,
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_firmware_revision_string = Characteristic(
        CHARACTERISTIC_FIRMWARE_REVISION_STRING_UUID,
        char_value_len=20,
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_hardware_revision_string = Characteristic(
        CHARACTERISTIC_HARDWARE_REVISION_STRING_UUID,
        char_value_len=20,
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_software_revision_string = Characteristic(
        CHARACTERISTIC_SOFTWARE_REVISION_STRING_UUID,
        char_value_len=20,
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_manufacturer_name = Characteristic(
        CHARACTERISTIC_MANUFACTURER_NAME_UUID,
        char_value_len=20,
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_regulatory_certification_data_list = Characteristic(
        CHARACTERISTIC_REGULATORY_CERTIFICATION_DATA_LIST_UUID,
        char_value_len=20,
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_pnp_id = Characteristic(
        CHARACTERISTIC_PNP_ID_UUID,
        char_value_len=len(PNP_ID),
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    service_device_information = Service(
        SERVICE_DEVICE_INFORMATION_UUID,
        service_type=SERVICE_PRIMARY,
        characteristics=[
            characteristic_model,
            characteristic_model_number,
            characteristic_serial_number,
            characteristic_firmware_revision_string,
            characteristic_hardware_revision_string,
            characteristic_software_revision_string,
            characteristic_manufacturer_name,
            characteristic_regulatory_certification_data_list,
            characteristic_pnp_id
        ]
    )

    ############################# Battery Service #############################

    # Client Characteristic Configuration:
    # Bit # (MSB)
    # 0:
    #     0: Notifications disabled
    #     1 :Notifications enabled
    # 1:
    #     0: Indications disabled
    #     1: Indications enabled

    descriptor_client_characteristic_configuration_battery_level = Descriptor(
        DESCRIPTOR_CLIENT_CHARACTERISTIC_CONFIGURATION_UUID,
        ustruct.pack("<H", 0b0000000000000001),
        perms=0x04,
        acc=0x03,
        mask=0x01,
        is_variable=False
    )

    # Characteristic Presentation Format:
    # 0x04: unsigned 8 bit integer
    # 0x00: no exponent
    # 0x27AD: unit = percentage
    # 0x01: Bluetooth SIG namespace
    # 0x0000: No description

    descriptor_characteristic_presentation_format = Descriptor(
        DESCRIPTOR_CHARACTERISTIC_PRESENTATION_FORMAT_UUID,
        ustruct.pack("<BBHBH", 0x04, 0x00, 0x27AD, 0x01, 0x0000),
        perms=0x04,
        acc=0x01,
        mask=0x01
    )

    characteristic_battery_level = Characteristic(
        CHARACTERISTIC_BATTERY_LEVEL_UUID,
        char_value_len=len(BATTERY_LEVEL),
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
        descriptors=[
            descriptor_characteristic_presentation_format,
            descriptor_client_characteristic_configuration_battery_level
        ]
    )

    service_battery = Service(
        SERVICE_BATTERY_UUID,
        service_type=SERVICE_PRIMARY,
        characteristics=[characteristic_battery_level]
    )

    ############################### HID Service ###############################

    characteristic_hid_information = Characteristic(
        CHARACTERISTIC_HID_INFORMATION_UUID,
        char_value_len=len(RESPONSE_HID_INFORMATION),
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_report_map = Characteristic(
        CHARACTERISTIC_REPORT_MAP_UUID,
        char_value_len=len(REPORT_MAP),
        props=PROP_READ,
        perms=PERM_ENCRY_READ,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_protocol_mode = Characteristic(
        CHARACTERISTIC_PROTOCOL_MODE_UUID,
        char_value_len=len(RESPONSE_HID_PROTOCOL_MODE),
        props=PROP_READ | PROP_WRITE_WO_RESP,
        perms=PERM_ENCRY_READ | PERM_ENCRY_WRITE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_hid_control_point = Characteristic(
        CHARACTERISTIC_HID_CONTROL_POINT_UUID,
        char_value_len=len(RESPONSE_HID_CONTROL_POINT),
        props=PROP_WRITE_WO_RESP,
        perms=PERM_ENCRY_WRITE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    # Client Characteristic Configuration:
    # Bit # (MSB)
    # 0:
    #     0: Notifications disabled
    #     1 :Notifications enabled
    # 1:
    #     0: Indications disabled
    #     1: Indications enabled

    # descriptor_client_characteristic_configuration_hid = Descriptor(
    #     DESCRIPTOR_CLIENT_CHARACTERISTIC_CONFIGURATION_UUID,
    #     ustruct.pack("<H", 0b0000000000000001),
    #     perms=0x04,
    #     acc=0x03,
    #     mask=0x01,
    #     is_variable=False
    # )

    # Report Reference:
    # Report ID: unsigned 8 bit integer, any value
    # Report Type: unsigned 8 bit integer
    #     1: Input Report
    #     2: Output report
    #     3: Feature Report
    #     4 - 255: Reserved for future use
    #     0: Reserved for future use

    descriptor_input_report_reference = Descriptor(
        DESCRIPTOR_REPORT_REFERENCE_UUID,
        ustruct.pack("<BB", REPORT_ID, 0x01),
        perms=0x04,
        acc=0x03,
        mask=0x01
    )

    # Input Report
    characteristic_input_report = Characteristic(
        CHARACTERISTIC_REPORT_UUID,
        char_value_len=len(RESPONSE_HID_EMPTY_BYTES),
        props=PROP_NOTIFY | PROP_READ | PROP_WRITE,
        perms=PERM_ENCRY_READ | PERM_ENCRY_WRITE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
        descriptors=[
            descriptor_input_report_reference,
            # descriptor_client_characteristic_configuration_hid
        ]
    )

    # Report Reference:
    # Report ID: unsigned 8 bit integer, any value
    # Report Type: unsigned 8 bit integer
    #     1: Input Report
    #     2: Output report
    #     3: Feature Report
    #     4 - 255: Reserved for future use
    #     0: Reserved for future use

    descriptor_output_report_reference = Descriptor(
        DESCRIPTOR_REPORT_REFERENCE_UUID,
        ustruct.pack("<BB", REPORT_ID, 0x02),
        perms=0x04,
        acc=0x03,
        mask=0x01
    )

    # Output Report
    characteristic_output_report = Characteristic(
        CHARACTERISTIC_REPORT_UUID,
        char_value_len=1,
        props=PROP_READ | PROP_WRITE | PROP_WRITE_WO_RESP,
        perms=PERM_ENCRY_READ | PERM_ENCRY_WRITE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
        descriptors=[descriptor_output_report_reference]
    )

    service_ble_hid = Service(
        SERVICE_BLE_HID_UUID,
        service_type=SERVICE_PRIMARY,
        characteristics=[
            characteristic_hid_information,
            characteristic_report_map,
            characteristic_protocol_mode,
            characteristic_hid_control_point,
            characteristic_input_report,
            characteristic_output_report
        ]
    )

    ############################# Scan Parameters #############################

    characteristic_scan_interval_window = Characteristic(
        CHARACTERISTIC_SCAN_INTERVAL_WINDOW_UUID,
        char_value_len=4,
        props=PROP_WRITE_WO_RESP,
        perms=PERM_ENCRY_READ | PERM_ENCRY_WRITE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP |
        MASK_NOTIFY_WRITE_REQ_AND_WAIT_FOR_APPL_RESP
    )

    characteristic_scan_refresh = Characteristic(
        CHARACTERISTIC_SCAN_REFRESH_UUID,
        char_value_len=1,
        props=PROP_NOTIFY,
        perms=PERM_ENCRY_READ | PERM_ENCRY_WRITE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP |
        MASK_NOTIFY_WRITE_REQ_AND_WAIT_FOR_APPL_RESP
    )

    service_scan_parameters = Service(
        SERVICE_SCAN_PARAMETERS_UUID,
        service_type=SERVICE_PRIMARY,
        characteristics=[
            characteristic_scan_interval_window,
            characteristic_scan_refresh
        ]
    )

    ########################### Advertisement Data ############################

    advertisement_services = [
        # 16-bit SERVICE BATTERY UUID.
        a for a in SERVICE_BATTERY_UUID.value
    ] + [
        # 16-bit SERVICE DEVICE INFORMATION UUID.
        a for a in SERVICE_DEVICE_INFORMATION_UUID.value
    ] + [
        # 16-bit SERVICE HID UUID.
        a for a in SERVICE_BLE_HID_UUID.value
    ] + [
        # 16-bit SERVICE SCAN PARAMETERS UUID.
        a for a in SERVICE_SCAN_PARAMETERS_UUID.value
    ]

    len_advertisement_services = len(advertisement_services)

    advertisement_data = bytes([
        # Length
        2,
        # Flags data type value.
        st_constant.AD_TYPE_FLAGS,
        # BLE general discoverable, without BR/EDR support.
        st_constant.FLAG_BIT_LE_GENERAL_DISCOVERABLE_MODE |\
        st_constant.FLAG_BIT_BR_EDR_NOT_SUPPORTED,
        # Length.
        1 + len_advertisement_services,
        # Complete list of 16-bit Service UUIDs data type value.
        st_constant.AD_TYPE_16_BIT_SERV_UUID_CMPLT_LIST,
    ] + advertisement_services
    )

    log.info("Advertising data: %s", format_advertisement(advertisement_data))

    def on_characteristic_read_request(uuid):
        nonlocal peripheral
        ########################### Battery Service ###########################
        if uuid == CHARACTERISTIC_BATTERY_LEVEL_UUID:
            peripheral.write_uuid(uuid, BATTERY_LEVEL)
            return True
        ###################### Device Information Service #####################
        elif uuid == CHARACTERISTIC_SYSTEM_ID_UUID:
            return True
        elif uuid == CHARACTERISTIC_MODEL_NUMBER_UUID:
            peripheral.write_uuid(uuid, MODEL_NUMBER)
            return True
        elif uuid == CHARACTERISTIC_SERIAL_NUMBER_UUID:
            peripheral.write_uuid(uuid, SERIAL_NUMBER)
            return True
        elif uuid == CHARACTERISTIC_FIRMWARE_REVISION_STRING_UUID:
            peripheral.write_uuid(uuid, FIRMWARE_REVISION)
            return True
        elif uuid == CHARACTERISTIC_HARDWARE_REVISION_STRING_UUID:
            peripheral.write_uuid(uuid, HARDWARE_REVISION)
            return True
        elif uuid == CHARACTERISTIC_SOFTWARE_REVISION_STRING_UUID:
            peripheral.write_uuid(uuid, SOFTWARE_REVISION)
            return True
        elif uuid == CHARACTERISTIC_MANUFACTURER_NAME_UUID:
            peripheral.write_uuid(uuid, MANUFACTURER_NAME)
            return True
        elif uuid == CHARACTERISTIC_PNP_ID_UUID:
            peripheral.write_uuid(uuid, PNP_ID)
            return True
        elif uuid == CHARACTERISTIC_REGULATORY_CERTIFICATION_DATA_LIST_UUID:
            # ???
            return True
        ############################# HID Service #############################
        elif uuid == CHARACTERISTIC_HID_INFORMATION_UUID:
            peripheral.write_uuid(uuid, RESPONSE_HID_INFORMATION)
            return True
        elif uuid == CHARACTERISTIC_REPORT_MAP_UUID:
            peripheral.write_uuid(uuid, REPORT_MAP)
            return True
        elif uuid == CHARACTERISTIC_HID_CONTROL_POINT_UUID:
            peripheral.write_uuid(uuid, RESPONSE_HID_CONTROL_POINT)
            return True
        elif uuid == CHARACTERISTIC_REPORT_UUID:
            peripheral.write_uuid(uuid, RESPONSE_HID_EMPTY_BYTES)
            return True
        elif uuid == CHARACTERISTIC_PROTOCOL_MODE_UUID:
            peripheral.write_uuid(uuid, RESPONSE_HID_PROTOCOL_MODE)
            return True
        ########################### Scan Parameters ###########################
        elif uuid == CHARACTERISTIC_SCAN_INTERVAL_WINDOW_UUID:
            # ???
            return True
        elif uuid == CHARACTERISTIC_SCAN_REFRESH_UUID:
            # ???
            return True
        else:
            return False

    def hid_over_gatt_event_handler(evt, handler=None, data=None):
        """ event callback """
        global CONNECTED
        nonlocal peripheral
        uuid = peripheral.uuid_from_handle((handler or 0) - 1)
        if evt == EVT_GAP_CONNECTED:
            log.info("EVT_GAP_CONNECTED %s", binascii.hexlify(data, ':'))
            CONNECTED = True
        elif evt == EVT_GAP_DISCONNECTED:
            log.info("EVT_GAP_DISCONNECTED")
            peripheral.set_discoverable()
            CONNECTED = False
        elif evt == EVT_GATTS_WRITE:
            log.info("EVT_GATTS_WRITE %s", binascii.hexlify(data))
        elif evt == EVT_GATTS_READ_PERMIT_REQ:
            ret = on_characteristic_read_request(uuid)
            log.info("EVT_GATTS_READ_PERMIT_REQ %s %s", uuid, ret)
            return ret
        elif evt == EVT_GATTS_WRITE_PERMIT_REQ:
            log.info("EVT_GATTS_WRITE_PERMIT_REQ %s %s",
                     uuid, binascii.hexlify(data))
            return True

    def notify_callback():
        global CONNECTED
        nonlocal peripheral
        if CONNECTED:
            pass

    peripheral = Peripheral(
        os.urandom(6),
        name="uPyKbd",
        connectable=True,
        data=advertisement_data,
        services=[
            service_battery,
            service_device_information,
            service_ble_hid,
            service_scan_parameters
        ],
        event_handler=hid_over_gatt_event_handler
    )
    _thread.start_new_thread(
        peripheral.run,
        tuple(),
        dict(callback=notify_callback, callback_time=5000)
    )
    return peripheral


def process_input(peripheral, data):
    global CONNECTED
    if not CONNECTED:
        log.error("we haven't connected yet...")
        return

    key_list = [0] * 8
    for charc in data:
        hid_value, is_upper_case = hid_keyboard_map(charc)
        key_list[0] = 0x02 if is_upper_case else 0x00
        key_list[2] = hid_value
        key_bytes = bytes(key_list)
        peripheral.write_uuid(CHARACTERISTIC_REPORT_UUID, key_bytes)
        peripheral.write_uuid(CHARACTERISTIC_REPORT_UUID,
                              RESPONSE_HID_EMPTY_BYTES)

    log.info("processed input:%s", data)


if __name__ == "__main__":
    main()
    # import utime; from api_hid_over_gatt import process_input, main; p = main()
    # utime.sleep(5); process_input(p, b"Hello, world!")
