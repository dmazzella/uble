# -*- coding: utf-8 -*-
import pyb
import gc
import ustruct
import urandom
import utime
from micropython import const

gc.threshold(4096)

import logging
from binascii import hexlify

from bluetooth_low_energy.modules.st_microelectronics.spbtle_rf import SPBTLE_RF
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms import event as st_event
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms import constant as st_constant
from bluetooth_low_energy.protocols.hci import HCI_EVENT_PKT
from bluetooth_low_energy.protocols.hci import uart
from bluetooth_low_energy.protocols.hci import event
from bluetooth_low_energy.protocols.hci import status

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("examples.bluest_protocol")


ACCELEROMETER_EXAMPLE = const(1)
GYROSCOPE_EXAMPLE = const(1)
MAGNETOMETER_EXAMPLE = const(1)
TEMPERATURE_EXAMPLE = const(1)
PRESS_EXAMPLE = const(1)
PWR_EXAMPE = const(1)
USE_CUSTOM_ALGORITHM1 = const(0)

HW_CAP_ACCEL = const(0x80)
HW_CAP_GYRO = const(0x40)
HW_CAP_MAGN = const(0x20)
HW_CAP_PRESS = const(0x10)
HW_CAP_HUMIDITY = const(0x08)
HW_CAP_TEMPERATURE = const(0x04)
HW_CAP_GG = const(0x02)
HW_CAP_RFID = const(0x01)

X_OFFSET = const(200)
Y_OFFSET = const(50)
Z_OFFSET = const(1000)

