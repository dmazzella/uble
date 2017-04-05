# -*- coding: utf-8 -*-
import gc
import pyb
from binascii import hexlify

gc.threshold(4096)

import logging

from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.event import (
    EVT_BLUE_HAL_INITIALIZED,
    EVT_BLUE_GATT_ATTRIBUTE_MODIFIED,
    EVT_BLUE_GATT_NOTIFICATION,
    EVT_BLUE_L2CAP_CONN_UPD_RESP,
    EVT_BLUE_GAP_PROCEDURE_COMPLETE,
    EVT_BLUE_GATT_DISC_READ_CHAR_BY_UUID_RESP,
    EVT_BLUE_GATT_PROCEDURE_COMPLETE,
    EVT_BLUE_GATT_TX_POOL_AVAILABLE)
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.constant import (
    GAP_GENERAL_DISCOVERY_PROC,
    CONFIG_DATA_PUBADDR_LEN,
    CONFIG_DATA_PUBADDR_OFFSET,
    RESET_NORMAL,
    GAP_CENTRAL_ROLE_IDB05A1,
    GAP_PERIPHERAL_ROLE_IDB05A1,
    PRIVACY_DISABLED,
    ADV_IND,
    SCAN_RSP,
    ADV_DIRECT_IND,
    PUBLIC_ADDR,
    RANDOM_ADDR,
    MITM_PROTECTION_REQUIRED,
    OOB_AUTH_DATA_ABSENT,
    MAX_ENCRY_KEY_SIZE,
    MIN_ENCRY_KEY_SIZE,
    USE_FIXED_PIN_FOR_PAIRING,
    BONDING)
from bluetooth_low_energy.protocols.hci.uart import (
    HCI_UART)
from bluetooth_low_energy.protocols.hci import (
    HCI_EVENT_PKT)
from bluetooth_low_energy.protocols.hci.event import (
    EVT_LE_ADVERTISING_REPORT,
    EVT_DISCONN_COMPLETE,
    EVT_LE_CONN_COMPLETE,
    EVT_LE_META_EVENT,
    EVT_VENDOR,
    HCI_EVENT)
from bluetooth_low_energy.modules.st_microelectronics.spbtle_rf import (
    SPBTLE_RF)
from bluetooth_low_energy.protocols.hci.status import (
    BLE_STATUS_SUCCESS)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("examples.discovery")


