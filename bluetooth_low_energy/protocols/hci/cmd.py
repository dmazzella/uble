# -*- coding: utf-8 -*-
import ustruct
import uctypes
from ubinascii import hexlify, unhexlify
from micropython import const

from bluetooth_low_energy.protocols.hci.event import EVT_CMD_STATUS

"""
OpCodes and names for HCI commands according to the Bluetooth specification

OpCode is 2 bytes, of which OGF is the upper 6 bits and OCF is the lower 10 bits.

 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
-------------------------------------------------
|            opcode             |    length     |
-------------------------------------------------
|        OCF        |    OGF    |
---------------------------------
"""

OGF_LINK_CTL = const(0x01)
OGF_HOST_CTL = const(0x03)
OGF_INFO_PARAM = const(0x04)
OGF_STATUS_PARAM = const(0x05)
OGF_LE_CTL = const(0x08)
OGF_VENDOR_CMD = const(0x3f)

OCF_DISCONNECT = const(0x0006)
OCF_RESET = const(0x0003)
OCF_READ_TRANSMIT_POWER_LEVEL = const(0x002D)
OCF_SET_CONTROLLER_TO_HOST_FC = const(0x0031)
OCF_HOST_NUM_COMP_PKTS = const(0x0035)
OCF_READ_LOCAL_VERSION = const(0x0001)
OCF_READ_LOCAL_COMMANDS = const(0x0002)
OCF_READ_LOCAL_FEATURES = const(0x0003)
OCF_READ_BD_ADDR = const(0x0009)
OCF_READ_RSSI = const(0x0005)
OCF_LE_SET_EVENT_MASK = const(0x0001)
OCF_LE_READ_BUFFER_SIZE = const(0x0002)
OCF_LE_READ_LOCAL_SUPPORTED_FEATURES = const(0x0003)
OCF_LE_SET_RANDOM_ADDRESS = const(0x0005)
OCF_LE_SET_ADV_PARAMETERS = const(0x0006)
OCF_LE_READ_ADV_CHANNEL_TX_POWER = const(0x0007)
OCF_LE_SET_ADV_DATA = const(0x0008)
OCF_LE_SET_SCAN_RESPONSE_DATA = const(0x0009)
OCF_LE_SET_ADVERTISE_ENABLE = const(0x000A)
OCF_LE_SET_SCAN_PARAMETERS = const(0x000B)
OCF_LE_SET_SCAN_ENABLE = const(0x000C)
OCF_LE_CREATE_CONN = const(0x000D)
OCF_LE_CREATE_CONN_CANCEL = const(0x000E)
OCF_LE_READ_WHITE_LIST_SIZE = const(0x000F)
OCF_LE_ADD_DEVICE_TO_WHITE_LIST = const(0x0011)
OCF_LE_CLEAR_WHITE_LIST = const(0x0010)
OCF_LE_REMOVE_DEVICE_FROM_WHITE_LIST = const(0x0012)
OCF_LE_CONN_UPDATE = const(0x0013)
OCF_LE_SET_HOST_CHANNEL_CLASSIFICATION = const(0x0014)
OCF_LE_READ_CHANNEL_MAP = const(0x0015)
OCF_LE_READ_REMOTE_USED_FEATURES = const(0x0016)
OCF_LE_ENCRYPT = const(0x0017)
OCF_LE_RAND = const(0x0018)
OCF_LE_START_ENCRYPTION = const(0x0019)
OCF_LE_LTK_REPLY = const(0x001A)
OCF_LE_LTK_NEG_REPLY = const(0x001B)
OCF_LE_READ_SUPPORTED_STATES = const(0x001C)
OCF_LE_RECEIVER_TEST = const(0x001D)
OCF_LE_TRANSMITTER_TEST = const(0x001E)
OCF_LE_TEST_END = const(0x001F)

