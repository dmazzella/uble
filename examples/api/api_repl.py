# -*- coding: utf-8 -*-
""" uBLE REPL """
import gc
gc.threshold(4096)
import os
import binascii
import ustruct
import utime
import _thread

import collections
import logging

from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.characteristic import Characteristic
from bluetooth_low_energy.api.descriptor import Descriptor
from bluetooth_low_energy.api.peripheral import Peripheral
from bluetooth_low_energy.api.service import Service
from bluetooth_low_energy.api.uuid import UUID

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("repl")


def main():
    """ main """

    buffer = collections.deque((), 80)

    class BleRepl(object):
        """ BleRepl """

        def write(self, data):
            """ write """
            def ble_write(d, i=0):
                """ ble_write """
                try:
                    for idx in range(0, len(d), 20):
                        repl_peripheral.write_uuid(
                            repl_tx_characteristic_uuid, d[idx:idx + 20])
                        i += idx
                        utime.sleep_us(250)
                except ValueError:
                    return ble_write(d, i)
                return i
            return ble_write(data)

        def readinto(self, data):
            """ readinto """
            nonlocal buffer
            while len(buffer) == 0:
                return None
            ustruct.pack_into("<B", data, 0, buffer.popleft())
            # char_ctrl_c = b"\x03"
            # if bytearray(char_ctrl_c) == data:
            #     raise KeyboardInterrupt()
            return 1

    repl_service_uuid = UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')
    repl_rx_characteristic_uuid = UUID('6e400002-b5a3-f393-e0a9-e50e24dcca9e')
    repl_tx_characteristic_uuid = UUID('6e400003-b5a3-f393-e0a9-e50e24dcca9e')

    def repl_event_handler(evt, handler=None, data=None):
        """ event callback """
        uuid = repl_peripheral.uuid_from_handle((handler or 0) - 1)
        if evt == EVT_GAP_CONNECTED:
            log.info("EVT_GAP_CONNECTED %s", binascii.hexlify(data, ':'))
            if hasattr(buffer, 'clear'):
                buffer.clear()
            os.dupterm(BleRepl())
        elif evt == EVT_GAP_DISCONNECTED:
            log.info("EVT_GAP_DISCONNECTED")
            os.dupterm(None)
            repl_peripheral.set_discoverable()
        elif evt == EVT_GATTS_WRITE:
            log.debug("EVT_GATTS_WRITE %s", binascii.hexlify(data))
        elif evt == EVT_GATTS_READ_PERMIT_REQ:
            log.debug("EVT_GATTS_READ_PERMIT_REQ %s", uuid)
            return True
        elif evt == EVT_GATTS_WRITE_PERMIT_REQ:
            log.debug("EVT_GATTS_WRITE_PERMIT_REQ %s %s",
                      uuid, binascii.hexlify(data))
            [buffer.append(d) for d in data]
            return True

    # REPL RX characteristic
    repl_rx_characteristic = Characteristic(
        repl_rx_characteristic_uuid,
        char_value_len=20,
        props=PROP_WRITE,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_WRITE_REQ_AND_WAIT_FOR_APPL_RESP
    )

    # REPL TX characteristic
    repl_tx_characteristic = Characteristic(
        repl_tx_characteristic_uuid,
        char_value_len=20,
        props=PROP_NOTIFY | PROP_READ,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    # REPL Service
    repl_service = Service(
        repl_service_uuid,
        service_type=SERVICE_PRIMARY,
        characteristics=[
            repl_rx_characteristic,
            repl_tx_characteristic
        ]
    )

    service_uuid_list = bytes([
        # Length
        2,
        # Flags data type value.
        st_constant.AD_TYPE_FLAGS,
        # BLE general discoverable, without BR/EDR support.
        st_constant.FLAG_BIT_LE_GENERAL_DISCOVERABLE_MODE |\
        st_constant.FLAG_BIT_BR_EDR_NOT_SUPPORTED,
        # Length.
        1 + len(repl_service_uuid.value),
        # Complete list of 128-bit Service UUIDs data type value.
        st_constant.AD_TYPE_128_BIT_SERV_UUID_CMPLT_LIST,
    ] + [
        # 128-bit REPL UUID.
        a for a in repl_service_uuid.value
    ])

    log.info(
        "Advertising data: %d %s",
        len(service_uuid_list), binascii.hexlify(service_uuid_list)
    )

    # uBLE v0.1: Power on
    # machine.Pin('X8', machine.Pin.OUT_PP, value=0)
    repl_peripheral = Peripheral(
        os.urandom(6),
        name="repl",
        connectable=True,
        data=service_uuid_list,
        services=[
            repl_service
        ],
        event_handler=repl_event_handler,
        # uBLE v0.1: nss, rst
        # nss_pin=machine.Pin('Y5', machine.Pin.OUT_PP),
        # rst_pin=machine.Pin('X9', machine.Pin.OUT_PP)
    )
    _thread.start_new_thread(repl_peripheral.run, tuple(), dict())


if __name__ == "__main__":
    main()
