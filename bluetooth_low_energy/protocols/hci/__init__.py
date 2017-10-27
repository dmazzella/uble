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

HCI_EVENT_HDR_SIZE = const(2)


# HCI Packet types
HCI_COMMAND_PKT = const(0x01)
HCI_ACLDATA_PKT = const(0x02)
HCI_SCODATA_PKT = const(0x03)
HCI_EVENT_PKT = const(0x04)
HCI_VENDOR_PKT = const(0xff)
