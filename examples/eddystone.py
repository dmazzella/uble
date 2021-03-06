# -*- coding: utf-8 -*-
import gc
gc.threshold(4096)

import stm
import utime
from micropython import const
from binascii import hexlify, unhexlify
import logging

from bluetooth_low_energy.modules.st_microelectronics.spbtle_rf import SPBTLE_RF
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms import event as st_event
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms import constant as st_constant
from bluetooth_low_energy.protocols.hci import HCI_EVENT_PKT
from bluetooth_low_energy.protocols.hci import uart
from bluetooth_low_energy.protocols.hci import event
from bluetooth_low_energy.protocols.hci import status

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("examples.eddystone")

def adcread(chan): # 16 temp 17 vbat 18 vref
    assert chan >= 16 and chan <= 18, 'Invalid ADC channel'
    start = utime.ticks_ms()
    timeout = 100
    stm.mem32[stm.RCC + stm.RCC_APB2ENR] |= 0x100 # enable ADC1 clock.0x4100
    stm.mem32[stm.ADC1 + stm.ADC_CR2] = 1 # Turn on ADC
    stm.mem32[stm.ADC1 + stm.ADC_CR1] = 0 # 12 bit
    if chan == 17:
        stm.mem32[stm.ADC1 + stm.ADC_SMPR1] = 0x200000 # 15 cycles
        stm.mem32[stm.ADC + 4] = 1 << 23
    elif chan == 18:
        stm.mem32[stm.ADC1 + stm.ADC_SMPR1] = 0x1000000
        stm.mem32[stm.ADC + 4] = 0xc00000
    else:
        stm.mem32[stm.ADC1 + stm.ADC_SMPR1] = 0x40000
        stm.mem32[stm.ADC + 4] = 1 << 23
    stm.mem32[stm.ADC1 + stm.ADC_SQR3] = chan
    stm.mem32[stm.ADC1 + stm.ADC_CR2] = 1 | (1 << 30) | (1 << 10) # start conversion
    while not stm.mem32[stm.ADC1 + stm.ADC_SR] & 2: # wait for EOC
        if utime.ticks_diff(utime.ticks_ms(), start) > timeout:
            raise OSError('ADC timout')
    data = stm.mem32[stm.ADC1 + stm.ADC_DR] # clear down EOC
    stm.mem32[stm.ADC1 + stm.ADC_CR2] = 0 # Turn off ADC
    return data

def v33():
    return 4096 * 1.21 / adcread(17)

def vbat():
    return 1.21 * 2 * adcread(18) / adcread(17)  #2:1 divider on Vbat channel

def vref():
    return 3.3 * adcread(17) / 4096

def temperature():
    return 25 + 400 * (3.3 * adcread(16) / 4096 - 0.76)

HTTP_WWW = const(0x00)
HTTPS_WWW = const(0x01)
HTTP = const(0x02)
HTTPS = const(0x03)
DOT_COM_SLASH = const(0x00)
DOT_ORG_SLASH = const(0x01)
DOT_EDU_SLASH = const(0x02)
DOT_NET_SLASH = const(0x03)
DOT_INFO_SLASH = const(0x04)
DOT_BIZ_SLASH = const(0x05)
DOT_GOV_SLASH = const(0x06)
DOT_COM = const(0x07)
DOT_ORG = const(0x08)
DOT_EDU = const(0x09)
DOT_NET = const(0x0A)
DOT_INFO = const(0x0B)
DOT_BIZ = const(0x0C)
DOT_GOV = const(0x0D)

SCAN_P = const(0x4000)
SCAN_L = const(0x4000)
# Supervision timeout, arg in msec.
SUPERV_TIMEOUT = const(600)
# Connection period, arg in msec.
CONN_P = lambda x: int(x / 1.25)
# Connection length, arg in msec.
CONN_L = lambda x: int(x / 0.625)

CONN_P1 = CONN_P(1000)
CONN_P2 = CONN_P(1000)
CONN_L1 = CONN_L(5)
CONN_L2 = CONN_L(5)

EDDYSTONE_UID_BEACON_TYPE = const(0x01)
EDDYSTONE_URL_BEACON_TYPE = const(0x02)
EDDYSTONE_TLM_BEACON_TYPE = const(0x03)

EDDYSTONE_BEACON_TYPE = EDDYSTONE_TLM_BEACON_TYPE