class BlueSTProtocol(SPBTLE_RF):
    """
    BlueST Protocol Demo
    """
    def __init__(self, *args, **kwargs):
        super(BlueSTProtocol, self).__init__(*args, **kwargs)

        self.rtc = pyb.RTC()
        self.rtc.datetime((2017, 1, 1, 0, 0, 0, 0, 0))

        self.bdaddr = bytes(reversed([0x12, 0x34, 0x00, 0xE1, 0x80, 0x02]))
        self.name = b'PyBLE'

        self.connection_handle = None

        self.service_handle = None
        self.dev_name_char_handle = None
        self.appearance_char_handle = None

        self.hw_serv_handle = None
        self.acc_gyro_mag_bluest_char_handle = None
        self.pressure_bluest_char_handle = None
        self.temperature_bluest_char_handle = None
        self.pwr_bluest_char_handle = None

        self.reset()

    def run(self, timeout=250):
        try:
            self.__start__()
            start = pyb.millis()
            while True:
                for evt in self.hci_isr(timeout):
                    self.__process__(evt)
                if pyb.elapsed_millis(start) >= 1000 and \
                    self.connection_handle is not None:
                    if any([ACCELEROMETER_EXAMPLE,
                            GYROSCOPE_EXAMPLE,
                            MAGNETOMETER_EXAMPLE]):
                        self.accgyromag_update()
                    if TEMPERATURE_EXAMPLE:
                        self.temp_update()
                    if PRESS_EXAMPLE:
                        self.press_update()
                    if PWR_EXAMPE:
                        self.pwr_update()
                    start = pyb.millis()
        except (KeyboardInterrupt, StopIteration):
            pass
        finally:
            self.__stop__()

    def __start__(self):
        # Reset BlueNRG-MS
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=st_event.EVT_BLUE_HAL_INITIALIZED
            ).struct.reason_code != st_constant.RESET_NORMAL:
            raise ValueError("reason_code")

        # Get the BlueNRG FW versions
        version = self.get_version()
        log.info("current version %s", version)

        # Reset BlueNRG again otherwise we won't be able to change its MAC address.
        # aci_hal_write_config_data() must be the first command after reset otherwise it will fail.
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=st_event.EVT_BLUE_HAL_INITIALIZED
            ).struct.reason_code != st_constant.RESET_NORMAL:
            raise ValueError("reason_code")

            # Configure BlueNRG address as public (its public address is used)
        result = self.aci_hal_write_config_data(
            offset=st_constant.CONFIG_DATA_PUBADDR_OFFSET,
            length=st_constant.CONFIG_DATA_PUBADDR_LEN,
            data=self.bdaddr
        ).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_write_config_data status: {:02x}".format(
                result.status))
        log.debug("aci_hal_write_config_data PUBADDR: %02x", result.status)

        # Init BlueNRG GATT layer
        result = self.aci_gatt_init().response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_init status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_init %02x", result.status)

        # Init BlueNRG GAP layer as peripheral or central
        result = self.aci_gap_init_IDB05A1(
            role=st_constant.GAP_PERIPHERAL_ROLE_IDB05A1,
            privacy_enabled=bool(st_constant.PRIVACY_DISABLED),
            device_name_char_len=len(self.name)).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_init status: {:02x}".format(
                result.status))
        log.debug("aci_gap_init %02x", result.status)

        self.service_handle = result.service_handle
        self.dev_name_char_handle = result.dev_name_char_handle
        self.appearance_char_handle = result.appearance_char_handle

        # Init BlueNRG GATT layer
        result = self.aci_gatt_update_char_value(
            serv_handle=self.service_handle,
            char_handle=self.dev_name_char_handle,
            char_val_offset=0,
            char_value_len=len(self.name),
            char_value=self.name).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

        result = self.aci_gap_set_auth_requirement(
            mitm_mode=st_constant.MITM_PROTECTION_REQUIRED,
            oob_enable=bool(st_constant.OOB_AUTH_DATA_ABSENT),
            oob_data=b'\x00'*16,
            min_encryption_key_size=st_constant.MIN_ENCRY_KEY_SIZE,
            max_encryption_key_size=st_constant.MAX_ENCRY_KEY_SIZE,
            use_fixed_pin=bool(st_constant.USE_FIXED_PIN_FOR_PAIRING),
            fixed_pin=123456,
            bonding_mode=st_constant.BONDING).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_set_auth_requirement status: {:02x}".format(
                result.status))
        log.debug("aci_gap_set_auth_requirement %02x", result.status)

        # Add services
        self.add_feature_service()

        # Set output power level
        result = self.aci_hal_set_tx_power_level(
            en_high_power=1,
            pa_level=5).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_set_tx_power_level status: {:02x}".format(
                result.status))
        log.debug("aci_hal_set_tx_power_level %02x", result.status)

    def add_feature_service(self):
        hw_sens_bluest_service_uuid = bytes(
            reversed([0x00, 0x00, 0x00, 0x00,
                      0x00, 0x01, 0x11, 0xe1, 0x9a, 0xb4, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        acc_gyro_mag_bluest_char_uuid = bytes(
            reversed([0x00, 0xE0, 0x00, 0x00,
                      0x00, 0x01, 0x11, 0xe1, 0xac, 0x36, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        pressure_bluest_char_uuid = bytes(
            reversed([0x00, 0x10, 0x00, 0x00,
                      0x00, 0x01, 0x11, 0xe1, 0xac, 0x36, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        temperature_bluest_char_uuid = bytes(
            reversed([0x00, 0x04, 0x00, 0x00,
                      0x00, 0x01, 0x11, 0xe1, 0xac, 0x36, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))
        pwr_bluest_char_uuid = bytes(
            reversed([0x00, 0x02, 0x00, 0x00,
                      0x00, 0x01, 0x11, 0xe1, 0xac, 0x36, 0x00, 0x02, 0xa5, 0xd5, 0xc5, 0x1b]))

        max_attr_records = 6
        result = self.aci_gatt_add_serv(
            service_uuid_type=st_constant.UUID_TYPE_128,
            service_uuid=hw_sens_bluest_service_uuid,
            service_type=st_constant.PRIMARY_SERVICE,
            max_attr_records=(1+3*max_attr_records)).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_serv status: {:02x}".format(
                result.status))
        log.info("#hw_serv_handle %04x", result.handle)
        self.hw_serv_handle = result.handle

        result = self.aci_gatt_add_char(
            service_handle=self.hw_serv_handle,
            char_uuid_type=st_constant.UUID_TYPE_128,
            char_uuid=acc_gyro_mag_bluest_char_uuid,
            char_value_len=(2+3*3*2),
            char_properties=st_constant.CHAR_PROP_NOTIFY|st_constant.CHAR_PROP_READ,
            sec_permissions=st_constant.ATTR_PERMISSION_NONE,
            gatt_evt_mask=st_constant.GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
            encry_key_size=st_constant.MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.acc_gyro_mag_bluest_char_handle = result.handle
        log.info("#acc_gyro_mag_bluest_char_handle: %04x",
            self.acc_gyro_mag_bluest_char_handle)

        result = self.aci_gatt_add_char(
            service_handle=self.hw_serv_handle,
            char_uuid_type=st_constant.UUID_TYPE_128,
            char_uuid=pressure_bluest_char_uuid,
            char_value_len=(4+2),
            char_properties=st_constant.CHAR_PROP_NOTIFY|st_constant.CHAR_PROP_READ,
            sec_permissions=st_constant.ATTR_PERMISSION_NONE,
            gatt_evt_mask=st_constant.GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
            encry_key_size=st_constant.MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.pressure_bluest_char_handle = result.handle
        log.info("#pressure_bluest_char_handle: %04x",
                 self.pressure_bluest_char_handle)

        result = self.aci_gatt_add_char(
            service_handle=self.hw_serv_handle,
            char_uuid_type=st_constant.UUID_TYPE_128,
            char_uuid=temperature_bluest_char_uuid,
            char_value_len=(2+2),
            char_properties=st_constant.CHAR_PROP_NOTIFY|st_constant.CHAR_PROP_READ,
            sec_permissions=st_constant.ATTR_PERMISSION_NONE,
            gatt_evt_mask=st_constant.GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
            encry_key_size=st_constant.MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.temperature_bluest_char_handle = result.handle
        log.info("#temperature_bluest_char_handle: %04x",
                 self.temperature_bluest_char_handle)

        result = self.aci_gatt_add_char(
            service_handle=self.hw_serv_handle,
            char_uuid_type=st_constant.UUID_TYPE_128,
            char_uuid=pwr_bluest_char_uuid,
            char_value_len=9,
            char_properties=st_constant.CHAR_PROP_NOTIFY|st_constant.CHAR_PROP_READ,
            sec_permissions=st_constant.ATTR_PERMISSION_NONE,
            gatt_evt_mask=st_constant.GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
            encry_key_size=st_constant.MAX_ENCRY_KEY_SIZE,
            is_variable=False).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_add_char status: {:02x}".format(
                result.status))
        self.pwr_bluest_char_handle = result.handle
        log.info("#pwr_bluest_char_handle: %04x",
                 self.pwr_bluest_char_handle)

        self.set_connectable()

    def accgyromag_update(self):
        # accel = pyb.Accel()
        # acc_axis_x, acc_axis_y, acc_axis_z = accel.x(), accel.y(), accel.z()
        tick = utime.time()
        acc_axis_x, acc_axis_y, acc_axis_z = (
            urandom.randint(0, 32767) % X_OFFSET,
            urandom.randint(0, 32767) % Y_OFFSET,
            urandom.randint(0, 32767) % Z_OFFSET)
        gyto_axis_x, gyto_axis_y, gyto_axis_z = (
            urandom.randint(0, 32767) % X_OFFSET,
            urandom.randint(0, 32767) % Y_OFFSET,
            urandom.randint(0, 32767) % Z_OFFSET)
        mag_axis_x, mag_axis_y, mag_axis_z = (
            urandom.randint(0, 32767) % X_OFFSET,
            urandom.randint(0, 32767) % Y_OFFSET,
            urandom.randint(0, 32767) % Z_OFFSET)

        buffer = ustruct.pack(
            "<HHHHHHHHHH",
            tick,
            acc_axis_x, acc_axis_y, acc_axis_z,
            gyto_axis_x, gyto_axis_y, gyto_axis_z,
            mag_axis_x, mag_axis_y, mag_axis_z)
        result = self.aci_gatt_update_char_value(
            serv_handle=self.hw_serv_handle,
            char_handle=self.acc_gyro_mag_bluest_char_handle,
            char_val_offset=0,
            char_value_len=len(buffer),
            char_value=buffer).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

    def temp_update(self):
        tick = utime.time()
        buffer = ustruct.pack(
            "<HB",
            tick,
            (270 + urandom.randint(0, 32767)))
        result = self.aci_gatt_update_char_value(
            serv_handle=self.hw_serv_handle,
            char_handle=self.temperature_bluest_char_handle,
            char_val_offset=0,
            char_value_len=len(buffer),
            char_value=buffer).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

    def pwr_update(self):
        tick = utime.time()
        chg = urandom.randint(0, 100)
        voltage = urandom.randint(0, 100)
        current = urandom.randint(0, 100)
        npwrstat = urandom.randint(0, 100)
        buffer = ustruct.pack(
            "<HHHHB",
            tick,
            chg, voltage, current, npwrstat)
        result = self.aci_gatt_update_char_value(
            serv_handle=self.hw_serv_handle,
            char_handle=self.pwr_bluest_char_handle,
            char_val_offset=0,
            char_value_len=len(buffer),
            char_value=buffer).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

    def press_update(self):
        tick = utime.time()
        buffer = ustruct.pack(
            "<HI",
            tick,
            100000 + urandom.randint(0, 32767))
        result = self.aci_gatt_update_char_value(
            serv_handle=self.hw_serv_handle,
            char_handle=self.pressure_bluest_char_handle,
            char_val_offset=0,
            char_value_len=len(buffer),
            char_value=buffer).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_update_char_value %02x", result.status)

    def set_connectable(self):
        local_name = ustruct.pack(
            "<B{:d}s".format(
                len(self.name)
            ),
            st_constant.AD_TYPE_COMPLETE_LOCAL_NAME, self.name)

        # disable scan response
        result = self.hci_le_set_scan_resp_data(
            length=st_constant.MAX_ADV_DATA_LEN,
            data=b'\x00'*st_constant.MAX_ADV_DATA_LEN).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("hci_le_set_scan_resp_data status: {:02x}".format(
                result.status))
        log.debug("hci_le_set_scan_resp_data %02x", result.status)

        # General Discoverable Mode
        result = self.aci_gap_set_discoverable(
            adv_type=st_constant.ADV_IND,
            adv_interv_min=0,
            adv_interv_max=0,
            own_addr_type=st_constant.PUBLIC_ADDR,
            adv_filter_policy=st_constant.NO_WHITE_LIST_USE,
            local_name_len=len(local_name),
            local_name=local_name,
            service_uuid_len=0,
            service_uuid_list=b'',
            slave_conn_interv_min=0,
            slave_conn_interv_max=0).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_set_discoverable status: {:02x}".format(
                result.status))
        log.debug("aci_gap_set_discoverable %02x", result.status)

        advbuffer = [
            0x0D, # lenght of MANUF_SPECIFIC advertising item
            st_constant.AD_TYPE_MANUFACTURER_SPECIFIC_DATA, # Type
            0x01, # Protocol version
            0x01, # /Dev ID
            0x00, 0x00, # Group A Features (big endian)
            0x00, 0x00, # Group B Features (big endian)
            0x00, 0x00, 0x00, # Public device address (48 bits) Company assigned
            0x00, 0x00, 0x00, # Public device address (48 bits) Company id
        ]

        advbuffer[4] = 0
        advbuffer[5] = 0
        advbuffer[6] = 0
        advbuffer[7] = 0

        n_added_features_a = 0x0000
        n_added_features_b = 0x0000

        if ACCELEROMETER_EXAMPLE:
            n_added_features_a |= HW_CAP_ACCEL
        if GYROSCOPE_EXAMPLE:
            n_added_features_a |= HW_CAP_GYRO
        if MAGNETOMETER_EXAMPLE:
            n_added_features_a |= HW_CAP_MAGN
        if TEMPERATURE_EXAMPLE:
            n_added_features_a |= HW_CAP_TEMPERATURE
        if PRESS_EXAMPLE:
            n_added_features_a |= HW_CAP_PRESS
        if PWR_EXAMPE:
            pass

        advbuffer[4] = ((n_added_features_a & 0xFF00) >> 8)
        advbuffer[5] = (n_added_features_a & 0xFF)
        if USE_CUSTOM_ALGORITHM1:
            advbuffer[6] = ((n_added_features_b & 0xFF00) >> 8)
            advbuffer[7] = (n_added_features_b & 0xFF)

        advbuffer_bytes = bytes(advbuffer)

        result = self.aci_gap_update_adv_data(
            adv_len=len(advbuffer_bytes),
            adv_data=advbuffer_bytes).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_update_adv_data status: {:02x}".format(
                result.status))
        log.debug("aci_gap_update_adv_data %02x", result.status)

    def __stop__(self):
        # Reset BlueNRG-MS
        self.reset()

    def __process__(self, evt):
        # Process event received from BlueNRG-MS
        hci_uart = uart.HCI_UART.from_buffer(evt)
        log.debug(hci_uart)
        if hci_uart.pkt_type == HCI_EVENT_PKT:
            hci_evt = event.HCI_EVENT.from_buffer(hci_uart.data)
            log.debug(hci_evt)
            if hci_evt.evtcode == event.EVT_DISCONN_COMPLETE:
                self.gap_disconnection_complete_cb()
            elif hci_evt.evtcode == event.EVT_LE_META_EVENT:
                if hci_evt.subevtcode == event.EVT_LE_CONN_COMPLETE:
                    self.gap_connection_complete_cb(
                        hci_evt.struct.peer_bdaddr,
                        hci_evt.struct.handle
                    )
            elif hci_evt.evtcode == event.EVT_VENDOR:
                if hci_evt.subevtcode == st_event.EVT_BLUE_GATT_ATTRIBUTE_MODIFIED:
                    self.attribute_modified_cb(
                        hci_evt.struct.attr_handle,
                        hci_evt.struct.data_length,
                        hci_evt.struct.att_data[:hci_evt.struct.data_length]
                    )
                elif hci_evt.subevtcode == st_event.EVT_BLUE_GATT_WRITE_PERMIT_REQ:
                    result = self.aci_gatt_write_response(
                        conn_handle=self.connection_handle,
                        attr_handle=hci_evt.struct.attr_handle,
                        write_status=False,
                        err_code=0,
                        att_val_len=hci_evt.struct.data_length,
                        att_val=\
                            hci_evt.struct.data[:hci_evt.struct.data_length]
                        ).response_struct
                    if result.status != status.BLE_STATUS_SUCCESS:
                        self.attribute_modified_cb(
                            hci_evt.struct.attr_handle,
                            hci_evt.struct.data_length,
                            hci_evt.struct.data[:hci_evt.struct.data_length]
                        )
                elif hci_evt.subevtcode == st_event.EVT_BLUE_GATT_READ_PERMIT_REQ:
                    self.read_request_cb(hci_evt.struct.attr_handle)

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
        if handle == self.acc_gyro_mag_bluest_char_handle + 1:
            self.accgyromag_update()
        elif handle == self.temperature_bluest_char_handle + 1:
            self.temp_update()
        elif handle == self.pwr_bluest_char_handle + 1:
            self.pwr_update()
        elif handle == self.pressure_bluest_char_handle + 1:
            self.press_update()

        if self.connection_handle is not None:
            result = self.aci_gatt_allow_read(
                conn_handle=self.connection_handle).response_struct
            if result.status != status.BLE_STATUS_SUCCESS:
                raise ValueError("aci_gatt_allow_read status: {:02x}".format(
                    result.status))
            log.debug("aci_gatt_allow_read %02x", result.status)
