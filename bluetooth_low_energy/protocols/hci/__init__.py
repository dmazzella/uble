# -*- coding: utf-8 -*-
import ustruct
import uctypes
from micropython import const

"""
Maximum payload of HCI commands that can be sent. Change this value if needed.
This value can be up to 255.
"""
HCI_MAX_PAYLOAD_SIZE = const(128)


HCI_READ_PACKET_SIZE = const(128)

# HCI Packet types
HCI_COMMAND_PKT = const(0x01)
HCI_ACLDATA_PKT = const(0x02)
HCI_SCODATA_PKT = const(0x03)
HCI_EVENT_PKT = const(0x04)
HCI_VENDOR_PKT = const(0xff)

HCI_UART_STRUCT = {
    "type": uctypes.UINT8 | 0,
    "data": (uctypes.ARRAY | 1, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 1)
}
HCI_UART_HDR_SIZE = 1

HCI_COMMAND_HDR_STRUCT = {
    "opcode": uctypes.UINT16 | 0,
    "length": uctypes.UINT8 | 1,
}
HCI_COMMAND_HDR_SIZE = 3

HCI_EVENT_STRUCT = {
    "event": uctypes.UINT8 | 0,
    "length": uctypes.UINT8 | 1,
    "data": (uctypes.ARRAY | 2, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 2)
}
HCI_EVENT_HDR_SIZE = 2

HCI_ACL_HDR_STRUCT = {
    "handle": uctypes.UINT16 | 0,
    "length": uctypes.UINT16 | 1
}
HCI_ACL_HDR_SIZE = 4

HCI_SCO_HDR_STRUCT = {
    "handle": uctypes.UINT16 | 0,
    "length": uctypes.UINT8 | 1
}
HCI_SCO_HDR_SIZE = 3

# from bluetooth_low_energy.protocols.hci.cmd import HCI_COMMAND, OPCODE
# # HCI_COMMAND decorator
# def WITH_HCI_COMMAND(ogf=0, ocf=0, **kwargs):
#     def wrap_hci_function(hci_function):
#         def wrapped_hci_function(module, *args):
#             hci_cmd = HCI_COMMAND(OPCODE.pack(ogf, ocf),
#                                   data=(hci_function(module, *args) or b''),
#                                   **kwargs)
#             module.hci_send_cmd(hci_cmd)
#             return hci_cmd
#         return wrapped_hci_function
#     return wrap_hci_function
