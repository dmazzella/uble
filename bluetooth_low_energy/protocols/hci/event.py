# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=C0111
import ustruct
import uctypes
from ubinascii import hexlify, unhexlify
from micropython import const

from bluetooth_low_energy.protocols.hci import HCI_MAX_PAYLOAD_SIZE

"""
Event codes and names for HCI events

Event code is 1 byte.

 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
---------------------------------
|   event code  |    length     |
---------------------------------

However, LE Meta events adds additional data that needs to be handled.

LE_META_EVENT:

 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
-------------------------------------------------
|   event code  |    length     | subevent code |
-------------------------------------------------
"""


"""
The HCI LE Meta Event is used to encapsulate all LE Controller specific events.
The Event Code of all LE Meta Events shall be 0x3E. The Subevent_Code is
the first octet of the event parameters. The Subevent_Code shall be set to one
of the valid Subevent_Codes from an LE specific event
"""
EVT_LE_CONN_COMPLETE = const(0x01)
EVT_LE_ADVERTISING_REPORT = const(0x02)
EVT_LE_CONN_UPDATE_COMPLETE = const(0x03)
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE = const(0x04)
EVT_LE_LTK_REQUEST = const(0x05)

HCI_LE_META_EVENTS = {
    EVT_LE_CONN_COMPLETE: [
        "CONN_COMPLETE",
        {
            "status": uctypes.UINT8 | 0,
            "handle": uctypes.UINT16 | 1,
            "role": uctypes.UINT8 | 3,
            "peer_bdaddr_type": uctypes.UINT8 | 4,
            "peer_bdaddr": (uctypes.ARRAY | 5, uctypes.UINT8 | 6),
            "interval": uctypes.UINT16 | 11,
            "latency": uctypes.UINT16 | 13,
            "supervision_timeout": uctypes.UINT16 | 15,
            "master_clock_accuracy": uctypes.UINT8 | 17
        }
    ],
    EVT_LE_ADVERTISING_REPORT: [
        "ADVERTISING_REPORT",
        {
            "evt_type": uctypes.UINT8 | 0,
            "bdaddr_type":  uctypes.UINT8 | 1,
            "bdaddr": (uctypes.ARRAY | 2, uctypes.UINT8 | 6),
            "data_length":  uctypes.UINT8 | 8,
            "data_RSSI":
            (uctypes.ARRAY | 9, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 9)
        }
    ],
    EVT_LE_CONN_UPDATE_COMPLETE: [
        "CONN_UPDATE_COMPLETE",
        {
            "status": uctypes.UINT8 | 0,
            "handle": uctypes.UINT16 | 1,
            "interval": uctypes.UINT16 | 3,
            "latency": uctypes.UINT16 | 5,
            "supervision_timeout": uctypes.UINT16 | 7,
        }
    ],
    EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE: [
        "READ_REMOTE_USED_FEATURES_COMPLETE",
        {
            "status": uctypes.UINT8 | 0,
            "handle": uctypes.UINT16 | 1,
            "features": (uctypes.ARRAY | 3, uctypes.UINT8 | 8)
        }
    ],
    EVT_LE_LTK_REQUEST: [
        "LTK_REQUEST",
        {
            "handle": uctypes.UINT16 | 0,
            "random": (uctypes.ARRAY | 2, uctypes.UINT8 | 8),
            "ediv": uctypes.UINT16 | 10,
        }
    ]
}

# Vendor Specific HCI_EVENTS
HCI_VENDOR_EVENTS = {}

"""
HCI Event codes

References can be found here:
* https://www.bluetooth.org/en-us/specification/adopted-specifications - Core specification 4.1
** [vol 2] Part E (Section 7.7) - Events
"""
EVT_CONN_COMPLETE = const(0x03)
EVT_DISCONN_COMPLETE = const(0x05)
EVT_ENCRYPT_CHANGE = const(0x08)
EVT_READ_REMOTE_VERSION_COMPLETE = const(0x0C)
EVT_CMD_STATUS = const(0x0F)
EVT_CMD_COMPLETE = const(0x0E)
EVT_HARDWARE_ERROR = const(0x10)
EVT_NUM_COMP_PKTS = const(0x13)
EVT_DATA_BUFFER_OVERFLOW = const(0x1A)
EVT_ENCRYPTION_KEY_REFRESH_COMPLETE = const(0x30)
EVT_LE_META_EVENT = const(0x3E)
EVT_VENDOR = const(0xFF)

