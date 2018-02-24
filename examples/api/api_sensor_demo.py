# -*- coding: utf-8 -*-
import ustruct
import urandom
import machine
from binascii import hexlify, unhexlify

from bluetooth_low_energy.api.characteristic import Characteristic
from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.descriptor import Descriptor
from bluetooth_low_energy.api.peripheral import Peripheral
from bluetooth_low_energy.api.service import Service
from bluetooth_low_energy.api.uuid import UUID


def main():
    """ Test Sensor Demo """

    acc_service_uuid = UUID('02366e80cf3a11e19ab40002a5d5c51b')
    free_fall_char_uuid = UUID('e23e78a0cf4a11e18ffc0002a5d5c51b')
    acc_char_uuid = UUID('340a1b80cf4b11e1ac360002a5d5c51b')

    env_service_uuid = UUID('42821a40e47711e282d00002a5d5c51b')
    temp_char_uuid = UUID('a32e5520e47711e2a9e30002a5d5c51b')
    press_char_uuid = UUID('cd20c480e48b11e2840b0002a5d5c51b')
    humidity_char_uuid = UUID('01c50b60e48c11e2a0730002a5d5c51b')

    def write_characteristics():
        """ write_characteristics """
        # Accelerator
        env_sens_peripheral.write_uuid(
            acc_char_uuid,
            ustruct.pack(
                "<HHH",
                (urandom.randint(-1000, 1000)),
                (urandom.randint(-1000, 1000)),
                (urandom.randint(-1000, 1000)))
        )
        # Free Fall
        env_sens_peripheral.write_uuid(
            env_service_uuid,
            ustruct.pack("<B", urandom.randint(0, 1))
        )
        # Temperature
        env_sens_peripheral.write_uuid(
            temp_char_uuid,
            ustruct.pack("<H", int(urandom.randint(-50, 50)  * 10))
        )
        # Pressure
        env_sens_peripheral.write_uuid(
            press_char_uuid,
            ustruct.pack("<H", (100000 + urandom.randint(0, 1000)//32767))
        )
        # Humidity
        env_sens_peripheral.write_uuid(
            humidity_char_uuid,
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
            return True
        elif event == EVT_GATTS_WRITE_PERMIT_REQ:
            print("EVT_GATTS_WRITE_PERMIT_REQ")
            return True

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
        temp_char_uuid,
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
        press_char_uuid,
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
        humidity_char_uuid,
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
        env_service_uuid,
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
        free_fall_char_uuid,
        char_value_len=1,
        props=PROP_NOTIFY | PROP_READ,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    accel_characteristic = Characteristic(
        acc_char_uuid,
        char_value_len=6,
        props=PROP_NOTIFY | PROP_READ,
        perms=PERM_NONE,
        mask=MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
    )

    # Accelerator Sensing service
    accel_sens_service = Service(
        acc_service_uuid,
        service_type=SERVICE_PRIMARY,
        characteristics=[
            free_fall_characteristic,
            accel_characteristic
        ]
    )

    ################## Accelerator Sensing #################
    
    # uBLE Breakout v0.1 use: Power-on on X8 
    #vin_pin=machine.Pin('X8', machine.Pin.OUT_PP, value=0)

    env_sens_peripheral = Peripheral(
        "0280E1003414",
        name="BlueNRG",
        connectable=True,
        services=[
            accel_sens_service,
            env_sens_service
        ],
        # uBLE Breakout v0.1 use: nss on Y5, rst on X9
        # nss_pin=machine.Pin('Y5', machine.Pin.OUT_PP),
        # rst_pin=machine.Pin('X9', machine.Pin.OUT_PP)
    )
    env_sens_peripheral.set_event_handler(event_handler_callback)
    env_sens_peripheral.run(callback=notify_callback, callback_time=5000)

if __name__ == "__main__":
    main()
