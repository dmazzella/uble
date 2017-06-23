# -*- coding: utf-8 -*-
import ustruct
from micropython import const
from binascii import hexlify, unhexlify
from bluetooth_low_energy.api.peripheral import Peripheral
from bluetooth_low_energy.api.constants import *

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

INTERVAL_INCREMENT = const(16)
INTERVAL_IN_MS = const(1000)
CALIBRATED_TX_POWER_AT_0_M = const(0xE2)
PHYSICAL_WEB_URL = b'micropython'

def main():
    """ Eddystone device """

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
        6 + len(PHYSICAL_WEB_URL) + 1,
        # Service Data data type value.
        st_constant.AD_TYPE_SERVICE_DATA,
        # 16-bit Eddystone UUID.
        0xAA, 0xFE,
        # URL frame type.
        0x10,
        # Ranging data.
        CALIBRATED_TX_POWER_AT_0_M,
        # URL Scheme Prefix is https://www.
        HTTPS_WWW,
    ] + [
        # Url
        x for x in PHYSICAL_WEB_URL
    ] + [
        # URL Scheme Postfix is .org
        DOT_ORG
    ]

    adv_bytes = bytes(adv)
    print("adv_data: {:d} {:s}".format(len(adv_bytes), hexlify(adv_bytes)))

    eddystone_peripheral = Peripheral(
        "0280E1003412",
        connectable=False,
        interval=int(INTERVAL_IN_MS * INTERVAL_INCREMENT / 10),
        data=adv_bytes
    )
    eddystone_peripheral.run()

if __name__ == "__main__":
    main()
