# -*- coding: utf-8 -*-
import gc
import pyb
from ubinascii import hexlify, unhexlify
from micropython import const

gc.threshold(4096)

import os
import logging

from bluetooth_low_energy.modules.st_microelectronics.spbtle_rf import SPBTLE_RF
from bluetooth_low_energy.protocols.hci.status import BLE_STATUS_SUCCESS
from bluetooth_low_energy.protocols.hci.uart import HCI_UART, EVENT, VENDOR
from bluetooth_low_energy.protocols.hci.event import HCI_EVENT

from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.event import (
    EVT_BLUE_HAL_INITIALIZED)
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.constant import (
    RESET_NORMAL,
    RESET_UPDATER_BAD_FLAG,
    RESET_UPDATER_PIN)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("examples.firmware_update")

# Firmware csv file created with "BlueNRG-MS_firmware_update_upy.py"
FW_FILENAME = "bluenrg_7_2_c_Mode_2-32MHz-XO32K_4M.csv"
FW_FILESIZE = os.stat(FW_FILENAME)[6]

BASE_ADDRESS = const(0x10010000)
DATA_SIZE = const(64)

class FirmwareUpdate(SPBTLE_RF):
    """
    Example for update BlueNRG-MS firmware
    """
    def __init__(self, *args, **kwargs):
        super(FirmwareUpdate, self).__init__(*args, **kwargs)

    def run(self, timeout=1000):
        # Reset BlueNRG-MS
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=EVT_BLUE_HAL_INITIALIZED
            ).struct.reason_code not in (RESET_NORMAL, RESET_UPDATER_BAD_FLAG):
            raise ValueError("reason_code")

        # Get the BlueNRG FW versions
        version = self.get_version()
        log.info("current version %s", version)

        # Enter bootloader mode
        self.hw_bootloader()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=EVT_BLUE_HAL_INITIALIZED
            ).struct.reason_code not in (RESET_UPDATER_BAD_FLAG, RESET_UPDATER_PIN):
            raise ValueError("reason_code")

        # Check updater version
        response = self.aci_get_updater_version().response_struct
        if response.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_get_updater_version status: {:02x}".format(
                response.status))
        elif response.version < 5:
            raise ValueError("aci_get_updater_version version: {:d}".format(
                response.version))

        # Erase blueflag
        if self.aci_erase_blue_flag().response_struct.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_erase_blue_flag status")

        address = BASE_ADDRESS
        with open(FW_FILENAME, 'rb') as fw_file:
            for index, line in enumerate(fw_file):
                line_numbers = (FW_FILESIZE // len(line))
                data = line.rstrip(b'\r\n')
                if index % 32 == 0:
                    # Erase sector
                    if self.aci_updater_erase_sector(
                            address=address
                        ).response_struct.status != BLE_STATUS_SUCCESS:
                        raise ValueError("aci_erase_blue_flag status")
                # Program sector
                if self.aci_updater_program_data_block(
                        address=address,
                        data_len=DATA_SIZE,
                        data=unhexlify(data)
                    ).response_struct.status != BLE_STATUS_SUCCESS:
                    raise ValueError("aci_updater_program_data_block status")

                log.info("%.2f %%", 100 * (index / line_numbers))
                address += DATA_SIZE

        # Reset Blue flag
        if self.aci_reset_blue_flag().response_struct.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_reset_blue_flag status")

        if self.aci_updater_reboot().response_struct.status != BLE_STATUS_SUCCESS:
            raise ValueError("aci_updater_reboot status")

        # Reset BlueNRG-MS
        self.reset()

        # Get the BlueNRG FW versions
        version = self.get_version()
        log.info("current version %s", version)

