# -*- coding: utf-8 -*-
import ustruct
import uctypes
from ubinascii import hexlify, unhexlify
from micropython import const

"""
SCO handle is 12 bits, followed by 2 bits packet status flags.

 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
-------------------------------------------------
|            handle     |ps |xx |    length     |
-------------------------------------------------
"""
HCI_SCO_STRUCT = {
    "handle": uctypes.BFUINT16 | 0 | 0 << uctypes.BF_POS | 12 << uctypes.BF_LEN,
    "ps": uctypes.BFUINT16 | 0 | 12 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
    "xx": uctypes.BFUINT16 | 0 | 14 << uctypes.BF_POS | 2 << uctypes.BF_LEN,
    "length": uctypes.UINT8 | 2
}


class HCI_SCO(object):
    """HCI_SCO"""
    struct_format = "<HB"
    struct_size = ustruct.calcsize(struct_format)

    def __init__(self, handle, ps=0, xx=0, data=b''):
        bin_str = "{:016b}{:02b}{:02b}{:012b}".format(
            len(data) if data else 0, xx, ps, handle
        )
        self._handle = handle
        self._ps = ps
        self._xx = xx
        self._tobytes = int(bin_str, 2)
        self._data = data

    def __getattr__(self, name):
        if name == "handle":
            return self._handle
        elif name == "ps":
            return self._ps
        elif name == "xx":
            return self._xx
        elif name == "tobytes":
            return self._tobytes
        elif name == "length":
            return len(self._data) if self._data else 0
        elif name == "data":
            return self._data[:self.length]

    def __str__(self):
        desc_str = (
            "<{:s} "
            "handle=0x{:04x} ps=0x{:02x} xx=0x{:02x} "
            "length={:d} data={:s}>"
        )
        return desc_str.format(
            self.__class__.__name__,
            self.handle,
            self.ps,
            self.xx,
            self.length,
            hexlify(self.data)
        )

    @staticmethod
    def from_buffer(data):
        """
        Parse HCI SCO data

        References can be found here:
        * https://www.bluetooth.org/en-us/specification/adopted-specifications
        ** Core specification 4.1
        ** [vol 2] Part E (Section 5) - HCI Data Formats
        ** [vol 2] Part E (Section 5.4) - Exchange of HCI-specific information
        """
        hci_sco = uctypes.struct(
            uctypes.addressof(data[:HCI_SCO.struct_size]),
            HCI_SCO_STRUCT,
            uctypes.LITTLE_ENDIAN
        )
        data = data[HCI_SCO.struct_size:]
        return HCI_SCO(hci_sco.handle, hci_sco.ps, hci_sco.xx, data)

    def to_buffer(self):
        """
        Get data string
        """
        return ustruct.pack(self.struct_format, self.tobytes) + self.data
