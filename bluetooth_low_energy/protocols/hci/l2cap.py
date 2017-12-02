# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0111
import ustruct
from ubinascii import hexlify, unhexlify
from micropython import const

"""
Fixed channel ids for L2CAP packets

References can be found here:
    * https://www.bluetooth.org/en-us/specification/adopted-specifications - Core specification 4.1
    ** [vol 3] Part A (Section 2.1) - Channel identifiers
"""
L2CAP_CID_NUL = const(0x0000)
L2CAP_CID_SCH = const(0x0001)
L2CAP_CID_ATT = const(0x0004)
L2CAP_CID_LE_SCH = const(0x0005)
L2CAP_CID_SMP = const(0x0006)

L2CAP_CHANNEL_IDS = {
    L2CAP_CID_NUL: "NUL",
    L2CAP_CID_SCH: "SCH",
    L2CAP_CID_ATT: "ATT",
    L2CAP_CID_LE_SCH: "LE_SCH",
    L2CAP_CID_SMP: "SMP"
}


class L2CAP(object):

    struct_format = "<HH"
    struct_size = ustruct.calcsize(struct_format)

    def __init__(self, cid, data=b''):
        self._cid = cid
        self._cid_name = L2CAP_CHANNEL_IDS[cid]
        self._data = data

    def __getattr__(self, name):
        if name == "cid":
            return self._cid
        elif name == "cid_name":
            return self._cid_name
        elif name == "length":
            return len(self._data) if self._data else 0
        elif name == "data":
            return self._data[:self.length]

    def __str__(self):
        desc_str = (
            "<{:s} "
            "cid={:s}(0x{:02x}) length={:d} data={:s}>"
        )
        return desc_str.format(
            self.__class__.__name__,
            self.cid_name,
            self.cid,
            self.length,
            hexlify(self.data)
        )

    @staticmethod
    def from_buffer(data):
        """
        Parse L2CAP packet

         0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
        -----------------------------------------------------------------
        |            length             |          channel id           |
        -----------------------------------------------------------------

        L2CAP is packet-based but follows a communication model based on channels.
        A channel represents a data flow between L2CAP entities in remote devices.
        Channels may be connection-oriented or connectionless. Fixed channels
        other than the L2CAP connectionless channel (CID 0x0002) and the two L2CAP
        signaling channels (CIDs 0x0001 and 0x0005) are considered connection-oriented.

        All L2CAP layer packet fields shall use Little Endian byte order with the exception of the
        information payload field. The endian-ness of higher layer protocols encapsulated within
        L2CAP information payload is protocol-specific

        References can be found here:
        * https://www.bluetooth.org/en-us/specification/adopted-specifications
        ** Core specification 4.1
        ** [vol 3] Part A (Section 3) - Data Packet Format
        """
        _, cid = ustruct.unpack(
            L2CAP.struct_format,
            data[:L2CAP.struct_size]
        )
        data = data[L2CAP.struct_size:]
        return L2CAP(cid, data)

    def to_buffer(self):
        return ustruct.pack(
            self.struct_format,
            self.length,
            self.cid
        ) + self.data


"""
Codes and names for L2CAP Signaling Protocol
"""

SCH_COMMAND_REJECT = const(0x01)
SCH_CONNECTION_REQUEST = const(0x02)
SCH_CONNECTION_RESPONSE = const(0x03)
SCH_CONFIGURE_REQUEST = const(0x04)
SCH_CONFIGURE_RESPONSE = const(0x05)
SCH_DISCONNECTION_REQUEST = const(0x06)
SCH_DISCONNECTION_RESPONSE = const(0x07)
SCH_ECHO_REQUEST = const(0x08)
SCH_ECHO_RESPONSE = const(0x09)
SCH_INFORMATION_REQUEST = const(0x0a)
SCH_INFORMATION_RESPONSE = const(0x0b)
SCH_CREATE_CHANNEL_REQUEST = const(0x0c)
SCH_CREATE_CHANNEL_RESPONSE = const(0x0d)
SCH_MOVE_CHANNEL_REQUEST = const(0x0e)
SCH_MOVE_CHANNEL_RESPONSE = const(0x0f)
SCH_MOVE_CHANNEL_CONFIRMATION = const(0x10)
SCH_MOVE_CHANNEL_CONFIRMATION_RESPONSE = const(0x11)
LE_SCH_CONNECTION_PARAMETER_UPDATE_REQUEST = const(0x12)
LE_SCH_CONNECTION_PARAMETER_UPDATE_RESPONSE = const(0x13)
LE_SCH_LE_CREDIT_BASED_CONNECTION_REQUEST = const(0x14)
LE_SCH_LE_CREDIT_BASED_CONNECTION_RESPONSE = const(0x15)
LE_SCH_LE_FLOW_CONTROL_CREDIT = const(0x16)

