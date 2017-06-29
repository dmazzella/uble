# -*- coding: utf-8 -*-
from binascii import hexlify
from bluetooth_low_energy.api.scanner import Scanner

def main(timeout=5000):

    scan = Scanner()
    scan_res = scan.scan(timeout)
    for _se in scan_res:
        print(
            "address: {0} address_type: {1} rssi: {2} data: {3}".format(
                hexlify(_se.address, ":"),
                _se.address_type,
                _se.rssi,
                _se.get_data()
            )
        )

if __name__ == "__main__":
    main()
