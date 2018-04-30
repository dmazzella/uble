# -*- coding: utf-8 -*-
# pylint: disable=C0111
import utime
import ustruct
from micropython import const
from binascii import hexlify, unhexlify

from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.scan_entry import ScanEntry
from bluetooth_low_energy.modules.st_microelectronics.spbtle_rf import \
    SPBTLE_RF
from bluetooth_low_energy.protocols.hci import (HCI_EVENT_PKT, event, status,
                                                uart)


class Scanner(SPBTLE_RF):
    """ Scanner """

    def __init__(self, *args, **kwargs):
        address = kwargs.pop('address', "0280E1003414")
        name = kwargs.pop('name', '')
        super(Scanner, self).__init__(*args, **kwargs)

        self.address = address if isinstance(
            address, bytes) else unhexlify(address)
        self.name = name
        self.response = []

    def __start__(self):
        # Reset BlueNRG-MS
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
            subevtcode=st_event.EVT_BLUE_HAL_INITIALIZED
        ).struct.reason_code != st_constant.RESET_NORMAL:
            raise ValueError("reason_code")

        # Configure BlueNRG-MS address as public (its public address is used)
        result = self.aci_hal_write_config_data(
            offset=st_constant.CONFIG_DATA_PUBADDR_OFFSET,
            length=st_constant.CONFIG_DATA_PUBADDR_LEN,
            data=self.address
        ).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError(
                "aci_hal_write_config_data status: {:02x}".format(
                    result.status
                )
            )

        # Configure BlueNRG Mode
        result = self.aci_hal_write_config_data(
            offset=st_constant.CONFIG_DATA_MODE_OFFSET,
            length=st_constant.CONFIG_DATA_MODE_LEN,
            data=b'\x02').response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_write_config_data status: {:02x}".format(
                result.status))

        # Init BlueNRG GATT layer
        result = self.aci_gatt_init().response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_init status: {:02x}".format(
                result.status))

        # Init BlueNRG GAP layer as central
        result = self.aci_gap_init_IDB05A1(
            role=st_constant.GAP_CENTRAL_ROLE_IDB05A1,
            privacy_enabled=bool(st_constant.PRIVACY_DISABLED),
            device_name_char_len=len(self.name)).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_init status: {:02x}".format(
                result.status))

        # Set output power level
        result = self.aci_hal_set_tx_power_level(
            en_high_power=1,
            pa_level=5).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_set_tx_power_level status: {:02x}".format(
                result.status))

        self.start()

    def __stop__(self):
        # Reset BlueNRG-MS
        self.reset()

    def __process__(self, evt):
        """ Process event received from BlueNRG-MS """
        hci_uart = uart.HCI_UART.from_buffer(evt)
        if hci_uart.pkt_type == HCI_EVENT_PKT:
            hci_evt = event.HCI_EVENT.from_buffer(hci_uart.data)
            if hci_evt.evtcode == event.EVT_LE_META_EVENT:
                if hci_evt.subevtcode == event.EVT_LE_ADVERTISING_REPORT:
                    hci_evt.data = hci_evt.data[1:]
                    if hci_evt.struct.evt_type in (
                        st_constant.ADV_IND, st_constant.ADV_SCAN_IND
                    ):
                        data = bytes(
                            hci_evt.struct.data_RSSI[
                                :hci_evt.struct.data_length]
                        ) if hci_evt.struct.data_length else b''
                        bdaddr = bytes(hci_evt.struct.bdaddr)
                        bdaddr_type = hci_evt.struct.bdaddr_type
                        rssi = data[-1] if hci_evt.struct.data_length else 0
                        self.response.append(
                            ScanEntry(bdaddr, bdaddr_type, rssi, data)
                        )
            elif hci_evt.evtcode == event.EVT_VENDOR:
                if hci_evt.subevtcode == st_event.EVT_BLUE_GAP_PROCEDURE_COMPLETE:
                    if hci_evt.struct.procedure_code == st_constant.GAP_GENERAL_DISCOVERY_PROC:
                        pass

    def start(self):
        """ start """
        result = self.aci_gap_start_general_discovery_proc(
            scan_interval=0x10,
            scan_window=0x10,
            own_address_type=st_constant.PUBLIC_ADDR,
            filter_duplicates=0x01).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError(
                "aci_gap_start_general_discovery_proc status: {:02x}".format(
                    result.status))

    def stop(self):
        """ stop """
        result = self.aci_gap_terminate_gap_procedure(
            procedure_code=0x02).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_terminate_gap_procedure status: {:02x}".format(
                result.status))

    def scan(self, timeout=100):
        """ scan """
        self.response.clear()
        try:
            def callback():
                """ periodic callback """
                self.stop()
                raise StopIteration()
            super(Scanner, self).run(callback=callback, callback_time=timeout)
        finally:
            return self.response