HCI_COMMANDS = {
    OGF_LINK_CTL: [
        "LINK_CTL",
        {
            OCF_DISCONNECT:
            [
                "DISCONNECT",
                {
                    "handle": uctypes.UINT16 | 0,
                    "reason": uctypes.UINT8 | 2
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ]
        }
    ],
    OGF_HOST_CTL: [
        "HOST_CTL",
        {
            OCF_RESET: [
                "RESET",
                None,
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_READ_TRANSMIT_POWER_LEVEL: [
                "READ_TRANSMIT_POWER_LEVEL",
                {
                    "handle": uctypes.UINT16 | 0,
                    "type": uctypes.UINT8 | 2
                },
                {
                    "status": uctypes.UINT8 | 0,
                    "handle": uctypes.UINT16 | 1,
                    "level": uctypes.UINT8 | 3
                }
            ],
            OCF_SET_CONTROLLER_TO_HOST_FC: [
                "SET_CONTROLLER_TO_HOST_FC",
                None,
                None
            ]
        }
    ],
    OGF_INFO_PARAM: [
        "INFO_PARAM",
        {
            OCF_READ_LOCAL_VERSION: [
                "READ_LOCAL_VERSION",
                None,
                {
                    "status": uctypes.UINT8 | 0,
                    "hci_version": uctypes.UINT8 | 1,
                    "hci_revision": uctypes.UINT16 | 2,
                    "lmp_pal_version": uctypes.UINT8 | 4,
                    "manufacturer_name": uctypes.UINT16 | 5,
                    "lmp_pal_subversion": uctypes.UINT16 | 7
                }
            ],
            OCF_READ_BD_ADDR: [
                "READ_BD_ADDR",
                None,
                {
                    "status": uctypes.UINT8 | 0,
                    "bdaddr": (uctypes.ARRAY | 1, uctypes.UINT8 | 6)
                }
            ],
        }
    ],
    OGF_STATUS_PARAM: [
        "STATUS_PARAM",
        {
            OCF_READ_RSSI: [
                "READ_RSSI",
                {
                    "handle": uctypes.UINT16 | 0
                },
                {
                    "status": uctypes.UINT8 | 0,
                    "handle": uctypes.UINT16 | 1,
                    "rssi": uctypes.UINT8 | 3
                }
            ]
        }
    ],
    OGF_LE_CTL: [
        "LE_CTL",
        {
            OCF_LE_SET_EVENT_MASK: [
                "LE_SET_EVENT_MASK",
                {
                    "mask": (uctypes.ARRAY | 0, uctypes.UINT8 | 8)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_READ_BUFFER_SIZE: [
                "LE_READ_BUFFER_SIZE",
                None,
                {
                    "status": uctypes.UINT8 | 0,
                    "pkt_len": uctypes.UINT16 | 1,
                    "max_pkt": uctypes.UINT8 | 3,
                }
            ],
            OCF_LE_READ_LOCAL_SUPPORTED_FEATURES: [
                "LE_READ_LOCAL_SUPPORTED_FEATURES",
                None,
                {
                    "status": uctypes.UINT8 | 0,
                    "features": (uctypes.ARRAY | 1, uctypes.UINT8 | 8)
                }
            ],
            OCF_LE_SET_RANDOM_ADDRESS: [
                "LE_SET_RANDOM_ADDRESS",
                {
                    "bdaddr": (uctypes.ARRAY | 0, uctypes.UINT8 | 6)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_SET_ADV_PARAMETERS: [
                "LE_SET_ADV_PARAMETERS",
                {
                    "min_interval": uctypes.UINT16 | 0,
                    "max_interval": uctypes.UINT16 | 2,
                    "advtype": uctypes.UINT8 | 4,
                    "own_bdaddr_type": uctypes.UINT8 | 5,
                    "direct_bdaddr_type": uctypes.UINT8 | 6,
                    "direct_bdaddr": (uctypes.ARRAY | 7, uctypes.UINT8 | 6),
                    "chan_map":  uctypes.UINT8 | 13,
                    "filter":  uctypes.UINT8 | 14
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_READ_ADV_CHANNEL_TX_POWER: [
                "LE_READ_ADV_CHANNEL_TX_POWER",
                None,
                {
                    "status": uctypes.UINT8   | 0,
                    "level": uctypes.INT8   | 1
                }
            ],
            OCF_LE_SET_ADV_DATA: [
                "LE_SET_ADV_DATA",
                {
                    "length": uctypes.UINT8   | 0,
                    "data": (uctypes.ARRAY | 1, uctypes.UINT8 | 31)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_SET_SCAN_RESPONSE_DATA: [
                "LE_SET_SCAN_RESPONSE_DATA",
                {
                    "length": uctypes.UINT8   | 0,
                    "data": (uctypes.ARRAY | 1, uctypes.UINT8 | 31)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_SET_ADVERTISE_ENABLE: [
                "LE_SET_ADVERTISE_ENABLE",
                {
                    "enable": uctypes.UINT8 | 0
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_SET_SCAN_PARAMETERS: [
                "LE_SET_SCAN_PARAMETERS",
                {
                    "type": uctypes.UINT8 | 0,
                    "interval": uctypes.UINT16 | 1,
                    "window": uctypes.UINT16 | 3,
                    "own_bdaddr_type": uctypes.UINT8 | 5,
                    "filter": uctypes.UINT8 | 6
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_SET_SCAN_ENABLE: [
                "LE_SET_SCAN_ENABLE",
                {
                    "enable": uctypes.UINT8 | 0,
                    "filter_dup": uctypes.UINT8 | 1
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_CREATE_CONN: [
                "LE_CREATE_CONN",
                {
                    "interval": uctypes.UINT16 | 0,
                    "window": uctypes.UINT16 | 2,
                    "initiator_filter": uctypes.UINT8 | 4,
                    "peer_bdaddr_type": uctypes.UINT8 | 5,
                    "peer_bdaddr": (uctypes.ARRAY | 6, uctypes.UINT8 | 6),
                    "own_bdaddr_type": uctypes.UINT8 | 12,
                    "min_interval": uctypes.UINT16 | 13,
                    "max_interval": uctypes.UINT16 | 15,
                    "latency": uctypes.UINT16 | 17,
                    "supervision_timeout": uctypes.UINT16 | 19,
                    "min_ce_length": uctypes.UINT16 | 21,
                    "max_ce_length": uctypes.UINT16 | 23
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_CREATE_CONN_CANCEL: [
                "LE_CREATE_CONN_CANCEL",
                None,
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_READ_WHITE_LIST_SIZE: [
                "LE_READ_WHITE_LIST_SIZE",
                None,
                {
                    "status": uctypes.UINT8 | 0,
                    "size": uctypes.UINT8 | 1
                }
            ],
            OCF_LE_ADD_DEVICE_TO_WHITE_LIST: [
                "LE_ADD_DEVICE_TO_WHITE_LIST",
                {
                    "bdaddr_type": uctypes.UINT8 | 0,
                    "bdaddr": (uctypes.ARRAY | 1, uctypes.UINT8 | 6)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_CLEAR_WHITE_LIST: [
                "LE_CLEAR_WHITE_LIST",
                None,
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_REMOVE_DEVICE_FROM_WHITE_LIST: [
                "LE_REMOVE_DEVICE_FROM_WHITE_LIST",
                {
                    "bdaddr_type": uctypes.UINT8 | 0,
                    "bdaddr": (uctypes.ARRAY | 1, uctypes.UINT8 | 6)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_CONN_UPDATE: [
                "LE_CONN_UPDATE",
                {
                    "handle": uctypes.UINT16 | 0,
                    "min_interval": uctypes.UINT16 | 2,
                    "max_interval": uctypes.UINT16 | 4,
                    "latency": uctypes.UINT16 | 6,
                    "supervision_timeout": uctypes.UINT16 | 8,
                    "min_ce_length": uctypes.UINT16 | 10,
                    "max_ce_length": uctypes.UINT16 | 12
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_SET_HOST_CHANNEL_CLASSIFICATION: [
                "LE_SET_HOST_CHANNEL_CLASSIFICATION",
                {
                    "map": (uctypes.ARRAY | 0, uctypes.UINT8 | 5)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_READ_CHANNEL_MAP: [
                "LE_READ_CHANNEL_MAP",
                {
                    "handle": uctypes.UINT16 | 0
                },
                {
                    "status": uctypes.UINT8 | 0,
                    "handle": uctypes.UINT16 | 1,
                    "map": (uctypes.ARRAY | 3, uctypes.UINT8 | 5)
                }
            ],
            OCF_LE_READ_REMOTE_USED_FEATURES: [
                "LE_READ_REMOTE_USED_FEATURES",
                {
                    "handle": uctypes.UINT16 | 0
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_ENCRYPT: [
                "LE_ENCRYPT",
                {
                    "key": (uctypes.ARRAY | 0, uctypes.UINT8 | 16),
                    "plaintext": (uctypes.ARRAY | 16, uctypes.UINT8 | 16)
                },
                {
                    "status": uctypes.UINT8 | 0,
                    "encdata": (uctypes.ARRAY | 1, uctypes.UINT8 | 16)
                }
            ],
            OCF_LE_RAND: [
                "LE_RAND",
                None,
                {
                    "status": uctypes.UINT8 | 0,
                    "random": (uctypes.ARRAY | 1, uctypes.UINT8 | 8)
                }
            ],
            OCF_LE_START_ENCRYPTION: [
                "LE_START_ENCRYPTION",
                {
                    "handle": uctypes.UINT16 | 0,
                    "random": (uctypes.ARRAY | 2, uctypes.UINT8 | 8),
                    "diversifier": uctypes.UINT16 | 10,
                    "key": (uctypes.ARRAY | 12, uctypes.UINT8 | 16)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_LTK_REPLY: [
                "LE_LTK_REPLY",
                {
                    "handle": uctypes.UINT16 | 0,
                    "key": (uctypes.ARRAY | 2, uctypes.UINT8 | 16)
                },
                {
                    "status": uctypes.UINT8 | 0,
                    "handle": uctypes.UINT16 | 1
                }
            ],
            OCF_LE_LTK_NEG_REPLY: [
                "LE_LTK_NEG_REPLY",
                {
                    "handle": uctypes.UINT16 | 0
                },
                {
                    "status": uctypes.UINT8 | 0,
                    "handle": uctypes.UINT16 | 1
                }
            ],
            OCF_LE_READ_SUPPORTED_STATES: [
                "LE_READ_SUPPORTED_STATES",
                {
                    "status": uctypes.UINT8 | 0,
                    "states": (uctypes.ARRAY | 1, uctypes.UINT8 | 8)
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_RECEIVER_TEST: [
                "LE_RECEIVER_TEST",
                {
                    "frequency": uctypes.UINT8 | 0
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_TRANSMITTER_TEST: [
                "LE_TRANSMITTER_TEST",
                {
                    "frequency": uctypes.UINT8 | 0,
                    "length": uctypes.UINT8 | 1,
                    "payload": uctypes.UINT8 | 2
                },
                {
                    "status": uctypes.UINT8 | 0
                }
            ],
            OCF_LE_TEST_END: [
                "LE_TEST_END",
                None,
                {
                    "status": uctypes.UINT8 | 0,
                    "num_pkts": uctypes.UINT16 | 1
                }
            ]
        }
    ],
    OGF_VENDOR_CMD: [
        "VENDOR_CMD",
        None
    ]
}

class OPCODE(object):
    """OPCODE"""
    @staticmethod
    def pack(ogf, ocf):
        """pack"""
        return (ocf & 0x03ff)|(ogf << 10)

    @staticmethod
    def unpack(opcode):
        """unpack"""
        return (opcode >> 10), (opcode & 0x03ff)

class HCI_COMMAND(object):
    """HCI_COMMAND"""
    _struct_format = "<HB"
    _struct_size = ustruct.calcsize(_struct_format)

    def __init__(self, ogf=0, ocf=0, opcode=0, data=b'', evtcode=EVT_CMD_STATUS, module="IDB05A1"):
        if ogf and ocf:
            opcode = OPCODE.pack(ogf, ocf)
        elif opcode:
            ogf, ocf = OPCODE.unpack(opcode)
        else:
            raise ValueError('ogf, ocf or opcode')
        ogf_name, ocf_dict = HCI_COMMANDS[ogf]
        ocf_name, request_struct, response_struct = ocf_dict[ocf]

        self._opcode = opcode
        self._ogf = ogf
        self._ogf_name = ogf_name
        self._ocf = ocf
        self._ocf_name = ocf_name
        self._evtcode = evtcode
        self._request_struct = request_struct
        self._request_data = data
        self._response_struct = response_struct
        self._response_data = b''
        self._module = module

    def __getattr__(self, name):
        if name == "ogf":
            return self._ogf
        elif name == "ogf_name":
            return self._ogf_name
        elif name == "ocf":
            return self._ocf
        elif name == "ocf_name":
            return self._ocf_name
        elif name == "opcode":
            return self._opcode
        elif name == "evtcode":
            return self._evtcode
        elif name == "request_struct":
            if self._request_struct is None:
                return None
            return uctypes.struct(
                uctypes.addressof(self.request_data),
                self._request_struct.get(self._module, self._request_struct),
                uctypes.LITTLE_ENDIAN
            )
        elif name == "response_struct":
            if self._response_struct is None:
                return None
            return uctypes.struct(
                uctypes.addressof(self.response_data),
                self._response_struct.get(self._module, self._response_struct),
                uctypes.LITTLE_ENDIAN
            )
        elif name == "request_length":
            return len(self._request_data) if self._request_data else 0
        elif name == "request_data":
            return self._request_data[:self.request_length]
        elif name == "response_length":
            return len(self._response_data) if self._response_data else 0
        elif name == "response_data":
            return self._response_data[:self.response_length]
        else:
            raise AttributeError(name)

    def __str__(self):
        desc_str = (
            "<{:s} "
            "opcode=0x{:04x} ogf={:s}(0x{:02x}) ocf={:s}(0x{:02x}) "
            "request_data={:s} response_data={:s}>"
        )
        return desc_str.format(
            self.__class__.__name__,
            self.opcode, self.ogf_name, self.ogf, self.ocf_name, self.ocf,
            hexlify(self.request_data),
            hexlify(self.response_data)
        )

    @staticmethod
    def from_buffer(data):
        """
        Parse HCI command

        References can be found here:
        * https://www.bluetooth.org/en-us/specification/adopted-specifications
        ** Core specification 4.1
        ** [vol 2] Part E (Section 5) - HCI Data Formats
        ** [vol 2] Part E (Section 5.4) - Exchange of HCI-specific information

        All integer values are stored in "little-endian" order.
        """
        opcode, length = ustruct.unpack_from(
            HCI_COMMAND._struct_format, data[:HCI_COMMAND._struct_size]
        )
        data = data[HCI_COMMAND._struct_size:]
        return HCI_COMMAND(opcode=opcode, data=data)

    def to_buffer(self, split=False):
        """
        Get data string
        """
        header_param = (
            ustruct.pack(
                self._struct_format,
                self.opcode,
                self.request_length
            ),
            self.request_data
        )
        return header_param if split else b''.join(header_param)