ADVERTISING_INTERVAL_IN_MS = const(1000)
CALIBRATED_TX_POWER_AT_0_M = const(0xE2)
NAMESPACE_ID = b'www.st.com'
BEACON_ID = bytes([0, 0, 0, 0, 0, 1])
URL_PREFIX = HTTPS
PHYSICAL_WEB_URL = b"goo.gl/rXrrL4"

ADVERTISING_INTERVAL_INCREMENT = const(16)


class Eddystone(SPBTLE_RF):
    """
    This example application shows how to use the BlueNRG Bluetooth Low Energy (BLE)
    expansion board to implement an Eddystone Beacon device.

    An Eddystone Beacon is a smart Bluetooth Low Energy device that transmits
    a small data payload at regular intervals using Bluetooth advertising packets.

    Beacons are used to mark important places and objects. Typically, a beacon
    is visible to a user's device from a range of a few meters, allowing for highly
    context-sensitive use cases.

    Eddystone is an open beacon format from Google that works with Android and iOS.
    Specifications can be found at https://developers.google.com/beacons/

    - UID: a UID beacon broadcasts a unique ID that provides proximity and general
           location information.
    - URL: a URL beacon broadcasts a packet containing an URL code usable by compatible
           applications.
    - TLM: a TLM beacon broadcasts telemetry information about the beacon itself such
           as battery voltage, device temperature, and counts of broadcast packets.

    To locate the beacon, it is necessary to have a scanner application running
    on a BLE-capable smartphone, such as one of the following ones for Android:
    - Physical Web:
          https://play.google.com/store/apps/details?id=physical_web.org.physicalweb
    - iBeacon & Eddystone Scanner:
          https://play.google.com/store/apps/details?id=de.flurp.beaconscanner.app
    - Beacon Radar:
          https://play.google.com/store/apps/details?id=net.beaconradar
    An alternative is to use a 'Physical Web' compatible browser like Google Chrome (version >=44)
    """

    def __init__(self, *args, beacon_type=None, **kwargs):
        super(Eddystone, self).__init__(*args, **kwargs)
        self.bdaddr = bytes(reversed([0x12, 0x34, 0x00, 0xE1, 0x80, 0x03]))
        self.name = b'PyEddystone'
        self.connection_handle = None
        self.service_handle = None
        self.dev_name_char_handle = None
        self.appearance_char_handle = None
        self.adv_count = 0
        if beacon_type is not None:
            global EDDYSTONE_BEACON_TYPE
            if beacon_type == 1:
                EDDYSTONE_BEACON_TYPE = EDDYSTONE_UID_BEACON_TYPE
            elif beacon_type == 2:
                EDDYSTONE_BEACON_TYPE = EDDYSTONE_URL_BEACON_TYPE
            elif beacon_type == 3:
                EDDYSTONE_BEACON_TYPE = EDDYSTONE_TLM_BEACON_TYPE
            else:
                raise ValueError(
                    "beacon type ({:d}) not supported. Must be in range 1-3".format(
                        beacon_type
                    )
                )

    def run(self, *args, **kwargs):
        """ run """
        def callback():
            """ callback """
            log.debug("memory free %d", gc.mem_free())

        super(Eddystone, self).run(callback=callback, callback_time=1000)

    def __start__(self):
        """ __start__ """
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
        # aci_hal_write_config_data() must be the first command after reset
        # otherwise it will fail.
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
        log.info("Public address: %s", hexlify(self.bdaddr, ":"))

        # Init BlueNRG GATT layer
        result = self.aci_gatt_init().response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_init status: {:02x}".format(
                result.status))
        log.debug("aci_gatt_init %02x", result.status)

        # Init BlueNRG GAP layer as peripheral
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

        # Set output power level
        result = self.aci_hal_set_tx_power_level(
            en_high_power=1,
            pa_level=4).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_set_tx_power_level status: {:02x}".format(
                result.status))
        log.debug("aci_hal_set_tx_power_level %02x", result.status)

        # Initialize beacon services
        if EDDYSTONE_BEACON_TYPE == EDDYSTONE_UID_BEACON_TYPE:
            self.eddystone_uid_start()
        elif EDDYSTONE_BEACON_TYPE == EDDYSTONE_URL_BEACON_TYPE:
            self.eddystone_url_start()
        elif EDDYSTONE_BEACON_TYPE == EDDYSTONE_TLM_BEACON_TYPE:
            self.eddystone_tlm_start()

    def __stop__(self):
        """ __stop__ """
        # Reset BlueNRG-MS
        self.reset()

    def __process__(self, evt):
        """ Process event received from BlueNRG-MS """
        hci_uart = uart.HCI_UART.from_buffer(evt)
        log.debug("%s", hci_uart)
        if hci_uart.pkt_type == HCI_EVENT_PKT:
            hci_evt = event.HCI_EVENT.from_buffer(hci_uart.data)
            log.debug("%s", hci_evt)
            if hci_evt.evtcode == event.EVT_DISCONN_COMPLETE:
                self.disconnection_complete_cb()
            elif hci_evt.evtcode == event.EVT_LE_META_EVENT:
                if hci_evt.subevtcode == event.EVT_LE_CONN_COMPLETE:
                    self.connection_complete_cb(
                        hci_evt.struct.peer_bdaddr, hci_evt.struct.handle)
            elif hci_evt.evtcode == event.EVT_VENDOR:
                pass

    def connection_complete_cb(self, bdaddr, handle):
        """ connection_complete_cb """
        log.info("connection_complete_cb %s", hexlify(bdaddr, ':'))
        self.connection_handle = handle

    def disconnection_complete_cb(self):
        """ disconnection_complete_cb """
        log.info("disconnection_complete_cb")
        # Initialize beacon services
        if EDDYSTONE_BEACON_TYPE == EDDYSTONE_UID_BEACON_TYPE:
            self.eddystone_uid_start()
        elif EDDYSTONE_BEACON_TYPE == EDDYSTONE_URL_BEACON_TYPE:
            self.eddystone_url_start()
        elif EDDYSTONE_BEACON_TYPE == EDDYSTONE_TLM_BEACON_TYPE:
            self.eddystone_tlm_start()

    def eddystone_start(self, eddystone_type, adv):
        """ This function initializes the Eddystone 'type' Bluetooth services """

        # disable scan response
        result = self.hci_le_set_scan_resp_data(
            length=st_constant.MAX_ADV_DATA_LEN,
            data=b'\x00' * st_constant.MAX_ADV_DATA_LEN).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("hci_le_set_scan_resp_data status: {:02x}".format(
                result.status))
        log.debug("hci_le_set_scan_resp_data %02x", result.status)

        advertising_interval = \
            int(eddystone_type["advertising_interval"]
                * ADVERTISING_INTERVAL_INCREMENT / 10)

        # General Discoverable Mode
        result = self.aci_gap_set_discoverable(
            adv_type=st_constant.ADV_SCAN_IND,
            adv_interv_min=advertising_interval,
            adv_interv_max=advertising_interval,
            own_addr_type=st_constant.PUBLIC_ADDR,
            adv_filter_policy=st_constant.NO_WHITE_LIST_USE,
            local_name_len=0,
            local_name=b'',
            service_uuid_len=0,
            service_uuid_list=b'',
            slave_conn_interv_min=0,
            slave_conn_interv_max=0).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_set_discoverable status: {:02x}".format(
                result.status))
        log.debug("aci_gap_set_discoverable %02x", result.status)

        # Remove the TX power level advertisemen
        # (this is done to decrease the packet size).
        result = self.aci_gap_delete_ad_type(
            ad_type=st_constant.AD_TYPE_TX_POWER_LEVEL
        ).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_delete_ad_type status: {:02x}".format(
                result.status))
        log.debug("aci_gap_delete_ad_type %02x", result.status)

        # Set the advertisement data
        adv_bytes = bytes(adv)
        log.info("adv_data: %d %r", len(adv_bytes), hexlify(adv_bytes))
        result = self.aci_gap_update_adv_data(
            adv_len=len(adv_bytes),
            adv_data=adv_bytes).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_update_adv_data status: {:02x}".format(
                result.status))
        log.debug("aci_gap_update_adv_data %02x", result.status)

        self.adv_count += 1

    def eddystone_uid_start(self):
        """ This function initializes the Eddystone UID Bluetooth services """
        log.info("Eddystone UID")
        eddystone_uid = {
            "advertising_interval": ADVERTISING_INTERVAL_IN_MS,
            "calibrated_tx_power": CALIBRATED_TX_POWER_AT_0_M,
            "namespace_id": NAMESPACE_ID,
            "beacon_id": BEACON_ID,
        }

        adv = [
            # Length
            2,
            # Flags data type value.
            st_constant.AD_TYPE_FLAGS,
            # BLE general discoverable, without BR/EDR support.
            (st_constant.FLAG_BIT_LE_GENERAL_DISCOVERABLE_MODE |
             st_constant.FLAG_BIT_BR_EDR_NOT_SUPPORTED),
            # Length.
            3,
            # Complete list of 16-bit Service UUIDs data type value.
            st_constant.AD_TYPE_16_BIT_SERV_UUID_CMPLT_LIST,
            # 16-bit Eddystone UUID.
            0xAA, 0xFE,
            # Length.
            23,
            # Service Data data type value.
            st_constant.AD_TYPE_SERVICE_DATA,
            # 16-bit Eddystone UUID.
            0xAA, 0xFE,
            # UID frame type.
            0x00,
            # Ranging data.
            eddystone_uid["calibrated_tx_power"],
        ] + [
            # 10-byte ID Namespace.
            x for x in eddystone_uid["namespace_id"]
        ] + [
            # 6-byte ID Instance.
            x for x in eddystone_uid["beacon_id"]
        ] + [
            # Reserved.
            0x00,
            # Reserved.
            0x00
        ]

        self.eddystone_start(eddystone_uid, adv)

    def eddystone_url_start(self):
        """ This function inizializes the Eddystone URL Bluetooth services """
        log.info("Eddystone URL")
        eddystone_url = {
            "advertising_interval": ADVERTISING_INTERVAL_IN_MS,
            "calibrated_tx_power": CALIBRATED_TX_POWER_AT_0_M,
            "url_scheme": URL_PREFIX,
            "url": PHYSICAL_WEB_URL,
        }

        adv = [
            # Length
            2,
            # Flags data type value.
            st_constant.AD_TYPE_FLAGS,
            # BLE general discoverable, without BR/EDR support.
            (st_constant.FLAG_BIT_LE_GENERAL_DISCOVERABLE_MODE |
             st_constant.FLAG_BIT_BR_EDR_NOT_SUPPORTED),
            # Length.
            3,
            # Complete list of 16-bit Service UUIDs data type value.
            st_constant.AD_TYPE_16_BIT_SERV_UUID_CMPLT_LIST,
            # 16-bit Eddystone UUID.
            0xAA, 0xFE,
            # Length.
            6 + len(eddystone_url["url"]),
            # Service Data data type value.
            st_constant.AD_TYPE_SERVICE_DATA,
            # 16-bit Eddystone UUID.
            0xAA, 0xFE,
            # URL frame type.
            0x10,
            # Ranging data.
            eddystone_url["calibrated_tx_power"],
            # URL Scheme Prefix is http://www.
            eddystone_url["url_scheme"],
        ] + [
            # Url
            x for x in eddystone_url["url"]
        ]

        self.eddystone_start(eddystone_url, adv)

    def eddystone_tlm_start(self):
        """ This function inizializes the Eddystone TLM Bluetooth services """
        log.info("Eddystone TLM")
        eddystone_tlm = {
            "advertising_interval": ADVERTISING_INTERVAL_IN_MS,
            "calibrated_tx_power": CALIBRATED_TX_POWER_AT_0_M,
            "vbatt": (int(1000 * (v33() * (3.6 / 1023.0)))).to_bytes(2, 'little'),
            "temp": (int(256.0 * temperature())).to_bytes(2, 'little'),
            "adv_cnt": (self.adv_count).to_bytes(4, 'little'),
            "sec_cnt": (utime.ticks_ms()//1000).to_bytes(4, 'little')
        }

        adv = [
            # Length
            2,
            # Flags data type value.
            st_constant.AD_TYPE_FLAGS,
            # BLE general discoverable, without BR/EDR support.
            (st_constant.FLAG_BIT_LE_GENERAL_DISCOVERABLE_MODE |
             st_constant.FLAG_BIT_BR_EDR_NOT_SUPPORTED),
            # Length.
            3,
            # Complete list of 16-bit Service UUIDs data type value.
            st_constant.AD_TYPE_16_BIT_SERV_UUID_CMPLT_LIST,
            # 16-bit Eddystone UUID.
            0xAA, 0xFE,
            # Length.
            17,
            # Service Data data type value.
            st_constant.AD_TYPE_SERVICE_DATA,
            # 16-bit Eddystone UUID.
            0xAA, 0xFE,
            # TLM frame type.
            0x20,
            # Version.
            0x00
        ] + [
            # 2-byte vbatt.
            x for x in eddystone_tlm["vbatt"]
        ] + [
            # 2-byte temp.
            x for x in eddystone_tlm["temp"]
        ] + [
            # 4-byte adv_cnt.
            x for x in eddystone_tlm["adv_cnt"]
        ] + [
            # 4-byte sec_cnt.
            x for x in eddystone_tlm["sec_cnt"]
        ]

        self.eddystone_start(eddystone_tlm, adv)
