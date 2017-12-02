# -*- coding: utf-8 -*-
# pylint: disable=C0111
# pylint: disable=C0302
import uctypes
from micropython import const

from bluetooth_low_energy.protocols.hci import HCI_MAX_PAYLOAD_SIZE

OCF_HAL_GET_FW_BUILD_NUMBER = const(0x0000)
OCF_HAL_WRITE_CONFIG_DATA = const(0x000C)
OCF_HAL_READ_CONFIG_DATA = const(0x000D)
OCF_HAL_SET_TX_POWER_LEVEL = const(0x000F)
OCF_HAL_DEVICE_STANDBY = const(0x0013)
OCF_HAL_LE_TX_TEST_PACKET_NUMBER = const(0x0014)
OCF_HAL_TONE_START = const(0x0015)
OCF_HAL_TONE_STOP = const(0x0016)
OCF_HAL_GET_LINK_STATUS = const(0x0017)
OCF_HAL_GET_ANCHOR_PERIOD = const(0x0019)
OCF_UPDATER_START = const(0x0020)
OCF_UPDATER_REBOOT = const(0x0021)
OCF_GET_UPDATER_VERSION = const(0x0022)
OCF_GET_UPDATER_BUFSIZE = const(0x0023)
OCF_UPDATER_ERASE_BLUE_FLAG = const(0x0024)
OCF_UPDATER_RESET_BLUE_FLAG = const(0x0025)
OCF_UPDATER_ERASE_SECTOR = const(0x0026)
OCF_UPDATER_READ_DATA_BLOCK = const(0x0028)
OCF_UPDATER_PROG_DATA_BLOCK = const(0x0027)
OCF_UPDATER_CALC_CRC = const(0x0029)
OCF_UPDATER_HW_VERSION = const(0x002A)
OCF_GAP_SET_NON_DISCOVERABLE = const(0x0081)
OCF_GAP_SET_LIMITED_DISCOVERABLE = const(0x0082)
OCF_GAP_SET_DISCOVERABLE = const(0x0083)
OCF_GAP_SET_DIRECT_CONNECTABLE = const(0x0084)
OCF_GAP_SET_IO_CAPABILITY = const(0x0085)
OCF_GAP_SET_AUTH_REQUIREMENT = const(0x0086)
OCF_GAP_SET_AUTHOR_REQUIREMENT = const(0x0087)
OCF_GAP_PASSKEY_RESPONSE = const(0x0088)
OCF_GAP_AUTHORIZATION_RESPONSE = const(0x0089)
OCF_GAP_INIT = const(0x008A)
OCF_GAP_SET_NON_CONNECTABLE = const(0x008B)
OCF_GAP_SET_UNDIRECTED_CONNECTABLE = const(0x008C)
OCF_GAP_SLAVE_SECURITY_REQUEST = const(0x008D)
OCF_GAP_UPDATE_ADV_DATA = const(0x008E)
OCF_GAP_DELETE_AD_TYPE = const(0x008F)
OCF_GAP_GET_SECURITY_LEVEL = const(0x0090)
OCF_GAP_SET_EVT_MASK = const(0x0091)
OCF_GAP_CONFIGURE_WHITELIST = const(0x0092)
OCF_GAP_TERMINATE = const(0x0093)
OCF_GAP_CLEAR_SECURITY_DB = const(0x0094)
OCF_GAP_ALLOW_REBOND_DB = const(0x0095)
OCF_GAP_START_LIMITED_DISCOVERY_PROC = const(0x0096)
OCF_GAP_START_GENERAL_DISCOVERY_PROC = const(0x0097)
OCF_GAP_START_NAME_DISCOVERY_PROC = const(0x0098)
OCF_GAP_START_AUTO_CONN_ESTABLISH_PROC = const(0x0099)
OCF_GAP_START_GENERAL_CONN_ESTABLISH_PROC = const(0x009A)
OCF_GAP_START_SELECTIVE_CONN_ESTABLISH_PROC = const(0x009B)
OCF_GAP_CREATE_CONNECTION = const(0x009C)
OCF_GAP_TERMINATE_GAP_PROCEDURE = const(0x009D)
OCF_GAP_START_CONNECTION_UPDATE = const(0x009E)
OCF_GAP_SEND_PAIRING_REQUEST = const(0x009F)
OCF_GAP_RESOLVE_PRIVATE_ADDRESS = const(0x00A0)
OCF_GAP_SET_BROADCAST_MODE = const(0x00A1)
OCF_GAP_START_OBSERVATION_PROC = const(0x00A2)
OCF_GAP_GET_BONDED_DEVICES = const(0x00A3)
OCF_GAP_IS_DEVICE_BONDED = const(0x00A4)
OCF_GATT_INIT = const(0x0101)
OCF_GATT_ADD_SERV = const(0x0102)
OCF_GATT_INCLUDE_SERV = const(0x0103)
OCF_GATT_ADD_CHAR = const(0x0104)
OCF_GATT_ADD_CHAR_DESC = const(0x0105)
OCF_GATT_UPD_CHAR_VAL = const(0x0106)
OCF_GATT_DEL_CHAR = const(0x0107)
OCF_GATT_DEL_SERV = const(0x0108)
OCF_GATT_DEL_INC_SERV = const(0x0109)
OCF_GATT_SET_EVT_MASK = const(0x010A)
OCF_GATT_EXCHANGE_CONFIG = const(0x010B)
OCF_ATT_FIND_INFO_REQ = const(0x010C)
OCF_ATT_FIND_BY_TYPE_VALUE_REQ = const(0x010D)
OCF_ATT_READ_BY_TYPE_REQ = const(0x010E)
OCF_ATT_READ_BY_GROUP_TYPE_REQ = const(0x010F)
OCF_ATT_PREPARE_WRITE_REQ = const(0x0110)
OCF_ATT_EXECUTE_WRITE_REQ = const(0x0111)
OCF_GATT_DISC_ALL_PRIM_SERVICES = const(0x0112)
OCF_GATT_DISC_PRIM_SERVICE_BY_UUID = const(0x0113)
OCF_GATT_FIND_INCLUDED_SERVICES = const(0x0114)
OCF_GATT_DISC_ALL_CHARAC_OF_SERV = const(0x0115)
OCF_GATT_DISC_CHARAC_BY_UUID = const(0x0116)
OCF_GATT_DISC_ALL_CHARAC_DESCRIPTORS = const(0x0117)
OCF_GATT_READ_CHARAC_VAL = const(0x0118)
OCF_GATT_READ_USING_CHARAC_UUID = const(0x0109)
OCF_GATT_READ_LONG_CHARAC_VAL = const(0x011A)
OCF_GATT_READ_MULTIPLE_CHARAC_VAL = const(0x011B)
OCF_GATT_WRITE_CHAR_VALUE = const(0x011C)
OCF_GATT_WRITE_LONG_CHARAC_VAL = const(0x011D)
OCF_GATT_WRITE_CHARAC_RELIABLE = const(0x011E)
OCF_GATT_WRITE_LONG_CHARAC_DESC = const(0x011F)
OCF_GATT_READ_LONG_CHARAC_DESC = const(0x0120)
OCF_GATT_WRITE_CHAR_DESC = const(0x0121)
OCF_GATT_READ_CHAR_DESC = const(0x0122)
OCF_GATT_WRITE_WITHOUT_RESPONSE = const(0x0123)
OCF_GATT_SIGNED_WRITE_WITHOUT_RESPONSE = const(0x0124)
OCF_GATT_CONFIRM_INDICATION = const(0x0125)
OCF_GATT_WRITE_RESPONSE = const(0x0126)
OCF_GATT_ALLOW_READ = const(0x0127)
OCF_GATT_SET_SECURITY_PERMISSION = const(0x0128)
OCF_GATT_SET_DESC_VAL = const(0x0129)
OCF_GATT_READ_HANDLE_VALUE = const(0x012A)
OCF_GATT_READ_HANDLE_VALUE_OFFSET = const(0x012B)
OCF_GATT_UPD_CHAR_VAL_EXT = const(0x012C)
OCF_L2CAP_CONN_PARAM_UPDATE_REQ = const(0x0181)
OCF_L2CAP_CONN_PARAM_UPDATE_RESP = const(0x0182)

