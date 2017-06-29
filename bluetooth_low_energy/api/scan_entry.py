# -*- coding: utf-8 -*-


class ScanEntry(object):
    """ ScanEntry """

    def __init__(self, address, address_type, rssi, data):
        self.address = address
        self.address_type = address_type
        self.rssi = rssi
        self.data = data
