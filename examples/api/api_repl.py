# -*- coding: utf-8 -*-
""" uBLE REPL """
import gc
gc.threshold((gc.mem_alloc() + gc.mem_free()) // 10)

import pyb
import os
import io
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
log = logging.getLogger("NUS")


def main():
    """ main """

    repl_service_uuid = UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')
    repl_rx_characteristic_uuid = UUID('6e400002-b5a3-f393-e0a9-e50e24dcca9e')
    repl_tx_characteristic_uuid = UUID('6e400003-b5a3-f393-e0a9-e50e24dcca9e')

    buffer_tx = collections.deque((), 2048)
    buffer_rx = collections.deque((), 4)

    class BleRepl(io.IOBase):
        """ BleRepl """

        def write(self, data):
            """ write """
            for d in data:
                buffer_tx.append(d)
            return len(data)

        def readinto(self, data):
            """ readinto """
            while len(buffer_rx) == 0:
                return None
            data[0] = buffer_rx.popleft()
            return 1

    def repl_transmit(*args, **kwargs):
        data = bytearray(20)
        data_mv = memoryview(data)
        blank = b'\x00' * 20
        while True:
            tx_len = len(buffer_tx)
            if tx_len:
                for i in range(min(20, tx_len)):
                    data_mv[i] = buffer_tx.popleft()
                repl_peripheral.write_uuid(
                    repl_tx_characteristic_uuid,
                    data_mv[:tx_len]
                )
                data_mv[:]= blank
            pyb.wfi()

    def repl_event_handler(evt, handler=None, data=None):
        """ event callback """
        uuid = repl_peripheral.uuid_from_handle((handler or 0) - 1)
        if evt == EVT_GAP_CONNECTED:
            log.info("EVT_GAP_CONNECTED %s", binascii.hexlify(data, ':'))
            if hasattr(buffer_rx, "clear"):
                buffer_rx.clear()
            if hasattr(buffer_tx, "clear"):
                buffer_tx.clear()
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
            for d in data:
                buffer_rx.append(d)
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
        name="NUS",
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
    _thread.start_new_thread(repl_peripheral.run, (), {})
    _thread.start_new_thread(repl_transmit, (), {})


if __name__ == "__main__":
    main()