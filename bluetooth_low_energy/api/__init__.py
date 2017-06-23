"""
Examples:
################################# Advertisment #################################

from bluetooth_low_energy.api import Peripheral
p = Peripheral()
p.advertise(device_name="MicroPython")

################################### DB setup ###################################

from bluetooth_low_energy.api import Service, Characteristic, UUID, Peripheral, constants
from pyb import LED

def event_handler(id, handle, data):
    print("BLE event:", id, "handle:", handle)
    print(data)
    if id == constants.EVT_GAP_CONNECTED:
        # connected
        LED(2).on()
    elif id == constants.EVT_GAP_DISCONNECTED:
        # disconnect
        LED(2).off()
    elif id == 80:
        print("id 80, data:", data)

s = Service(
    UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
)
s.add_characteristic(
    Characteristic(
        UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e"),
        props=Characteristic.PROP_WRITE | Characteristic.PROP_WRITE_WO_RESP
    )
)
s.add_characteristic(
    Characteristic(
        UUID("6e400003-b5a3-f393-e0a9-e50e24dcca9e"),
        props=Characteristic.PROP_NOTIFY,
        attrs=Characteristic.ATTR_CCCD
    )
)
p = Peripheral()
p.add_service(s)
p.set_connection_handler(event_handler)
p.advertise(device_name="micr", services=[s])
"""
