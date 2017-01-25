# -*- coding: utf-8 -*-
import pyb

from bluetooth_low_energy.modules.st_microelectronics.bluenrg_ms import (
    BlueNRG_MS)

class SPBTLE_RF(BlueNRG_MS):
    """
    SPBTLE-RF:
        Very low power module for Bluetooth Smart v4.1
    """
    def __init__(self, *args, **kwargs):
        super(SPBTLE_RF, self).__init__(*args, **kwargs)
        self.reset()

    def __start__(self):
        super(SPBTLE_RF, self).__start__()

    def __stop__(self):
        super(SPBTLE_RF, self).__stop__()

    def __process__(self, event):
        super(SPBTLE_RF, self).__process__(event)
