# -*- coding: utf-8 -*-
# pylint: disable=C0111
from bluetooth_low_energy.api.util import format_advertisement


class ScanEntry(object):
    """ ScanEntry """

    def __init__(self, address, address_type, rssi, data):
        self.address = address
        self.address_type = address_type
        self.rssi = rssi
        self.data = data

    def get_data(self):
        """ return formatted advertisement data"""
        return format_advertisement(self.data)