HCI_EVENTS = {
    EVT_CONN_COMPLETE: [
        "CONN_COMPLETE",
        {
            "status": uctypes.UINT8 | 0,
            "handle": uctypes.UINT16 | 1,
            "bdaddr": (uctypes.ARRAY | 3, uctypes.UINT8 | 6),
            "link_type": uctypes.UINT8 | 9,
            "encr_mode": uctypes.UINT8 | 10
        }
    ],
    EVT_DISCONN_COMPLETE: [
        "DISCONN_COMPLETE",
        {
            "status": uctypes.UINT8 | 0,
            "handle": uctypes.UINT16 | 1,
            "reason": uctypes.UINT8 | 3
        }
    ],
    EVT_ENCRYPT_CHANGE: [
        "ENCRYPT_CHANGE",
        {
            "status": uctypes.UINT8 | 0,
            "handle": uctypes.UINT16 | 1,
            "encrypt": uctypes.UINT8 | 3
        }
    ],
    EVT_READ_REMOTE_VERSION_COMPLETE: [
        "READ_REMOTE_VERSION_COMPLETE",
        {
            "status": uctypes.UINT8 | 0,
            "connection_handle": uctypes.UINT16 | 1,
            "version": uctypes.UINT8 | 3,
            "manufacturer_name": uctypes.UINT16 | 4,
            "subversion": uctypes.UINT16 | 6
        }
    ],
    EVT_CMD_COMPLETE: [
        "CMD_COMPLETE",
        {
            "ncmd": uctypes.UINT8 | 0,
            "opcode": uctypes.UINT16 | 1
        }
    ],
    EVT_CMD_STATUS: [
        "CMD_STATUS",
        {
            "status": uctypes.UINT8 | 0,
            "ncmd": uctypes.UINT8 | 1,
            "opcode": uctypes.UINT16 | 2
        }
    ],
    EVT_HARDWARE_ERROR: [
        "HARDWARE_ERROR",
        {
            "code": uctypes.UINT8 | 0
        }
    ],
    EVT_NUM_COMP_PKTS: [
        "NUM_COMP_PKTS",
        {
            "num_hndl": uctypes.UINT8 | 0,
            "hndl": (
                uctypes.ARRAY | 1, (HCI_MAX_PAYLOAD_SIZE // 4) - 2,
                {
                    "hndl": uctypes.UINT16 | 0,
                    "num_comp_pkts": uctypes.UINT16 | 2
                }
            )
        }
    ],
    EVT_DATA_BUFFER_OVERFLOW: [
        "DATA_BUFFER_OVERFLOW",
        {
            "link_type": uctypes.UINT8 | 0
        }
    ],
    EVT_ENCRYPTION_KEY_REFRESH_COMPLETE: [
        "ENCRYPTION_KEY_REFRESH_COMPLETE",
        {
            "status": uctypes.UINT8 | 0,
            "handle": uctypes.UINT16 | 1
        }
    ],
    EVT_LE_META_EVENT: [
        "LE_META_EVENT",
        {
            "subevent": uctypes.UINT8 | 0,
            "data": (uctypes.ARRAY | 1, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 1)
        }
    ],
    EVT_VENDOR: [
        "VENDOR",
        {
            "subevent": uctypes.UINT16 | 0,
            "data": (uctypes.ARRAY | 2, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 1)
        }
    ]
}


class HCI_EVENT(object):
    """HCI_EVENT"""
    struct_format = "<BB"
    _struct_size = ustruct.calcsize(struct_format)

    def __init__(self, evtcode, data=b'', module="IDB05A1"):
        evtname, evtstruct = HCI_EVENTS[evtcode]
        subevtcode, subevtname = (0, "")
        if evtcode in (EVT_LE_META_EVENT, EVT_VENDOR):
            subevt = uctypes.struct(
                uctypes.addressof(data),
                evtstruct,
                uctypes.LITTLE_ENDIAN
            )
            subevtcode = subevt.subevent
            if evtcode == EVT_LE_META_EVENT:
                subevtname, evtstruct = HCI_LE_META_EVENTS[subevtcode]
            elif evtcode == EVT_VENDOR:
                subevtname, evtstruct = HCI_VENDOR_EVENTS[subevtcode]
            data = bytes(subevt.data)

        self._evtcode = evtcode
        self._evtname = evtname
        self._subevtcode = subevtcode
        self._subevtname = subevtname
        self._struct = evtstruct
        self._data = data
        self._module = module

    def __getattr__(self, name):
        if name == "evtcode":
            return self._evtcode
        elif name == "evtname":
            return self._evtname
        elif name == "subevtcode":
            return self._subevtcode
        elif name == "subevtname":
            return self._subevtname
        elif name == "struct_size":
            return uctypes.sizeof(self.struct)
        elif name == "struct":
            if self._struct is None:
                return None
            return uctypes.struct(
                uctypes.addressof(self.data),
                self._struct.get(self._module, self._struct),
                uctypes.LITTLE_ENDIAN
            )
        elif name == "length":
            return len(self._data)
        elif name == "data":
            return self._data

    def __str__(self):
        desc_str = (
            "<{:s} evtcode={:s}(0x{:02x}){:s}length={:d} data={:s}>"
        )
        return desc_str.format(
            self.__class__.__name__,
            self.evtname,
            self.evtcode,
            (
                " subevtcode={:s}(0x{:02x}) ".format(
                    self._subevtname,
                    self._subevtcode
                ) if self._subevtcode else " "
            ),
            self.length,
            hexlify(self.data)
        )

    @staticmethod
    def from_buffer(data):
        """
        Parse HCI event data

        References can be found here:
        * https://www.bluetooth.org/en-us/specification/adopted-specifications
          - Core specification 4.1
        ** [vol 2] Part E (Section 5) - HCI Data Formats
        ** [vol 2] Part E (Section 5.4) - Exchange of HCI-specific information
        ** [vol 2] Part E (Section 7.7) - Events
        ** [vol 2] Part E (Section 7.7.65) - Le Meta Event

        All integer values are stored in "little-endian" order.
        """
        evtcode, _ = ustruct.unpack(
            HCI_EVENT.struct_format,
            data[:HCI_EVENT._struct_size]
        )
        data = data[HCI_EVENT._struct_size:]
        return HCI_EVENT(evtcode, data=data)

    def to_buffer(self):
        if self.subevtcode:
            return ustruct.pack(
                self.struct_format + "B",
                self.evtcode,
                self.length,
                self.subevtcode,
            ) + self.data
        return ustruct.pack(
            self.struct_format,
            self.evtcode,
            self.length
        ) + self.data
