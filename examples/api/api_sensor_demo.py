# -*- coding: utf-8 -*-
import ustruct
import urandom
from binascii import hexlify, unhexlify

from bluetooth_low_energy.api.characteristic import Characteristic
from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.descriptor import Descriptor
from bluetooth_low_energy.api.peripheral import Peripheral
from bluetooth_low_energy.api.service import Service
from bluetooth_low_energy.api.uuid import UUID


def main():
    """ Test Temperature device """

    def write_characteristics():
        """ write_characteristics """
        # Accelerator
        env_sens_peripheral.write_uuid(
            UUID("1bc5d5a5-0200-36ac-e1114bcf801b0a34"),
            ustruct.pack(
                "<HHH",
                (urandom.randint(-1000, 1000)),
                (urandom.randint(-1000, 1000)),
                (urandom.randint(-1000, 1000)))
        )
        # Free Fall
        env_sens_peripheral.write_uuid(
            UUID("1bc5d5a5-0200-fc8f-e1114acfa0783ee2"),
            ustruct.pack("<B", urandom.randint(0, 1))
        )
        # Temperature
        env_sens_peripheral.write_uuid(
            UUID("1bc5d5a5-0200-e3a9-e21177e420552ea3"),
            ustruct.pack("<H", int(urandom.randint(-50, 50)  * 10))
        )
        # Pressure
        env_sens_peripheral.write_uuid(
            UUID("1bc5d5a5-0200-0b84-e2118be480c420cd"),
            ustruct.pack("<H", (100000 + urandom.randint(0, 1000)//32767))
        )
        # Humidity
        env_sens_peripheral.write_uuid(
            UUID("1bc5d5a5-0200-73a0-e2118ce4600bc501"),
            ustruct.pack("<H", (450 + urandom.randint(0, 100)//32767))
        )

    notify_enabled = False
    def event_handler_callback(event, handler=None, data=None):
        """ event callback """
        if event == EVT_GAP_CONNECTED:
            print("EVT_GAP_CONNECTED {:s}".format(hexlify(data, ':')))
        elif event == EVT_GAP_DISCONNECTED:
            print("EVT_GAP_DISCONNECTED")
            env_sens_peripheral.set_discoverable()
        elif event == EVT_GATTS_WRITE:
            print("EVT_GATTS_WRITE")
            nonlocal notify_enabled
            notify_enabled = (int(data[0]) == 1)
            print("notify_enabled", notify_enabled)
            uuid = env_sens_peripheral.uuid_from_handle(handler-1)
            if uuid is not None:
                print("{!s}".format(uuid))
        elif event == EVT_GATTS_READ_PERMIT_REQ:
            print("EVT_GATTS_READ_PERMIT_REQ")
            uuid = env_sens_peripheral.uuid_from_handle(handler-1)
            if uuid is not None:
                print("{!s}".format(uuid))
            #write_characteristics()
        elif event == EVT_GATTS_WRITE_PERMIT_REQ:
            print("EVT_GATTS_WRITE_PERMIT_REQ")

    def notify_callback():
        """ notify_callback """
        if notify_enabled:
            write_characteristics()

    ################ Environmental Sensing ################

    # Temperature characteristic descriptor
    temp_characteristic_descriptor = Descriptor(
        UUID("2904"),
        ustruct.pack("<BBHBH", 0x0e, -1, 0x272f, 0, 0),
        perms=PERM_NONE,
        acc=ACC_READ_ONLY,
        mask=MASK_DONT_NOTIFY_EVENTS
    )

    # Temperature characteristic
    temp_characteristic = Characteristic(
        UUID('1bc5d5a5-0200-e3a9-e21177e420552ea3'),
        char_value_len=2,
        props=PROP_NOTIFY | PROP_READ,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
        descriptors=[
            temp_characteristic_descriptor
        ]
    )

    # Pressure characteristic descriptor
    press_characteristic_descriptor = Descriptor(
        UUID("2904"),
        ustruct.pack("<BBHBH", 0x0f, -5, 0x2780, 0, 0),
        perms=PERM_NONE,
        acc=ACC_READ_ONLY,
        mask=MASK_DONT_NOTIFY_EVENTS
    )

    # Pressure characteristic
    press_characteristic = Characteristic(
        UUID('1bc5d5a5-0200-0b84-e2118be480c420cd'),
        char_value_len=2,
        props=PROP_NOTIFY | PROP_READ,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
        descriptors=[
            press_characteristic_descriptor
        ]
    )

    # Humidity characteristic descriptor
    humidity_characteristic_descriptor = Descriptor(
        UUID("2904"),
        ustruct.pack("<BBHBH", 0x06, -1, 0x2700, 0, 0),
        perms=PERM_NONE,
        acc=ACC_READ_ONLY,
        mask=MASK_DONT_NOTIFY_EVENTS
    )

    # Humidity characteristic
    humidity_characteristic = Characteristic(
        UUID('1bc5d5a5-0200-73a0-e2118ce4600bc501'),
        char_value_len=2,
        props=PROP_NOTIFY | PROP_READ,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP,
        descriptors=[
            humidity_characteristic_descriptor
        ]
    )

    # Environmental Sensing service
    env_sens_service = Service(
        UUID('1bc5d5a5-0200-d082-e21177e4401a8242'),
        service_type=SERVICE_PRIMARY,
        characteristics=[
            temp_characteristic,
            press_characteristic,
            humidity_characteristic
        ]
    )

    ################# Environmental Sensing #################

    ################## Accelerator Sensing ##################

    # Free fall characteristic
    free_fall_characteristic = Characteristic(
        UUID('1bc5d5a5-0200-fc8f-e1114acfa0783ee2'),
        char_value_len=1,
        props=PROP_NOTIFY | PROP_READ,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    accel_characteristic = Characteristic(
        UUID('1bc5d5a5-0200-36ac-e1114bcf801b0a34'),
        char_value_len=6,
        props=PROP_NOTIFY | PROP_READ,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    # Accelerator Sensing service
    accel_sens_service = Service(
        UUID('1bc5d5a5-0200-b49a-e1113acf806e3602'),
        service_type=SERVICE_PRIMARY,
        characteristics=[
            free_fall_characteristic,
            accel_characteristic
        ]
    )

    ################## Accelerator Sensing #################

    env_sens_peripheral = Peripheral(
        "0280E1003414",
        name="BlueNRG",
        connectable=True,
        services=[
            accel_sens_service,
            env_sens_service
        ]
    )
    env_sens_peripheral.set_event_handler(event_handler_callback)
    env_sens_peripheral.run(callback=notify_callback, callback_time=5000)

if __name__ == "__main__":
    main()
