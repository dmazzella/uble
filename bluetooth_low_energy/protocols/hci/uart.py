# -*- coding: utf-8 -*-
import ustruct
from ubinascii import hexlify, unhexlify


from bluetooth_low_energy.protocols.hci import (
    HCI_COMMAND_PKT as COMMAND,
    HCI_ACLDATA_PKT as ACLDATA,
    HCI_SCODATA_PKT as SCODATA,
    HCI_EVENT_PKT as EVENT,
    HCI_VENDOR_PKT as VENDOR)
"""
HCI Packet types for UART Transport layer
Core specification 4.1 [vol 4] Part A (Section 2) - Protocol
"""
HCI_UART_PKT_TYPES = {
    COMMAND: "COMMAND",
    ACLDATA: "ACLDATA",
    SCODATA: "SCODATA",
    EVENT: "EVENT",
    VENDOR: "VENDOR"
}


class HCI_UART(object):
    """HCI_UART"""
    struct_format = "<B"
    struct_size = ustruct.calcsize(struct_format)

    def __init__(self, pkt_type, data=b''):
        self._pkt_type = pkt_type
        self._pkt_type_name = HCI_UART_PKT_TYPES[pkt_type]
        self._data = data

    def __getattr__(self, name):
        if name == "pkt_type":
            return self._pkt_type
        elif name == "pkt_type_name":
            return self._pkt_type_name
        elif name == "data":
            return self._data
        else:
            raise AttributeError(name)

    def __str__(self):
        return "<{:s} pkt_type={:s}(0x{:02x}) data={:s}>".format(
            self.__class__.__name__,
            self.pkt_type_name,
            self.pkt_type,
            hexlify(self.data)
        )

    @staticmethod
    def from_buffer(data):
        """
        Parse a hci information from the specified data string

        There are four kinds of HCI packets that can be sent via the UART Transport
        Layer; i.e. HCI Command Packet, HCI Event Packet, HCI ACL Data Packet
        and HCI Synchronous Data Packet (see Host Controller Interface Functional
        Specification in Volume 2, Part E). HCI Command Packets can only be sent to
        the Bluetooth Host Controller, HCI Event Packets can only be sent from the
        Bluetooth Host Controller, and HCI ACL/Synchronous Data Packets can be
        sent both to and from the Bluetooth Host Controller.

        References can be found here:
        * https://www.bluetooth.org/en-us/specification/adopted-specifications
        ** Core specification 4.1
        ** [vol 4] Part A (Section 2) Protocol
        """
        pkt_type = ustruct.unpack(
            HCI_UART.struct_format, data[:HCI_UART.struct_size]
        )[0]
        return HCI_UART(pkt_type, data[HCI_UART.struct_size:])

    def to_buffer(self):
        """
        Get data string
        """
        return ustruct.pack(HCI_UART.struct_format, self.pkt_type) + self.data
