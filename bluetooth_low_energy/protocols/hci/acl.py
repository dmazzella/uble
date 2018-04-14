# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0111
import ustruct
import uctypes
from ubinascii import hexlify, unhexlify
from micropython import const

"""
ACL handle is 12 bits, followed by 2 bits packet boundary flags and 2
bits broadcast flags.

 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
-----------------------------------------------------------------
|            handle     |pb |bc |             length            |
-----------------------------------------------------------------

References can be found here:
    * https://www.bluetooth.org/en-us/specification/adopted-specifications
    ** Core specification 4.1
    ** [vol 2] Part E (Section 5.4.2) - HCI ACL Data Packets
"""
HCI_ACL_STRUCT = {
    "handle": uctypes.BFUINT16 | 0 | 0 << uctypes.BF_POS | 12 << uctypes.BF_LEN,
    "pb": uctypes.BFUINT16 | 0 | 12 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
    "bc": uctypes.BFUINT16 | 0 | 14 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
    "length": uctypes.UINT16 | 2
}

"""
Packet Boundary flag

References can be found here:
    * https://www.bluetooth.org/en-us/specification/adopted-specifications
    ** Core specification 4.1
    ** [vol 2] Part E (Section 5.4.2) - HCI ACL Data Packets
"""
ACL_PB_START_NON_AUTO_L2CAP_PDU = const(0)
ACL_PB_CONT_FRAG_MSG = const(1)
ACL_PB_START_AUTO_L2CAP_PDU = const(2)
ACL_PB_COMPLETE_L2CAP_PDU = const(3)

PB_FLAGS = {
    ACL_PB_START_NON_AUTO_L2CAP_PDU: "START_NON_AUTO_L2CAP_PDU",
    ACL_PB_CONT_FRAG_MSG: "CONT_FRAG_MSG",
    ACL_PB_START_AUTO_L2CAP_PDU: "START_AUTO_L2CAP_PDU",
    ACL_PB_COMPLETE_L2CAP_PDU: "COMPLETE_L2CAP_PDU"
}


class HCI_ACL(object):
    """HCI_ACL"""
    struct_format = "<I"
    struct_size = ustruct.calcsize(struct_format)

    def __init__(self, handle, pb=0, bc=0, data=b''):
        bin_str = "{:016b}{:02b}{:02b}{:012b}".format(
            len(data) if data else 0, bc, pb, handle
        )
        self._handle = handle
        self._pb = pb
        self._pb_name = PB_FLAGS[pb]
        self._bc = bc
        self._tobytes = int(bin_str, 2)
        self._data = data

    def __getattr__(self, name):
        if name == "handle":
            return self._handle
        elif name == "pb":
            return self._pb
        elif name == "pb_name":
            return self._pb_name
        elif name == "bc":
            return self._bc
        elif name == "tobytes":
            return self._tobytes
        elif name == "length":
            return len(self._data)
        elif name == "data":
            return self._data

    def __str__(self):
        desc_str = (
            "<{:s} "
            "handle=0x{:04x} pb={:s}(0x{:02x}) bc=0x{:02x} "
            "length={:d} data={:s}>"
        )
        return desc_str.format(
            self.__class__.__name__,
            self.handle,
            self.pb_name,
            self.pb,
            self.bc,
            self.length,
            hexlify(self.data)
        )

    @staticmethod
    def from_buffer(data):
        """
        Parse HCI ACL data

        References can be found here:
        * https://www.bluetooth.org/en-us/specification/adopted-specifications
        ** Core specification 4.1
        ** [vol 2] Part E (Section 5) - HCI Data Formats
        ** [vol 2] Part E (Section 5.4) - Exchange of HCI-specific information
        """
        hci_acl = uctypes.struct(
            uctypes.addressof(data[:HCI_ACL.struct_size]),
            HCI_ACL_STRUCT,
            uctypes.LITTLE_ENDIAN
        )
        data = data[HCI_ACL.struct_size:]
        return HCI_ACL(hci_acl.handle, hci_acl.pb, hci_acl.bc, data)

    def to_buffer(self):
        """
        Get data string
        """
        return ustruct.pack(self.struct_format, self.tobytes) + self.data