HCI_VENDOR_COMMANDS = [
    "VENDOR_CMD",
    {
        OCF_HAL_GET_FW_BUILD_NUMBER: [
            "HAL_GET_FW_BUILD_NUMBER",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "build_number": uctypes.UINT16 | 1
            }
        ],
        OCF_HAL_WRITE_CONFIG_DATA: [
            "HAL_WRITE_CONFIG_DATA",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_HAL_READ_CONFIG_DATA: [
            "HAL_READ_CONFIG_DATA",
            None,
            {
                "offset": uctypes.UINT8 | 0
            }
        ],
        OCF_HAL_SET_TX_POWER_LEVEL: [
            "HAL_SET_TX_POWER_LEVEL",
            {
                "en_high_power": uctypes.UINT8 | 0,
                "pa_level": uctypes.UINT8 | 1
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_HAL_DEVICE_STANDBY: [
            "HAL_DEVICE_STANDBY",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_HAL_LE_TX_TEST_PACKET_NUMBER: [
            "HAL_LE_TX_TEST_PACKET_NUMBER",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "number_of_packets": uctypes.UINT32 | 1
            }
        ],
        OCF_HAL_TONE_START: [
            "HAL_TONE_START",
            {
                "rf_channel": uctypes.UINT8 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_HAL_TONE_STOP: [
            "HAL_TONE_STOP",
            {
                "rf_channel": uctypes.UINT8 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_HAL_GET_LINK_STATUS: [
            "HAL_GET_LINK_STATUS",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "link_status": (uctypes.ARRAY | 1, uctypes.UINT8 | 8),
                "conn_handle": (uctypes.ARRAY | 9, uctypes.UINT16 | 8)
            }
        ],
        OCF_HAL_GET_ANCHOR_PERIOD: [
            "HAL_GET_ANCHOR_PERIOD",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "anchor_period": uctypes.UINT32 | 1,
                "max_free_slot": uctypes.UINT32 | 5
            }
        ],
        OCF_UPDATER_START: [
            "UPDATER_START",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_UPDATER_REBOOT: [
            "UPDATER_REBOOT",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GET_UPDATER_VERSION: [
            "GET_UPDATER_VERSION",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "version": uctypes.UINT8 | 1
            }
        ],
        OCF_GET_UPDATER_BUFSIZE: [
            "GET_UPDATER_BUFSIZE",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "buffer_size": uctypes.UINT8 | 1
            }
        ],
        OCF_UPDATER_ERASE_BLUE_FLAG: [
            "UPDATER_ERASE_BLUE_FLAG",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_UPDATER_RESET_BLUE_FLAG: [
            "UPDATER_RESET_BLUE_FLAG",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_UPDATER_ERASE_SECTOR: [
            "UPDATER_ERASE_SECTOR",
            {
                "address": uctypes.UINT32 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_UPDATER_READ_DATA_BLOCK: [
            "UPDATER_READ_DATA_BLOCK",
            {
                "address": uctypes.UINT32 | 0,
                "data_len": uctypes.UINT16 | 4
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_UPDATER_PROG_DATA_BLOCK: [
            "UPDATER_PROG_DATA_BLOCK",
            {
                "address": uctypes.UINT32 | 0,
                "data_len": uctypes.UINT16 | 4,
                "data":
                (uctypes.ARRAY | 6, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 6)
            },
            {
                "status": uctypes.UINT8 | 0,
                "data":
                (uctypes.ARRAY | 1, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 1)
            }
        ],
        OCF_UPDATER_CALC_CRC: [
            "UPDATER_CALC_CRC",
            {
                "address": uctypes.UINT32 | 0,
                "num_sectors": uctypes.UINT8 | 4
            },
            {
                "status": uctypes.UINT8 | 0,
                "crc": uctypes.UINT32 | 1
            }
        ],
        OCF_UPDATER_HW_VERSION: [
            "UPDATER_HW_VERSION",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "version": uctypes.UINT8 | 1
            }
        ],
        OCF_GAP_SET_NON_DISCOVERABLE: [
            "GAP_SET_NON_DISCOVERABLE",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SET_LIMITED_DISCOVERABLE: [
            "GAP_SET_LIMITED_DISCOVERABLE",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SET_DISCOVERABLE: [
            "GAP_SET_DISCOVERABLE",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SET_DIRECT_CONNECTABLE: [
            "GAP_SET_DIRECT_CONNECTABLE",
            {
                "IDB05A1": {
                    "own_bdaddr_type": uctypes.UINT8 | 0,
                    "directed_adv_type": uctypes.UINT8 | 1,
                    "direct_bdaddr_type": uctypes.UINT8 | 2,
                    "direct_bdaddr": (uctypes.ARRAY | 3, uctypes.UINT8 | 6),
                    "adv_interv_min": uctypes.UINT16 | 9,
                    "adv_interv_max": uctypes.UINT16 | 11
                },
                "IDB04A1": {
                    "own_bdaddr_type": uctypes.UINT8 | 0,
                    "direct_bdaddr_type": uctypes.UINT8 | 1,
                    "direct_bdaddr": (uctypes.ARRAY | 2, uctypes.UINT8 | 6)
                }
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SET_IO_CAPABILITY: [
            "GAP_SET_IO_CAPABILITY",
            {
                "io_capability": uctypes.UINT8 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SET_AUTH_REQUIREMENT: [
            "GAP_SET_AUTH_REQUIREMENT",
            {
                "mitm_mode": uctypes.UINT8 | 0,
                "oob_enable": uctypes.UINT8 | 1,
                "oob_data": (uctypes.ARRAY | 2, uctypes.UINT8 | 16),
                "min_encryption_key_size": uctypes.UINT8 | 18,
                "max_encryption_key_size": uctypes.UINT8 | 19,
                "use_fixed_pin": uctypes.UINT8 | 20,
                "fixed_pin": uctypes.UINT32 | 21,
                "bonding_mode": uctypes.UINT8 | 25
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SET_AUTHOR_REQUIREMENT: [
            "GAP_SET_AUTHOR_REQUIREMENT",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "authorization_enable": uctypes.UINT8 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_PASSKEY_RESPONSE: [
            "GAP_PASSKEY_RESPONSE",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "passkey": uctypes.UINT32 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_AUTHORIZATION_RESPONSE: [
            "GAP_AUTHORIZATION_RESPONSE",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "authorize": uctypes.UINT8 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_INIT: [
            "GAP_INIT",
            {
                "IDB05A1": {
                    "role": uctypes.UINT8 | 0,
                    "privacy_enabled": uctypes.UINT8 | 1,
                    "device_name_char_len": uctypes.UINT8 | 2
                },
                "IDB04A1": {
                    "role": uctypes.UINT8 | 0
                }
            },
            {
                "status": uctypes.UINT8 | 0,
                "service_handle": uctypes.UINT16 | 1,
                "dev_name_char_handle": uctypes.UINT16 | 3,
                "appearance_char_handle": uctypes.UINT16 | 5
            }
        ],
        OCF_GAP_SET_NON_CONNECTABLE: [
            "GAP_SET_NON_CONNECTABLE",
            {
                "IDB05A1": {
                    "advertising_event_type": uctypes.UINT8 | 0,
                    "own_address_type": uctypes.UINT8 | 1
                },
                "IDB04A1": {
                    "advertising_event_type": uctypes.UINT8 | 0
                }
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SET_UNDIRECTED_CONNECTABLE: [
            "GAP_SET_UNDIRECTED_CONNECTABLE",
            {
                "adv_filter_policy": uctypes.UINT8 | 0,
                "own_addr_type": uctypes.UINT8 | 1
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SLAVE_SECURITY_REQUEST: [
            "GAP_SLAVE_SECURITY_REQUEST",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "bonding": uctypes.UINT8 | 2,
                "mitm_protection": uctypes.UINT8 | 3
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_UPDATE_ADV_DATA: [
            "GAP_UPDATE_ADV_DATA",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_DELETE_AD_TYPE: [
            "GAP_DELETE_AD_TYPE",
            {
                "ad_type": uctypes.UINT8 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_GET_SECURITY_LEVEL: [
            "GAP_GET_SECURITY_LEVEL",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "mitm_protection": uctypes.UINT8 | 1,
                "bonding": uctypes.UINT8 | 2,
                "oob_data": uctypes.UINT8 | 3,
                "passkey_required": uctypes.UINT8 | 4
            }
        ],
        OCF_GAP_SET_EVT_MASK: [
            "GAP_SET_EVT_MASK",
            {
                "evt_mask": uctypes.UINT16 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_CONFIGURE_WHITELIST: [
            "GAP_CONFIGURE_WHITELIST",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_TERMINATE: [
            "GAP_TERMINATE",
            {
                "handle": uctypes.UINT16 | 0,
                "reason": uctypes.UINT8 | 1
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_CLEAR_SECURITY_DB: [
            "GAP_CLEAR_SECURITY_DB",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_ALLOW_REBOND_DB: [
            "GAP_ALLOW_REBOND_DB",
            {
                "conn_handle": uctypes.UINT16 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_START_LIMITED_DISCOVERY_PROC: [
            "GAP_START_LIMITED_DISCOVERY_PROC",
            {
                "scan_interval": uctypes.UINT16 | 0,
                "scan_window": uctypes.UINT16 | 2,
                "own_address_type": uctypes.UINT16 | 2,
                "filter_duplicates": uctypes.UINT8 | 5
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_START_GENERAL_DISCOVERY_PROC: [
            "GAP_START_GENERAL_DISCOVERY_PROC",
            {
                "scan_interval": uctypes.UINT16 | 0,
                "scan_window": uctypes.UINT16 | 2,
                "own_address_type": uctypes.UINT16 | 2,
                "filter_duplicates": uctypes.UINT8 | 5
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_START_NAME_DISCOVERY_PROC: [
            "GAP_START_NAME_DISCOVERY_PROC",
            {
                "scan_interval": uctypes.UINT16 | 0,
                "scan_window": uctypes.UINT16 | 2,
                "peer_bdaddr_type": uctypes.UINT8 | 4,
                "peer_bdaddr": (uctypes.ARRAY | 5, uctypes.UINT8 | 6),
                "own_bdaddr_type": uctypes.UINT8 | 11,
                "conn_min_interval": uctypes.UINT16 | 12,
                "conn_max_interval": uctypes.UINT16 | 14,
                "conn_latency": uctypes.UINT16 | 16,
                "supervision_timeout": uctypes.UINT16 | 18,
                "min_conn_length": uctypes.UINT16 | 20,
                "max_conn_length": uctypes.UINT16 | 22
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_START_AUTO_CONN_ESTABLISH_PROC: [
            "GAP_START_AUTO_CONN_ESTABLISH_PROC",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_START_GENERAL_CONN_ESTABLISH_PROC: [
            "GAP_START_GENERAL_CONN_ESTABLISH_PROC",
            {
                "IDB05A1": {
                    "scan_type": uctypes.UINT8 | 0,
                    "scan_interval": uctypes.UINT16 | 1,
                    "scan_window": uctypes.UINT16 | 3,
                    "own_address_type": uctypes.UINT8 | 5,
                    "filter_duplicates": uctypes.UINT8 | 6
                },
                "IDB04A1": {
                    "scan_type": uctypes.UINT8 | 0,
                    "scan_interval": uctypes.UINT16 | 1,
                    "scan_window": uctypes.UINT16 | 3,
                    "own_address_type": uctypes.UINT8 | 5,
                    "filter_duplicates": uctypes.UINT8 | 6,
                    "reconn_addr": (uctypes.ARRAY | 7, uctypes.UINT8 | 6)
                }
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_START_SELECTIVE_CONN_ESTABLISH_PROC: [
            "GAP_START_SELECTIVE_CONN_ESTABLISH_PROC",
            {
                "scan_type": uctypes.UINT8 | 0,
                "scan_interval": uctypes.UINT16 | 1,
                "scan_window": uctypes.UINT16 | 3,
                "own_address_type": uctypes.UINT8 | 5,
                "filter_duplicates": uctypes.UINT8 | 6,
                "num_whitelist_entries": uctypes.UINT8 | 7,
                "addr_array":
                (uctypes.ARRAY | 8, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 8)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_CREATE_CONNECTION: [
            "GAP_CREATE_CONNECTION",
            {
                "scan_interval": uctypes.UINT16 | 0,
                "scan_window": uctypes.UINT16 | 2,
                "peer_bdaddr_type": uctypes.UINT8 | 4,
                "peer_bdaddr": (uctypes.ARRAY | 5, uctypes.UINT8 | 6),
                "own_bdaddr_type": uctypes.UINT8 | 11,
                "conn_min_interval": uctypes.UINT16 | 12,
                "conn_max_interval": uctypes.UINT16 | 14,
                "conn_latency": uctypes.UINT16 | 16,
                "supervision_timeout": uctypes.UINT16 | 18,
                "min_conn_length": uctypes.UINT16 | 20,
                "max_conn_length": uctypes.UINT16 | 22
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_TERMINATE_GAP_PROCEDURE: [
            "GAP_TERMINATE_GAP_PROCEDURE",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_START_CONNECTION_UPDATE: [
            "GAP_START_CONNECTION_UPDATE",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "conn_min_interval": uctypes.UINT16 | 2,
                "conn_max_interval": uctypes.UINT16 | 4,
                "conn_latency": uctypes.UINT16 | 6,
                "supervision_timeout": uctypes.UINT16 | 8,
                "min_conn_length": uctypes.UINT16 | 10,
                "max_conn_length": uctypes.UINT16 | 12
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SEND_PAIRING_REQUEST: [
            "GAP_SEND_PAIRING_REQUEST",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "force_rebond": uctypes.UINT8 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_RESOLVE_PRIVATE_ADDRESS: [
            "GAP_RESOLVE_PRIVATE_ADDRESS",
            {
                "IDB05A1": {
                    "address": (uctypes.ARRAY | 0, uctypes.UINT8 | 6)
                },
                "IDB04A1": None
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_SET_BROADCAST_MODE: [
            "GAP_SET_BROADCAST_MODE",
            {
                "adv_interv_min": uctypes.UINT16 | 0,
                "adv_interv_max": uctypes.UINT16 | 2,
                "dv_type": uctypes.UINT8 | 4,
                "own_addr_type": uctypes.UINT8 | 5,
                "var_len_data":
                (uctypes.ARRAY | 6, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 6)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_START_OBSERVATION_PROC: [
            "GAP_START_OBSERVATION_PROC",
            {
                "scan_interval": uctypes.UINT16 | 0,
                "scan_window": uctypes.UINT16 | 2,
                "scan_type": uctypes.UINT8 | 4,
                "own_address_type": uctypes.UINT8 | 5,
                "filter_duplicates": uctypes.UINT8 | 6
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GAP_GET_BONDED_DEVICES: [
            "GAP_GET_BONDED_DEVICES",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "num_addr": uctypes.UINT8 | 1,
                "dev_list":
                (uctypes.ARRAY | 2, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 2)
            }
        ],
        OCF_GAP_IS_DEVICE_BONDED: [
            "GAP_IS_DEVICE_BONDED",
            {
                "peer_address_type": uctypes.UINT8 | 0,
                "peer_address": (uctypes.ARRAY | 1, uctypes.UINT8 | 6)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_INIT: [
            "GATT_INIT",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_ADD_SERV: [
            "GATT_ADD_SERV",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "handle": uctypes.UINT16 | 1
            }
        ],
        OCF_GATT_INCLUDE_SERV: [
            "GATT_INCLUDE_SERV",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "handle": uctypes.UINT16 | 1
            }
        ],
        OCF_GATT_ADD_CHAR: [
            "GATT_ADD_CHAR",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "handle": uctypes.UINT16 | 1
            }
        ],
        OCF_GATT_ADD_CHAR_DESC: [
            "GATT_ADD_CHAR_DESC",
            None,
            {
                "status": uctypes.UINT8 | 0,
                "handle": uctypes.UINT16 | 1
            }
        ],
        OCF_GATT_UPD_CHAR_VAL: [
            "GATT_UPD_CHAR_VAL",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_DEL_CHAR: [
            "GATT_DEL_CHAR",
            {
                "service_handle": uctypes.UINT16 | 0,
                "char_handle": uctypes.UINT16 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_DEL_SERV: [
            "GATT_DEL_SERV",
            {
                "service_handle": uctypes.UINT16 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_DEL_INC_SERV: [
            "GATT_DEL_INC_SERV",
            {
                "service_handle": uctypes.UINT16 | 0,
                "inc_serv_handle": uctypes.UINT16 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_SET_EVT_MASK: [
            "GATT_SET_EVT_MASK",
            {
                "evt_mask": uctypes.UINT32 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_EXCHANGE_CONFIG: [
            "GATT_EXCHANGE_CONFIG",
            {
                "conn_handle": uctypes.UINT16 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_ATT_FIND_INFO_REQ: [
            "ATT_FIND_INFO_REQ",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "start_handle": uctypes.UINT16 | 2,
                "end_handle": uctypes.UINT16 | 4
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_ATT_FIND_BY_TYPE_VALUE_REQ: [
            "ATT_FIND_BY_TYPE_VALUE_REQ",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "start_handle": uctypes.UINT16 | 2,
                "end_handle": uctypes.UINT16 | 4,
                "uuid": (uctypes.ARRAY | 6, uctypes.UINT8 | 2),
                "attr_val_len": uctypes.UINT8 | 8,
                "attr_val":
                (uctypes.ARRAY | 9, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 9)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_ATT_READ_BY_TYPE_REQ: [
            "ATT_READ_BY_TYPE_REQ",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "start_handle": uctypes.UINT16 | 2,
                "end_handle": uctypes.UINT16 | 4,
                "uuid_type": uctypes.UINT8 | 6,
                "uuid": (uctypes.ARRAY | 7, uctypes.UINT8 | 16)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_ATT_READ_BY_GROUP_TYPE_REQ: [
            "ATT_READ_BY_GROUP_TYPE_REQ",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "start_handle": uctypes.UINT16 | 2,
                "end_handle": uctypes.UINT16 | 4,
                "uuid_type": uctypes.UINT8 | 6,
                "uuid": (uctypes.ARRAY | 7, uctypes.UINT8 | 16)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_ATT_PREPARE_WRITE_REQ: [
            "ATT_PREPARE_WRITE_REQ",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "value_offset": uctypes.UINT16 | 4,
                "attr_val_len": uctypes.UINT8 | 6,
                "attr_val":
                (uctypes.ARRAY | 7, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 7)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_ATT_EXECUTE_WRITE_REQ: [
            "ATT_EXECUTE_WRITE_REQ",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "execute": uctypes.UINT8 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_DISC_ALL_PRIM_SERVICES: [
            "GATT_DISC_ALL_PRIM_SERVICES",
            {
                "conn_handle": uctypes.UINT16 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_DISC_PRIM_SERVICE_BY_UUID: [
            "GATT_DISC_PRIM_SERVICE_BY_UUID",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "uuid_type": uctypes.UINT8 | 2,
                "uuid": (uctypes.ARRAY | 3, uctypes.UINT8 | 16)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_FIND_INCLUDED_SERVICES: [
            "GATT_FIND_INCLUDED_SERVICES",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "start_handle": uctypes.UINT16 | 2,
                "end_handle": uctypes.UINT16 | 4
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_DISC_ALL_CHARAC_OF_SERV: [
            "GATT_DISC_ALL_CHARAC_OF_SERV",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "start_handle": uctypes.UINT16 | 2,
                "end_handle": uctypes.UINT16 | 4
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_DISC_CHARAC_BY_UUID: [
            "GATT_DISC_CHARAC_BY_UUID",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_DISC_ALL_CHARAC_DESCRIPTORS: [
            "GATT_DISC_ALL_CHARAC_DESCRIPTORS",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "start_handle": uctypes.UINT16 | 2,
                "end_handle": uctypes.UINT16 | 4
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_READ_CHARAC_VAL: [
            "GATT_READ_CHARAC_VAL",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_READ_USING_CHARAC_UUID: [
            "GATT_READ_USING_CHARAC_UUID",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "start_handle": uctypes.UINT16 | 2,
                "end_handle": uctypes.UINT16 | 4,
                "uuid_type": uctypes.UINT8 | 6,
                "uuid": (uctypes.ARRAY | 7, uctypes.UINT8 | 16)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_READ_LONG_CHARAC_VAL: [
            "GATT_READ_LONG_CHARAC_VAL",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "val_offset": uctypes.UINT16 | 4
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_READ_MULTIPLE_CHARAC_VAL: [
            "GATT_READ_MULTIPLE_CHARAC_VAL",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "num_handles": uctypes.UINT8 | 2,
                "set_of_handles":
                (uctypes.ARRAY | 3, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 3)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_WRITE_CHAR_VALUE: [
            "GATT_WRITE_CHAR_VALUE",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_WRITE_LONG_CHARAC_VAL: [
            "GATT_WRITE_LONG_CHARAC_VAL",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "val_offset": uctypes.UINT16 | 4,
                "val_len": uctypes.UINT8 | 6,
                "attr_val":
                (uctypes.ARRAY | 7, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 7)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_WRITE_CHARAC_RELIABLE: [
            "GATT_WRITE_CHARAC_RELIABLE",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "val_offset": uctypes.UINT16 | 4,
                "val_len": uctypes.UINT8 | 6,
                "attr_val":
                (uctypes.ARRAY | 7, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 7)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_WRITE_LONG_CHARAC_DESC: [
            "GATT_WRITE_LONG_CHARAC_DESC",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "val_offset": uctypes.UINT16 | 4,
                "val_len": uctypes.UINT8 | 6,
                "attr_val":
                (uctypes.ARRAY | 7, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 7)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_READ_LONG_CHARAC_DESC: [
            "GATT_READ_LONG_CHARAC_DESC",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "val_offset": uctypes.UINT16 | 4
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_WRITE_CHAR_DESC: [
            "GATT_WRITE_CHAR_DESC",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_READ_CHAR_DESC: [
            "GATT_READ_CHAR_DESC",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_WRITE_WITHOUT_RESPONSE: [
            "GATT_WRITE_WITHOUT_RESPONSE",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "val_len": uctypes.UINT8 | 4,
                "attr_val":
                (uctypes.ARRAY | 5, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 5)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_SIGNED_WRITE_WITHOUT_RESPONSE: [
            "GATT_SIGNED_WRITE_WITHOUT_RESPONSE",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "val_len": uctypes.UINT8 | 4,
                "attr_val":
                (uctypes.ARRAY | 5, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 5)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_CONFIRM_INDICATION: [
            "GATT_CONFIRM_INDICATION",
            {
                "conn_handle": uctypes.UINT16 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_WRITE_RESPONSE: [
            "GATT_WRITE_RESPONSE",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_ALLOW_READ: [
            "GATT_ALLOW_READ",
            {
                "conn_handle": uctypes.UINT16 | 0
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_SET_SECURITY_PERMISSION: [
            "GATT_SET_SECURITY_PERMISSION",
            {
                "service_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "security_permission": uctypes.UINT8 | 4
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_SET_DESC_VAL: [
            "GATT_SET_DESC_VAL",
            None,
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_GATT_READ_HANDLE_VALUE: [
            "GATT_READ_HANDLE_VALUE",
            {
                "attr_handle": uctypes.UINT16 | 0
            },
            {
                "status": uctypes.UINT8 | 0,
                "value_len": uctypes.UINT16 | 1,
                "value":
                (uctypes.ARRAY | 3, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 3)
            }
        ],
        OCF_GATT_READ_HANDLE_VALUE_OFFSET: [
            "GATT_READ_HANDLE_VALUE_OFFSET",
            {
                "attr_handle": uctypes.UINT16 | 0,
                "offset": uctypes.UINT8 | 2
            },
            {
                "status": uctypes.UINT8 | 0,
                "value_len": uctypes.UINT16 | 1,
                "value":
                (uctypes.ARRAY | 3, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 3)
            }
        ],
        OCF_GATT_UPD_CHAR_VAL_EXT: [
            "GATT_UPD_CHAR_VAL_EXT",
            {
                "service_handle": uctypes.UINT16 | 0,
                "char_handle": uctypes.UINT16 | 2,
                "update_type": uctypes.UINT8 | 4,
                "char_length": uctypes.UINT16 | 5,
                "value_offset": uctypes.UINT16 | 7,
                "value_length": uctypes.UINT8 | 9,
                "value":
                (uctypes.ARRAY | 10, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 10)
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_L2CAP_CONN_PARAM_UPDATE_REQ: [
            "L2CAP_CONN_PARAM_UPDATE_REQ",
            {
                "conn_handle": uctypes.UINT16 | 0,
                "interval_min": uctypes.UINT16 | 2,
                "interval_max": uctypes.UINT16 | 4,
                "slave_latency": uctypes.UINT16 | 6,
                "timeout_multiplier": uctypes.UINT16 | 8
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ],
        OCF_L2CAP_CONN_PARAM_UPDATE_RESP: [
            "L2CAP_CONN_PARAM_UPDATE_RESP",
            {
                "IDB05A1": {
                    "conn_handle": uctypes.UINT16 | 0,
                    "interval_min": uctypes.UINT16 | 2,
                    "interval_max": uctypes.UINT16 | 4,
                    "slave_latency": uctypes.UINT16 | 6,
                    "timeout_multiplier": uctypes.UINT16 | 8,
                    "min_ce_length": uctypes.UINT16 | 10,
                    "max_ce_length": uctypes.UINT16 | 12,
                    "id": uctypes.UINT8 | 14,
                    "accept": uctypes.UINT8 | 15
                },
                "IDB04A1": {
                    "conn_handle": uctypes.UINT16 | 0,
                    "interval_min": uctypes.UINT16 | 2,
                    "interval_max": uctypes.UINT16 | 4,
                    "slave_latency": uctypes.UINT16 | 6,
                    "timeout_multiplier": uctypes.UINT16 | 8,
                    "id": uctypes.UINT8 | 10,
                    "accept": uctypes.UINT8 | 11
                }
            },
            {
                "status": uctypes.UINT8 | 0
            }
        ]
    }
]
