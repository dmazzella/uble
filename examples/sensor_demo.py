# -*- coding: utf-8 -*-
import pyb
import gc
import ustruct
import urandom
from micropython import const

gc.threshold(4096)

import logging
from binascii import hexlify

from bluetooth_low_energy.modules.st_microelectronics.spbtle_rf import SPBTLE_RF
from bluetooth_low_energy.protocols.hci import HCI_EVENT_PKT
from bluetooth_low_energy.protocols.hci.event import (
    EVT_DISCONN_COMPLETE,
    EVT_LE_CONN_COMPLETE,
    EVT_LE_META_EVENT,
    EVT_VENDOR,
    HCI_EVENT)
from bluetooth_low_energy.protocols.hci.status import BLE_STATUS_SUCCESS
from bluetooth_low_energy.protocols.hci.uart import HCI_UART
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.constant import (
    AD_TYPE_COMPLETE_LOCAL_NAME,
    ADV_IND,
    ATTR_PERMISSION_NONE,
    ATTR_ACCESS_READ_ONLY,
    BONDING,
    CHAR_FORMAT_DESC_UUID,
    CHAR_PROP_NOTIFY,
    CHAR_PROP_READ,
    CHAR_PROP_WRITE,
    CHAR_PROP_WRITE_WITHOUT_RESP,
    CHAR_VALUE_LEN_VARIABLE,
    CHAR_VALUE_LEN_CONSTANT,
    CONFIG_DATA_MODE_LEN,
    CONFIG_DATA_MODE_OFFSET,
    CONFIG_DATA_PUBADDR_LEN,
    CONFIG_DATA_PUBADDR_OFFSET,
    FORMAT_SINT16,
    FORMAT_SINT24,
    FORMAT_UINT16,
    GAP_CENTRAL_ROLE_IDB05A1,
    GAP_PERIPHERAL_ROLE_IDB05A1,
    GATT_DONT_NOTIFY_EVENTS,
    GATT_NOTIFY_ATTRIBUTE_WRITE,
    GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
    MAX_ADV_DATA_LEN,
    MAX_ENCRY_KEY_SIZE,
    MIN_ENCRY_KEY_SIZE,
    MITM_PROTECTION_REQUIRED,
    NO_WHITE_LIST_USE,
    OOB_AUTH_DATA_ABSENT,
    PRIMARY_SERVICE,
    PRIVACY_DISABLED,
    PUBLIC_ADDR,
    RESET_NORMAL,
    SECONDARY_SERVICE,
    USE_FIXED_PIN_FOR_PAIRING,
    UUID_TYPE_128,
    UUID_TYPE_16,
    UNIT_TEMP_CELSIUS,
    UNIT_PRESSURE_BAR,
    UNIT_UNITLESS)
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.event import (
    EVT_BLUE_GATT_ATTRIBUTE_MODIFIED,
    EVT_BLUE_GATT_READ_PERMIT_REQ,
    EVT_BLUE_HAL_INITIALIZED)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("examples.sensor_demo")

X_OFFSET = const(200)
Y_OFFSET = const(50)
Z_OFFSET = const(1000)