class Discovery(SPBTLE_RF):
    """
    Simple discovery devices
    """
    def __init__(self, *args, bdaddr=None, **kwargs):
        super(Discovery, self).__init__(*args, **kwargs)
        self.bdaddr = bytearray(reversed([0x00, 0x00, 0x00, 0xE1, 0x80, 0x02]))
        self.name = b'BlueNRG'
        self.connection_handle = None
        self.discovery_time = 1000
        self.connect_bdaddr = bdaddr
        self.client_connection = (isinstance(self.connect_bdaddr, (bytes, bytearray)) and len(self.connect_bdaddr) == 6)


    def run(self, *args, **kwargs):
        def callback():
            log.info("memory free %d", gc.mem_free())

        super(Discovery, self).run(callback=callback, callback_time=self.discovery_time)

    def __start__(self):
        # Reset BlueNRG-MS
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=EVT_BLUE_HAL_INITIALIZED
            ).struct.reason_code != RESET_NORMAL:
            raise ValueError("reason_code")

        # Get a random number from BlueNRG-MS
        result = self.hci_le_rand().response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("hci_le_rand status: {:02x}".format(
                result.status))
        log.debug("hci_le_rand: %02x", result.status)

        # Setup discovery time with random number
        for i in range(8):
            self.discovery_time += (2 * result.random[i])

        # Setup last 3 bytes of public address with random number
        self.bdaddr[3] = result.random[0]
        self.bdaddr[4] = result.random[3]
        self.bdaddr[5] = result.random[6]

        # Reset BlueNRG-MS again otherwise we won't be able to change its MAC address.
        # aci_hal_write_config_data() must be the first command after reset otherwise it will fail.
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=EVT_BLUE_HAL_INITIALIZED).struct.reason_code != RESET_NORMAL:
            raise ValueError("reason_code")

        # Configure BlueNRG-MS address as public (its public address is used)
        result = self.aci_hal_write_config_data(
            offset=CONFIG_DATA_PUBADDR_OFFSET,
            length=CONFIG_DATA_PUBADDR_LEN,
            data=self.bdaddr
        ).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_write_config_data status: {:02x}".format(
                result.status))
        log.debug("aci_hal_write_config_data PUBADDR: %02x", result.status)

        log.info("Public address: %s", hexlify(self.bdaddr, ":"))

        # Init BlueNRG-MS GATT layer
        result = self.aci_gatt_init().response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_init status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_init %02x", result.status)

        # Init BlueNRG-MS GAP layer as peripheral or central
        result = self.aci_gap_init_IDB05A1(
            role=GAP_CENTRAL_ROLE_IDB05A1 \
                if not self.client_connection else GAP_PERIPHERAL_ROLE_IDB05A1,
            privacy_enabled=bool(PRIVACY_DISABLED),
            device_name_char_len=len(self.name)).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_init status: {:02x}".format(
                result.status))
        log.debug("aci_gap_init %02x", result.status)

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

        # Set output power level
        result = self.aci_hal_set_tx_power_level(
            en_high_power=1,
            pa_level=4).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_set_tx_power_level status: {:02x}".format(
                result.status))
        log.debug("aci_hal_set_tx_power_level %02x", result.status)

        if not self.client_connection:
            log.info("CENTRAL: BLE Stack Initialized")
            self.start_discovery()
        else:
            log.info("PERIPHERAL: BLE Stack Initialized")
            self.start_connection(self.connect_bdaddr)

    def __stop__(self):
        # Reset BlueNRG-MS
        self.reset()

    def start_discovery(self):
        result = self.aci_gap_start_general_discovery_proc(
            scan_interval=0x500,
            scan_window=0x500,
            own_address_type=PUBLIC_ADDR, # public address
            filter_duplicates=0x01).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError(
                "aci_gap_start_general_discovery_proc status: {:02x}".format(
                    result.status))
        log.info("aci_gap_start_general_discovery_proc %02x", result.status)

    def stop_discovery(self):
        result = self.aci_gap_terminate_gap_procedure(
            procedure_code=0x02).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_terminate_gap_procedure status: {:02x}".format(
                result.status))
        log.debug("aci_gap_terminate_gap_procedure %02x", result.status)

    def start_connection(self, bdaddr):
        # Do connection with first discovered device
        result = self.aci_gap_create_connection(
            scan_interval=100*1000//625,
            scan_window=50*1000//625,
            peer_bdaddr_type=PUBLIC_ADDR,
            peer_bdaddr=bdaddr,
            own_bdaddr_type=PUBLIC_ADDR,
            conn_min_interval=22*100//125,
            conn_max_interval=22*100//125,
            conn_latency=0,
            supervision_timeout=500//10,
            min_conn_length=22*1000//625,
            max_conn_length=22*1000//625).response_struct
        if result.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_create_connection status: {:02x}".format(
                result.status))
        log.info("aci_gap_create_connection %02x", result.status)

    def __process__(self, event):
        # Process event received from BlueNRG-MS
        hci_uart = HCI_UART.from_buffer(event)
        log.debug("%s", hci_uart)
        if hci_uart.pkt_type == HCI_EVENT_PKT:
            hci_evt = HCI_EVENT.from_buffer(hci_uart.data)
            log.debug("%s", hci_evt)
            if hci_evt.evtcode == EVT_DISCONN_COMPLETE:
                log.info("EVT_DISCONN_COMPLETE")
                self.disconnection_complete_cb()

            elif hci_evt.evtcode == EVT_LE_META_EVENT:
                log.info("EVT_LE_META_EVENT")

                if hci_evt.subevtcode == EVT_LE_CONN_COMPLETE:
                    log.info("EVT_LE_CONN_COMPLETE")
                    self.connection_complete_cb(hci_evt.struct.peer_bdaddr, hci_evt.struct.handle)
                    # result = self.aci_gap_terminate_gap_procedure(
                    #     procedure_code=0x00
                    # ).response_struct
                    # if result.status != BLE_STATUS_SUCCESS:
                    #     raise ValueError("aci_gap_terminate_gap_procedure status: {:02x}".format(
                    #         result.status))
                    # log.info("aci_gap_terminate_gap_procedure %02x", result.status)

                elif hci_evt.subevtcode == EVT_LE_ADVERTISING_REPORT:
                    hci_evt.data = hci_evt.data[1:]

                    log.info("EVT_LE_ADVERTISING_REPORT %02x %s %d %s",
                             hci_evt.struct.evt_type,
                             hexlify(hci_evt.struct.bdaddr, ':'),
                             hci_evt.struct.data_length,
                             hexlify(hci_evt.struct.data_RSSI[:hci_evt.struct.data_length]))

                    if hci_evt.struct.evt_type == ADV_IND:
                        log.info("ADV_IND")
                    elif hci_evt.struct.evt_type == SCAN_RSP:
                        log.info("SCAN_RSP")
                    elif hci_evt.struct.evt_type == ADV_DIRECT_IND:
                        log.info("ADV_DIRECT_IND")

            elif hci_evt.evtcode == EVT_VENDOR:
                if hci_evt.subevtcode == EVT_BLUE_GATT_ATTRIBUTE_MODIFIED:
                    log.debug("EVT_BLUE_GATT_ATTRIBUTE_MODIFIED")
                    self.attribute_modified_cb(
                        hci_evt.struct.attr_handle,
                        hci_evt.struct.data_length,
                        hci_evt.struct.att_data[:hci_evt.struct.data_length]
                    )
                elif hci_evt.subevtcode == EVT_BLUE_GATT_NOTIFICATION:
                    log.debug("EVT_BLUE_GATT_NOTIFICATION")
                    self.notification_cb(
                        hci_evt.struct.attr_handle,
                        hci_evt.struct.event_data_length - 2,
                        hci_evt.struct.attr_value)
                elif hci_evt.subevtcode == EVT_BLUE_L2CAP_CONN_UPD_RESP:
                    log.debug(
                        "EVT_BLUE_L2CAP_CONN_UPD_RESP: %02x",
                        hci_evt.struct.result)
                elif hci_evt.subevtcode == EVT_BLUE_GAP_PROCEDURE_COMPLETE:
                    log.debug(
                        "EVT_BLUE_GAP_PROCEDURE_COMPLETE: %02x",
                        hci_evt.struct.procedure_code)
                    if hci_evt.struct.procedure_code == GAP_GENERAL_DISCOVERY_PROC:
                        log.info("GAP_GENERAL_DISCOVERY_PROC")
                        self.start_discovery()
                elif hci_evt.subevtcode == EVT_BLUE_GATT_DISC_READ_CHAR_BY_UUID_RESP:
                    log.debug(
                        "EVT_BLUE_GATT_DISC_READ_CHAR_BY_UUID_RESP: %02x",
                        hci_evt.struct.attr_handle)
                elif hci_evt.subevtcode == EVT_BLUE_GATT_PROCEDURE_COMPLETE:
                    # Wait for gatt procedure complete event trigger related to
                    # Discovery Charac by UUID
                    log.debug("EVT_BLUE_GATT_PROCEDURE_COMPLETE")
                elif hci_evt.subevtcode == EVT_BLUE_GATT_TX_POOL_AVAILABLE:
                    # New event available on BlueNRG-MS FW stack 7.1.b to know
                    # when there is a buffer available on GATT pool
                    log.debug("EVT_BLUE_GATT_TX_POOL_AVAILABLE")

    def attribute_modified_cb(self, handle, data_length, att_data):
        log.info("attribute_modified_cb %04x %d %s",
                 handle, data_length, hexlify(att_data))

    def notification_cb(self, attr_handle, attr_len, attr_value):
        log.info("notification_cb %04x %d %s",
                 attr_handle, attr_len, hexlify(attr_value))

    def connection_complete_cb(self, bdaddr, handle):
        log.info("connection_complete_cb %s", hexlify(bdaddr, ':'))
        self.connection_handle = handle

    def disconnection_complete_cb(self):
        log.info("disconnection_complete_cb")
