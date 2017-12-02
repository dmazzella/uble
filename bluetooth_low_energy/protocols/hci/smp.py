# -*- coding: utf-8 -*-
import ustruct
from ubinascii import hexlify, unhexlify
from micropython import const

"""
SMP PDUs

References can be found here:
    * https://www.bluetooth.org/en-us/specification/adopted-specifications - Core specification 4.1
    ** [vol 3] Part H (Section 3.3) - Command Format
"""
PAIRING_REQUEST = const(0x01)
PAIRING_RESPONSE = const(0x02)
PAIRING_CONFIRM = const(0x03)
PAIRING_RANDOM = const(0x04)
PAIRING_FAILED = const(0x05)
ENCRYPTION_INFORMATION = const(0x06)
MASTER_IDENTIFICATION = const(0x07)
IDENTITY_INFORMATION = const(0x08)
IDENTITY_ADDRESS_INFORMATION = const(0x09)
SIGNING_INFORMATION = const(0x0a)
SECURITY_REQUEST = const(0x0b)

SMP_PDUS = {
    PAIRING_REQUEST: "Pairing_Request",
    PAIRING_RESPONSE: "Pairing_Response",
    PAIRING_CONFIRM: "Pairing_Confirm",
    PAIRING_RANDOM: "Pairing_Random",
    PAIRING_FAILED: "Pairing_Failed",
    ENCRYPTION_INFORMATION: "Encryption_Information",
    MASTER_IDENTIFICATION: "Master_Identification",
    IDENTITY_INFORMATION: "Identity_Information",
    IDENTITY_ADDRESS_INFORMATION: "Identity_Address Information",
    SIGNING_INFORMATION: "Signing_Information",
    SECURITY_REQUEST: "Security_Request"
}


class SMP(object):
    """SMP"""
    struct_format = "<B"
    struct_size = ustruct.calcsize(struct_format)

    def __init__(self, code, data=b''):
        self._code = code
        self._code_name = SMP_PDUS[code]
        self._data = data

    def __getattr__(self, name):
        if name == "code":
            return self._code
        elif name == "code_name":
            return self._code_name
        elif name == "length":
            return len(self._data) if self._data else 0
        elif name == "data":
            return self._data[:self.length]

    def __str__(self):
        desc_str = (
            "<{:s} "
            "code={:s}(0x{:02x}) length={:d} data={:s}>"
        )
        return desc_str.format(
            self.__class__.__name__,
            self.code_name,
            self.code,
            self.length,
            hexlify(self.data)
        )

    @staticmethod
    def from_buffer(data):
        """
        SMP code is the first octet of the PDU

         0 1 2 3 4 5 6 7
        -----------------
        |      code     |
        -----------------

        References can be found here:
            * https://www.bluetooth.org/en-us/specification/adopted-specifications
            ** Core specification 4.1
            ** [vol 3] Part H (Section 3.3) - Command Format
        """
        code = ustruct.unpack(SMP.struct_format, data[:SMP.struct_size])[0]
        data = data[SMP.struct_size:]
        return SMP(code, data)

    def to_buffer(self):
        """
        Get data string
        """
        return ustruct.pack(self.struct_format, self.code) + self.data