class SensorDemo(SPBTLE_RF):
    """
    This application contains an example which shows how implementing a proprietary
    Bluetooth Low Energy profile: the sensor profile with emulated sensors data.

    This profile exposes two services:
    - acceleration service
    - environmental service.

    Acceleration service exposes these characteristics:
    - free-fall characteristic (read & notify properties): it is not used on SensorDemo version
      since no real accelerometer is used.

    - acceleration characteristic (read & notify properties): emulated/random values.
      Each value is made up of six bytes. Each couple of bytes contains the emulated acceleration
      on one of the 3 axes (random values).

    Environmental service exposes these characteristics:
    -  temperature, pressure and humidity chracteristics (read property):
       emulated/random values. For each characteristic, a characteristic format descriptor
       is present to describe the type of data contained inside the characteristic.
    """
    def __init__(self, *args, **kwargs):
        super(SensorDemo, self).__init__(*args, **kwargs)
        self.bdaddr = bytes(reversed([0x12, 0x34, 0x00, 0xE1, 0x80, 0x02]))
        self.connection_handle = None
        self.name = b'BlueNRG'

        self.acc_serv_handle = None
        self.free_fall_char_handle = None
        self.acc_char_handle = None

        self.env_serv_handle = None
        self.temp_char_handle = None
        self.press_char_handle = None
        self.humidity_char_handle = None

        self.reset()

    def run(self, timeout=250):
        super(SensorDemo, self).run(timeout=timeout)

    def __start__(self):

        # Reset BlueNRG-MS
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=EVT_BLUE_HAL_INITIALIZED).struct.reason_code != RESET_NORMAL:
            raise ValueError("reason_code")

        # Get the BlueNRG FW versions
        version = self.get_version()
        log.info("current version %s", version)

        # Reset BlueNRG again otherwise we won't be able to change its MAC address.
        # aci_hal_write_config_data() must be the first command after reset otherwise it will fail.
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=EVT_BLUE_HAL_INITIALIZED).struct.reason_code != RESET_NORMAL:
            raise ValueError("reason_code")

        # Configure BlueNRG address as public (its public address is used)
        result = self.aci_hal_write_config_data(
            offset=CONFIG_DATA_PUBADDR_OFFSET,
            length=CONFIG_DATA_PUBADDR_LEN,
            data=self.bdaddr
        ).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_write_config_data status: {:02x}".format(
                result.status))
        log.debug("aci_hal_write_config_data PUBADDR: %02x", result.status)

        # Configure BlueNRG Mode
        result = self.aci_hal_write_config_data(
            offset=CONFIG_DATA_MODE_OFFSET,
            length=CONFIG_DATA_MODE_LEN,
            data=b'\x02').response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_write_config_data status: {:02x}".format(
                result.status))
        log.debug("aci_hal_write_config_data MODE: %02x", result.status)

        # Init BlueNRG GATT layer
        result = self.aci_gatt_init().response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_init status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_init %02x", result.status)

        # Init BlueNRG GAP layer as peripheral or central
        result = self.aci_gap_init_IDB05A1(
            role=GAP_PERIPHERAL_ROLE_IDB05A1,
            privacy_enabled=bool(PRIVACY_DISABLED),
            device_name_char_len=len(self.name)).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_init status: {:02x}".format(
                result.status))
        log.debug("aci_gap_init %02x", result.status)

        service_handle = result.service_handle
        dev_name_char_handle = result.dev_name_char_handle
        appearance_char_handle = result.appearance_char_handle

        # Init BlueNRG GATT layer
        result = self.aci_gatt_update_char_value(
            serv_handle=service_handle,
            char_handle=dev_name_char_handle,
            char_val_offset=0,
            char_value_len=len(self.name),
            char_value=self.name).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

        result = self.aci_gap_set_auth_requirement(
            mitm_mode=MITM_PROTECTION_REQUIRED,
            oob_enable=bool(OOB_AUTH_DATA_ABSENT),
            oob_data=b'\x00'*16,
            min_encryption_key_size=MIN_ENCRY_KEY_SIZE,
            max_encryption_key_size=MAX_ENCRY_KEY_SIZE,
            use_fixed_pin=bool(USE_FIXED_PIN_FOR_PAIRING),
            fixed_pin=123456,
            bonding_mode=BONDING).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_set_auth_requirement status: {:02x}".format(
                result.status))
        log.debug("aci_gap_set_auth_requirement %02x", result.status)

        # Add services
        self.add_acc_service()
        self.add_environmental_sensor_service()

        # Set output power level
        result = self.aci_hal_set_tx_power_level(
            en_high_power=1,
            pa_level=4).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_set_tx_power_level status: {:02x}".format(
                result.status))
        log.debug("aci_hal_set_tx_power_level %02x", result.status)

        self.set_connectable()

    def add_acc_service(self):
        acc_service_uuid = bytes(
            reversed([0x02, 0x36, 0x6e, 0x80, 0xcf, 0x3a, 0x11, 0xe1,
                      0x9a, 0xb4, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        free_fall_char_uuid = bytes(
            reversed([0xe2, 0x3e, 0x78, 0xa0, 0xcf, 0x4a, 0x11, 0xe1,
                      0x8f, 0xfc, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        acc_char_uuid = bytes(
            reversed([0x34, 0x0a, 0x1b, 0x80, 0xcf, 0x4b, 0x11, 0xe1,
                      0xac, 0x36, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))

        result = self.aci_gatt_add_serv(
            service_uuid_type=UUID_TYPE_128,
            service_uuid=acc_service_uuid,
            service_type=PRIMARY_SERVICE,
            max_attr_records=7).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_serv status: {:02x}".format(
                result.status))
        log.info("#acc_serv_handle %04x", result.handle)
        self.acc_serv_handle = result.handle

        result = self.aci_gatt_add_char(
            service_handle=self.acc_serv_handle,
            char_uuid_type=UUID_TYPE_128,
            char_uuid=free_fall_char_uuid,
            char_value_len=1,
            char_properties=CHAR_PROP_NOTIFY,
            sec_permissions=ATTR_PERMISSION_NONE,
            gatt_evt_mask=GATT_DONT_NOTIFY_EVENTS,
            encry_key_size=MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.free_fall_char_handle = result.handle
        log.info("#free_fall_char_handle: %04x", self.free_fall_char_handle)

        result = self.aci_gatt_add_char(
            service_handle=self.acc_serv_handle,
            char_uuid_type=UUID_TYPE_128,
            char_uuid=acc_char_uuid,
            char_value_len=6,
            char_properties=CHAR_PROP_NOTIFY|CHAR_PROP_READ,
            sec_permissions=ATTR_PERMISSION_NONE,
            gatt_evt_mask=GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
            encry_key_size=MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.acc_char_handle = result.handle
        log.info("#acc_char_handle: %04x", self.acc_char_handle)

    def free_fall_notify(self):
        val = ustruct.pack('<B', 0x01)
        result = self.aci_gatt_update_char_value(
            serv_handle=self.acc_serv_handle,
            char_handle=self.free_fall_char_handle,
            char_val_offset=0,
            char_value_len=1,
            char_value=val).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))

    def acc_update(self):
        #accel = pyb.Accel()
        #axis_x, axis_y, axis_z = accel.x(), accel.y(), accel.z()
        axis_x, axis_y, axis_z = (
            urandom.randint(0, 32767) % X_OFFSET,
            urandom.randint(0, 32767) % Y_OFFSET,
            urandom.randint(0, 32767) % Z_OFFSET)
        buffer = ustruct.pack(
            "<HHH",
            axis_x, axis_y, axis_z)
        result = self.aci_gatt_update_char_value(
            serv_handle=self.acc_serv_handle,
            char_handle=self.acc_char_handle,
            char_val_offset=0,
            char_value_len=len(buffer),
            char_value=buffer).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

    def add_environmental_sensor_service(self):
        env_service_uuid = bytes(
            reversed([0x42, 0x82, 0x1a, 0x40, 0xe4, 0x77, 0x11, 0xe2,
                      0x82, 0xd0, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        temp_char_uuid = bytes(
            reversed([0xa3, 0x2e, 0x55, 0x20, 0xe4, 0x77, 0x11, 0xe2,
                      0xa9, 0xe3, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        press_char_uuid = bytes(
            reversed([0xcd, 0x20, 0xc4, 0x80, 0xe4, 0x8b, 0x11, 0xe2,
                      0x84, 0x0b, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        humidity_char_uuid = bytes(
            reversed([0x01, 0xc5, 0x0b, 0x60, 0xe4, 0x8c, 0x11, 0xe2,
                      0xa0, 0x73, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))

        char_format_struct = "<BBHBH"
        char_format_size = ustruct.calcsize(char_format_struct)

        max_attr_records = 6
        result = self.aci_gatt_add_serv(
            service_uuid_type=UUID_TYPE_128,
            service_uuid=env_service_uuid,
            service_type=PRIMARY_SERVICE,
            max_attr_records=(1+3*max_attr_records)).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_serv status: {:02x}".format(
                result.status))
        log.info("#env_serv_handle %04x", result.handle)
        self.env_serv_handle = result.handle

        # Temperature Characteristic
        result = self.aci_gatt_add_char(
            service_handle=self.env_serv_handle,
            char_uuid_type=UUID_TYPE_128,
            char_uuid=temp_char_uuid,
            char_value_len=1,
            char_properties=CHAR_PROP_READ,
            sec_permissions=ATTR_PERMISSION_NONE,
            gatt_evt_mask=GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
            encry_key_size=MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.temp_char_handle = result.handle
        log.info("#temp_char_handle: %04x", self.temp_char_handle)

        uuid16 = ustruct.pack(
            "<H",
            CHAR_FORMAT_DESC_UUID)

        char_format = ustruct.pack(
            char_format_struct,
            FORMAT_SINT16, -1, UNIT_TEMP_CELSIUS, 0, 0)

        result = self.aci_gatt_add_char_desc(
            service_handle=self.env_serv_handle,
            char_handle=self.temp_char_handle,
            desc_uuid_type=UUID_TYPE_16,
            uuid=uuid16,
            desc_value_max_len=char_format_size,
            desc_value_len=char_format_size,
            desc_value=char_format,
            sec_permissions=ATTR_PERMISSION_NONE,
            acc_permissions=ATTR_ACCESS_READ_ONLY,
            gatt_evt_mask=GATT_DONT_NOTIFY_EVENTS,
            encry_key_size=MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char_desc status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_add_char_desc %02x", result.status)

        # Pressure Characteristic
        result = self.aci_gatt_add_char(
            service_handle=self.env_serv_handle,
            char_uuid_type=UUID_TYPE_128,
            char_uuid=press_char_uuid,
            char_value_len=2,
            char_properties=CHAR_PROP_READ,
            sec_permissions=ATTR_PERMISSION_NONE,
            gatt_evt_mask=GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
            encry_key_size=MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.press_char_handle = result.handle
        log.info("#press_char_handle: %04x", self.press_char_handle)

        char_format = ustruct.pack(
            char_format_struct,
            FORMAT_SINT24, -5, UNIT_PRESSURE_BAR, 0, 0)

        result = self.aci_gatt_add_char_desc(
            service_handle=self.env_serv_handle,
            char_handle=self.press_char_handle,
            desc_uuid_type=UUID_TYPE_16,
            uuid=uuid16,
            desc_value_max_len=char_format_size,
            desc_value_len=char_format_size,
            desc_value=char_format,
            sec_permissions=ATTR_PERMISSION_NONE,
            acc_permissions=ATTR_ACCESS_READ_ONLY,
            gatt_evt_mask=GATT_DONT_NOTIFY_EVENTS,
            encry_key_size=MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char_desc status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_add_char_desc %02x", result.status)

        # Humidity Characteristic
        result = self.aci_gatt_add_char(
            service_handle=self.env_serv_handle,
            char_uuid_type=UUID_TYPE_128,
            char_uuid=humidity_char_uuid,
            char_value_len=2,
            char_properties=CHAR_PROP_READ,
            sec_permissions=ATTR_PERMISSION_NONE,
            gatt_evt_mask=GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
            encry_key_size=MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.humidity_char_handle = result.handle
        log.info("#humidity_char_handle: %04x", self.humidity_char_handle)

        char_format = ustruct.pack(
            char_format_struct,
            FORMAT_UINT16, -1, UNIT_UNITLESS, 0, 0)

        result = self.aci_gatt_add_char_desc(
            service_handle=self.env_serv_handle,
            char_handle=self.humidity_char_handle,
            desc_uuid_type=UUID_TYPE_16,
            uuid=uuid16,
            desc_value_max_len=char_format_size,
            desc_value_len=char_format_size,
            desc_value=char_format,
            sec_permissions=ATTR_PERMISSION_NONE,
            acc_permissions=ATTR_ACCESS_READ_ONLY,
            gatt_evt_mask=GATT_DONT_NOTIFY_EVENTS,
            encry_key_size=MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char_desc status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_add_char_desc %02x", result.status)

    def temp_update(self):
        buffer = ustruct.pack(
            "<B",
            (270 + urandom.randint(0, 32767)))
        result = self.aci_gatt_update_char_value(
            serv_handle=self.env_serv_handle,
            char_handle=self.temp_char_handle,
            char_val_offset=0,
            char_value_len=len(buffer),
            char_value=buffer).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

    def press_update(self):
        buffer = ustruct.pack(
            "<H",
            100000 + urandom.randint(0, 32767))
        result = self.aci_gatt_update_char_value(
            serv_handle=self.env_serv_handle,
            char_handle=self.press_char_handle,
            char_val_offset=0,
            char_value_len=len(buffer),
            char_value=buffer).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

    def humidity_update(self):
        buffer = ustruct.pack(
            "<H",
            (450 + urandom.randint(0, 32767) * 100))
        result = self.aci_gatt_update_char_value(
            serv_handle=self.env_serv_handle,
            char_handle=self.humidity_char_handle,
            char_val_offset=0,
            char_value_len=len(buffer),
            char_value=buffer).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

    def set_connectable(self):

        local_name = ustruct.pack(
            "<B{:d}s".format(
                len(self.name)
            ),
            AD_TYPE_COMPLETE_LOCAL_NAME, self.name)

        # disable scan response
        result = self.hci_le_set_scan_resp_data(
            length=MAX_ADV_DATA_LEN,
            data=b'\x00'*MAX_ADV_DATA_LEN).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("hci_le_set_scan_resp_data status: {:02x}".format(
                result.status))
        log.debug("hci_le_set_scan_resp_data %02x", result.status)

        # General Discoverable Mode
        result = self.aci_gap_set_discoverable(
            adv_type=ADV_IND,
            adv_interv_min=0,
            adv_interv_max=0,
            own_addr_type=PUBLIC_ADDR,
            adv_filter_policy=NO_WHITE_LIST_USE,
            local_name_len=len(local_name),
            local_name=local_name,
            service_uuid_len=0,
            service_uuid_list=b'',
            slave_conn_interv_min=0,
            slave_conn_interv_max=0).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_set_discoverable status: {:02x}".format(
                result.status))
        log.debug("aci_gap_set_discoverable %02x", result.status)

    def __stop__(self):
        # Reset BlueNRG-MS
        self.reset()

    def __process__(self, event):
        # Process event received from BlueNRG-MS
        hci_uart = HCI_UART.from_buffer(event)
        log.debug(hci_uart)
        if hci_uart.pkt_type == HCI_EVENT_PKT:
            hci_evt = HCI_EVENT.from_buffer(hci_uart.data)
            log.debug(hci_evt)
            if hci_evt.evtcode == EVT_DISCONN_COMPLETE:
                self.gap_disconnection_complete_cb()
            elif hci_evt.evtcode == EVT_LE_META_EVENT:
                if hci_evt.subevtcode == EVT_LE_CONN_COMPLETE:
                    self.gap_connection_complete_cb(
                        hci_evt.struct.peer_bdaddr,
                        hci_evt.struct.handle
                    )
            elif hci_evt.evtcode == EVT_VENDOR:
                if hci_evt.subevtcode == EVT_BLUE_GATT_ATTRIBUTE_MODIFIED:
                    self.attribute_modified_cb(
                        hci_evt.struct.attr_handle,
                        hci_evt.struct.data_length,
                        hci_evt.struct.att_data[:hci_evt.struct.data_length]
                    )
                elif hci_evt.subevtcode == EVT_BLUE_GATT_READ_PERMIT_REQ:
                    self.read_request_cb(hci_evt.struct.attr_handle)

        # self.free_fall_notify()
        self.acc_update()

    def gap_connection_complete_cb(self, address, handle):
        log.info("gap_connection_complete_cb")
        self.connection_handle = handle

    def gap_disconnection_complete_cb(self):
        log.info("gap_disconnection_complete_cb")
        self.connection_handle = None
        self.set_connectable()

    def attribute_modified_cb(self, handle, data_length, att_data):
        log.debug("attribute_modified_cb %04x %d %s", 
                  handle, data_length, hexlify(att_data))

    def read_request_cb(self, handle):
        log.debug("read_request_cb %04x", handle)
        if handle == self.acc_char_handle + 1:
            self.acc_update()
        elif handle == self.temp_char_handle + 1:
            self.temp_update()
        elif handle == self.press_char_handle + 1:
            self.press_update()
        elif handle == self.humidity_char_handle + 1:
            self.humidity_update()

        if self.connection_handle is not None:
            result = self.aci_gatt_allow_read(
                conn_handle=self.connection_handle).response_struct
            if result.status != BLE_STATUS_SUCCESS:
                raise ValueError("aci_gatt_allow_read status: {:02x}".format(
                    result.status))
            log.debug("aci_gatt_allow_read %02x", result.status)
