# -*- coding: utf-8 -*-
import ustruct
import uctypes
from ubinascii import hexlify, unhexlify

"""
ATT PDUs

References can be found here:
    * https://www.bluetooth.org/en-us/specification/adopted-specifications
    ** Core specification 4.1
    ** [vol 3] Part F (Section 3.4.8) - Attribute Opcode Summary
"""
ATT_PDUS = {
    0x01: "Error_Response",
    0x02: "Exchange_MTU_Request",
    0x03: "Exchange_MTU_Response",
    0x04: "Find_Information_Request",
    0x05: "Find_Information_Response",
    0x06: "Find_By_Type_Value_Request",
    0x07: "Find_By_Type_Value_Response",
    0x08: "Read_By_Type_Request",
    0x09: "Read_By_Type_Response",
    0x0A: "Read_Request",
    0x0B: "Read_Response",
    0x0C: "Read_Blob_Request",
    0x0D: "Read_Blob_Response",
    0x0E: "Read_Multiple_Request",
    0x0F: "Read_Multiple_Response",
    0x10: "Read_By_Group_Type_Request",
    0x11: "Read_By_Group_Type_Response",
    0x12: "Write_Request",
    0x13: "Write_Response",
    0x52: "Write_Command",
    0xD2: "Signed_Write_Command",
    0x16: "Prepare_Write_Request",
    0x17: "Prepare_Write_Response",
    0x18: "Execute_Write_Request",
    0x19: "Execute_Write_Response",
    0x1B: "Handle_Value_Notification",
    0x1D: "Handle_Value_Indication",
    0x1E: "Handle_Value_Confirmation"
}

"""
Attribute opcode is the first octet of the PDU

 0 1 2 3 4 5 6 7
-----------------
|   att opcode  |
-----------------
|     a     |b|c|
-----------------
a - method
b - command flag
c - authentication signature flag

References can be found here:
    * https://www.bluetooth.org/en-us/specification/adopted-specifications
    ** Core specification 4.1
    ** [vol 3] Part F (Section 3.3) - Attribute PDU
"""
ATT_STRUCT = {
    "a": uctypes.BFUINT8 | 0 | 0 << uctypes.BF_POS | 6 << uctypes.BF_LEN,
    "b": uctypes.BFUINT8 | 0 | 6 << uctypes.BF_POS | 1 << uctypes.BF_LEN,
    "c": uctypes.BFUINT8 | 0 | 7 << uctypes.BF_POS | 1 << uctypes.BF_LEN
}


class ATT(object):
    """ATT"""
    struct_format = "<B"
    struct_size = ustruct.calcsize(struct_format)

    def __init__(self, opcode, data=b''):
        self._opcode = opcode
        self._opcode_name = ATT_PDUS[opcode]
        self._data = data

    def __getattr__(self, name):
        if name == "opcode":
            return self._opcode
        elif name == "opcode_name":
            return self._opcode_name
        elif name == "length":
            return len(self._data) if self._data else 0
        elif name == "data":
            return self._data[:self.length]

    def __str__(self):
        desc_str = (
            "<{:s} "
            "opcode={:s}(0x{:02x}) length={:d} data={:s}>"
        )
        return desc_str.format(
            self.__class__.__name__,
            self.opcode_name,
            self.opcode,
            self.length,
            hexlify(self.data)
        )

    @staticmethod
    def from_buffer(data):
        """
        Attribute opcode is the first octet of the PDU

         0 1 2 3 4 5 6 7
        -----------------
        |   att opcode  |
        -----------------
        |     a     |b|c|
        -----------------
        a - method
        b - command flag
        c - authentication signature flag

        References can be found here:
            * https://www.bluetooth.org/en-us/specification/adopted-specifications
            ** Core specification 4.1
            ** [vol 3] Part F (Section 3.3) - Attribute PDU
        """
        opcode = ustruct.unpack(ATT.struct_format, data[:ATT.struct_size])[0]

        att = uctypes.struct(
            uctypes.addressof(data[:ATT.struct_size]),
            ATT_STRUCT,
            uctypes.LITTLE_ENDIAN
        )

        data = data[ATT.struct_size:]
        return ATT(opcode, data)

    def to_buffer(self):
        """
        Get data string
        """
        return ustruct.pack(self.struct_format, self.opcode) + self._data