L2CAP_SCH_PDUS = {
    SCH_COMMAND_REJECT: "SCH Command reject",
    SCH_CONNECTION_REQUEST: "SCH Connection request",
    SCH_CONNECTION_RESPONSE: "SCH Connection response",
    SCH_CONFIGURE_REQUEST: "SCH Configure request",
    SCH_CONFIGURE_RESPONSE: "SCH Configure response",
    SCH_DISCONNECTION_REQUEST: "SCH Disconnection request",
    SCH_DISCONNECTION_RESPONSE: "SCH Disconnection response",
    SCH_ECHO_REQUEST: "SCH Echo request",
    SCH_ECHO_RESPONSE: "SCH Echo response",
    SCH_INFORMATION_REQUEST: "SCH Information request",
    SCH_INFORMATION_RESPONSE: "SCH Information response",
    SCH_CREATE_CHANNEL_REQUEST: "SCH Create Channel request",
    SCH_CREATE_CHANNEL_RESPONSE: "SCH Create Channel response",
    SCH_MOVE_CHANNEL_REQUEST: "SCH Move Channel request",
    SCH_MOVE_CHANNEL_RESPONSE: "SCH Move Channel response",
    SCH_MOVE_CHANNEL_CONFIRMATION: "SCH Move Channel Confirmation",
    SCH_MOVE_CHANNEL_CONFIRMATION_RESPONSE:
    "SCH Move Channel Confirmation response",
    LE_SCH_CONNECTION_PARAMETER_UPDATE_REQUEST:
        "LE SCH Connection_Parameter_Update_Request",
    LE_SCH_CONNECTION_PARAMETER_UPDATE_RESPONSE:
        "LE SCH Connection_Parameter_Update_Response",
    LE_SCH_LE_CREDIT_BASED_CONNECTION_REQUEST:
        "LE SCH LE_Credit_Based_Connection Request",
    LE_SCH_LE_CREDIT_BASED_CONNECTION_RESPONSE:
        "LE SCH LE_Credit_Based_Connection Response",
    LE_SCH_LE_FLOW_CONTROL_CREDIT:
        "LE SCH LE_Flow_Control_Credit"
}


class L2CAP_SCH(object):
    """L2CAP_SCH"""
    struct_format = "<BBH"
    struct_size = ustruct.calcsize(struct_format)

    def __init__(self, code, cid, data=b''):
        self._code = code
        self._cid = cid
        self._cid_name = L2CAP_SCH_PDUS[id]
        self._data = data

    def __getattr__(self, name):
        if name == "_code":
            return self._code
        elif name == "cid":
            return self._cid
        elif name == "cid_name":
            return self._cid_name
        elif name == "length":
            return len(self._data) if self._data else 0
        elif name == "data":
            return self._data[:self.length]

    def __str__(self):
        desc_str = (
            "<{:s} "
            "code={:02x} cid={:s}(0x{:02x}) length={:d} data={:s}>"
        )
        return desc_str.format(
            self.__class__.__name__,
            self.code,
            self.cid_name,
            self.cid,
            self.length,
            hexlify(self.data)
        )

    @staticmethod
    def from_buffer(data):
        """
        Parse the signaling channel data.

        The signaling channel is a L2CAP packet with channel id 0x0001 (L2CAP CID_SCH)
        or 0x0005 (L2CAP_CID_LE_SCH)

         0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
        -----------------------------------------------------------------
        |      code     |       cid     |             length            |
        -----------------------------------------------------------------

        References can be found here:
        * https://www.bluetooth.org/en-us/specification/adopted-specifications
        ** Core specification 4.1
        ** [vol 3] Part A (Section 4) - Signaling Packet Formats
        """
        code, cid, _ = ustruct.unpack(
            L2CAP_SCH.struct_format,
            data[:L2CAP_SCH.struct_size]
        )
        data = data[L2CAP_SCH.struct_size:]
        return L2CAP_SCH(code, cid, data)

    def to_buffer(self):
        """
        Get data string
        """
        return ustruct.pack(
            self.struct_format,
            self.code,
            self.cid,
            self.length
        ) + self.data
