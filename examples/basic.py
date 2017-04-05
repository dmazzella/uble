# -*- coding: utf-8 -*-
import gc
gc.threshold(4096)

import logging

from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.event import (
    EVT_BLUE_HAL_INITIALIZED)
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.constant import (
    RESET_NORMAL)
from bluetooth_low_energy.modules.st_microelectronics.spbtle_rf import (
    SPBTLE_RF)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("examples.basic")

class Basic(SPBTLE_RF):
    """
    Simple example for print BlueNRG-MS firmware versione
    """
    def __init__(self, *args, **kwargs):
        super(Basic, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        # Reset BlueNRG-MS
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=EVT_BLUE_HAL_INITIALIZED
            ).struct.reason_code != RESET_NORMAL:
            raise ValueError("reason_code")

        # Get the BlueNRG FW versions
        version = self.get_version()
        log.info("current version %s", version)

