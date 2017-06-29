# -*- coding: utf-8 -*-
import ustruct
from micropython import const
from binascii import hexlify, unhexlify
from bluetooth_low_energy.api.util import format_advertisement
from bluetooth_low_energy.api.scanner import Scanner
from bluetooth_low_energy.api.scan_entry import ScanEntry
from bluetooth_low_energy.api.constants import *

def main(timeout=5000):

    scan = Scanner()
    scan_res = scan.scan(timeout)
    for _se in scan_res:
        print(
            "address: {0} address_type: {1} rssi: {2} data: {3}".format(
                hexlify(_se.address, ":"),
                _se.address_type,
                _se.rssi,
                format_advertisement(_se.data)
            )
        )

if __name__ == "__main__":
    main()
