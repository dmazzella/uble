# -*- coding: utf-8 -*-
# pylint: disable=C0111
import uctypes
from micropython import const

from bluetooth_low_energy.protocols.hci import HCI_MAX_PAYLOAD_SIZE

EVT_BLUE_HAL_INITIALIZED = const(0x0001)
EVT_BLUE_HAL_EVENTS_LOST_IDB05A1 = const(0x0002)
EVT_BLUE_HAL_CRASH_INFO_IDB05A1 = const(0x0003)
EVT_BLUE_GAP_LIMITED_DISCOVERABLE = const(0x0400)
EVT_BLUE_GAP_PAIRING_CMPLT = const(0x0401)
EVT_BLUE_GAP_PASS_KEY_REQUEST = const(0x0402)
EVT_BLUE_GAP_SLAVE_SECURITY_INITIATED = const(0x0404)
EVT_BLUE_GAP_BOND_LOST = const(0x0405)
EVT_BLUE_GAP_DEVICE_FOUND = const(0x0406)
EVT_BLUE_GAP_PROCEDURE_COMPLETE = const(0x0407)
EVT_BLUE_GAP_ADDR_NOT_RESOLVED_IDB05A1 = const(0x0408)
EVT_BLUE_GAP_RECONNECTION_ADDRESS_IDB04A1 = const(0x0408)
EVT_BLUE_GAP_AUTHORIZATION_REQUEST = const(0x0403)
EVT_BLUE_L2CAP_CONN_UPD_RESP = const(0x0800)
EVT_BLUE_L2CAP_PROCEDURE_TIMEOUT = const(0x0801)
EVT_BLUE_L2CAP_CONN_UPD_REQ = const(0x0802)
EVT_BLUE_GATT_ATTRIBUTE_MODIFIED = const(0x0C01)
EVT_BLUE_GATT_PROCEDURE_TIMEOUT = const(0x0C02)
EVT_BLUE_ATT_EXCHANGE_MTU_RESP = const(0x0C03)
EVT_BLUE_ATT_FIND_INFORMATION_RESP = const(0x0C04)
EVT_BLUE_ATT_FIND_BY_TYPE_VAL_RESP = const(0x0C05)
EVT_BLUE_ATT_READ_BY_TYPE_RESP = const(0x0C06)
EVT_BLUE_ATT_READ_RESP = const(0x0C07)
EVT_BLUE_ATT_READ_BLOB_RESP = const(0x0C08)
EVT_BLUE_ATT_READ_MULTIPLE_RESP = const(0x0C09)
EVT_BLUE_ATT_READ_BY_GROUP_TYPE_RESP = const(0x0C0A)
EVT_BLUE_ATT_PREPARE_WRITE_RESP = const(0x0C0C)
EVT_BLUE_ATT_EXEC_WRITE_RESP = const(0x0C0D)
EVT_BLUE_GATT_INDICATION = const(0x0C0E)
EVT_BLUE_GATT_NOTIFICATION = const(0x0C0F)
EVT_BLUE_GATT_PROCEDURE_COMPLETE = const(0x0C10)
EVT_BLUE_GATT_ERROR_RESP = const(0x0C11)
EVT_BLUE_GATT_DISC_READ_CHAR_BY_UUID_RESP = const(0x0C12)
EVT_BLUE_GATT_WRITE_PERMIT_REQ = const(0x0C13)
EVT_BLUE_GATT_READ_PERMIT_REQ = const(0x0C14)
EVT_BLUE_GATT_READ_MULTI_PERMIT_REQ = const(0x0C15)
EVT_BLUE_GATT_TX_POOL_AVAILABLE = const(0x0C16)
EVT_BLUE_GATT_SERVER_CONFIRMATION_EVENT = const(0x0C17)
EVT_BLUE_GATT_PREPARE_WRITE_PERMIT_REQ = const(0x0C18)

# Lost_Events
# Lost events bitmap
# See EVT_BLUE_HAL_EVENTS_LOST.

EVT_DISCONN_COMPLETE_BIT = const(0)
EVT_ENCRYPT_CHANGE_BIT = const(1)
EVT_READ_REMOTE_VERSION_COMPLETE_BIT = const(2)
EVT_CMD_COMPLETE_BIT = const(3)
EVT_CMD_STATUS_BIT = const(4)
EVT_HARDWARE_ERROR_BIT = const(5)
EVT_NUM_COMP_PKTS_BIT = const(6)
EVT_ENCRYPTION_KEY_REFRESH_BIT = const(7)
EVT_BLUE_HAL_INITIALIZED_BIT = const(8)
EVT_BLUE_GAP_SET_LIMITED_DISCOVERABLE_BIT = const(9)
EVT_BLUE_GAP_PAIRING_CMPLT_BIT = const(10)
EVT_BLUE_GAP_PASS_KEY_REQUEST_BIT = const(11)
EVT_BLUE_GAP_AUTHORIZATION_REQUEST_BIT = const(12)
EVT_BLUE_GAP_SECURITY_REQ_INITIATED_BIT = const(13)
EVT_BLUE_GAP_BOND_LOST_BIT = const(14)
EVT_BLUE_GAP_PROCEDURE_COMPLETE_BIT = const(15)
EVT_BLUE_GAP_ADDR_NOT_RESOLVED_BIT = const(16)
EVT_BLUE_L2CAP_CONN_UPDATE_RESP_BIT = const(17)
EVT_BLUE_L2CAP_PROCEDURE_TIMEOUT_BIT = const(18)
EVT_BLUE_L2CAP_CONN_UPDATE_REQ_BIT = const(19)
EVT_BLUE_GATT_ATTRIBUTE_MODIFIED_BIT = const(20)
EVT_BLUE_GATT_PROCEDURE_TIMEOUT_BIT = const(21)
EVT_BLUE_EXCHANGE_MTU_RESP_BIT = const(22)
EVT_BLUE_ATT_FIND_INFORMATION_RESP_BIT = const(23)
EVT_BLUE_ATT_FIND_BY_TYPE_VAL_RESP_BIT = const(24)
EVT_BLUE_ATT_READ_BY_TYPE_RESP_BIT = const(25)
EVT_BLUE_ATT_READ_RESP_BIT = const(26)
EVT_BLUE_ATT_READ_BLOB_RESP_BIT = const(27)
EVT_BLUE_ATT_READ_MULTIPLE_RESP_BIT = const(28)
EVT_BLUE_ATT_READ_BY_GROUP_RESP_BIT = const(29)
EVT_BLUE_ATT_WRITE_RESP_BIT = const(30)
EVT_BLUE_ATT_PREPARE_WRITE_RESP_BIT = const(31)
EVT_BLUE_ATT_EXEC_WRITE_RESP_BIT = const(32)
EVT_BLUE_GATT_INDICATION_BIT = const(33)
EVT_BLUE_GATT_NOTIFICATION_BIT = const(34)
EVT_BLUE_GATT_PROCEDURE_COMPLETE_BIT = const(35)
EVT_BLUE_GATT_ERROR_RESP_BIT = const(36)
EVT_BLUE_GATT_DISC_READ_CHARAC_BY_UUID_RESP_BIT = const(37)
EVT_BLUE_GATT_WRITE_PERMIT_REQ_BIT = const(38)
EVT_BLUE_GATT_READ_PERMIT_REQ_BIT = const(39)
EVT_BLUE_GATT_READ_MULTI_PERMIT_REQ_BIT = const(40)
EVT_BLUE_GATT_TX_POOL_AVAILABLE_BIT = const(41)
EVT_BLUE_GATT_SERVER_RX_CONFIRMATION_BIT = const(42)
EVT_BLUE_GATT_PREPARE_WRITE_PERMIT_REQ_BIT = const(43)
EVT_LL_CONNECTION_COMPLETE_BIT = const(44)
EVT_LL_ADVERTISING_REPORT_BIT = const(45)
EVT_LL_CONNECTION_UPDATE_COMPLETE_BIT = const(46)
EVT_LL_READ_REMOTE_USED_FEATURES_BIT = const(47)
EVT_LL_LTK_REQUEST_BIT = const(48)

HCI_VENDOR_EVENTS = {
    EVT_BLUE_HAL_INITIALIZED: [
        "BLUE_HAL_INITIALIZED",
        {
            "reason_code": uctypes.UINT8 | 0
        }
    ],
    EVT_BLUE_HAL_EVENTS_LOST_IDB05A1: [
        "BLUE_HAL_EVENTS_LOST_IDB05A1",
        {
            "lost_events": (uctypes.ARRAY | 0, uctypes.UINT8 | 8)
        }
    ],
    EVT_BLUE_HAL_CRASH_INFO_IDB05A1: [
        "BLUE_HAL_CRASH_INFO_IDB05A1",
        {
            "crash_type": uctypes.UINT8 | 0,
            "sp": uctypes.UINT32 | 1,
            "sp1": uctypes.UINT32 | 5,
            "r0": uctypes.UINT32 | 9,
            "r1": uctypes.UINT32 | 13,
            "r2": uctypes.UINT32 | 17,
            "r3": uctypes.UINT32 | 21,
            "r12": uctypes.UINT32 | 25,
            "lr": uctypes.UINT32 | 29,
            "pc": uctypes.UINT32 | 33,
            "xpsr": uctypes.UINT32 | 37,
            "debug_data_len": uctypes.UINT8 | 41,
            "debug_data":
            (uctypes.ARRAY | 46, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 46)
        }
    ],
    EVT_BLUE_GAP_LIMITED_DISCOVERABLE: [
        "BLUE_GAP_LIMITED_DISCOVERABLE",
        None
    ],
    EVT_BLUE_GAP_PAIRING_CMPLT: [
        "BLUE_GAP_PAIRING_CMPLT",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "status": uctypes.UINT8 | 2
        }
    ],
    EVT_BLUE_GAP_PASS_KEY_REQUEST: [
        "BLUE_GAP_PASS_KEY_REQUEST",
        {
            "conn_handle": uctypes.UINT16 | 0
        }
    ],
    EVT_BLUE_GAP_SLAVE_SECURITY_INITIATED: [
        "BLUE_GAP_SLAVE_SECURITY_INITIATED",
        None
    ],
    EVT_BLUE_GAP_BOND_LOST: [
        "BLUE_GAP_BOND_LOST",
        None
    ],
    EVT_BLUE_GAP_DEVICE_FOUND: [
        "BLUE_GAP_DEVICE_FOUND",
        {
            "evt_type": uctypes.UINT8 | 0,
            "bdaddr_type": uctypes.UINT8 | 1,
            "bdaddr": (uctypes.ARRAY | 2, uctypes.UINT8 | 6),
            "data_length": uctypes.UINT8 | 8,
            "data_rssi":
            (uctypes.ARRAY | 9, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 9)
        }
    ],
    EVT_BLUE_GAP_PROCEDURE_COMPLETE: [
        "BLUE_GAP_PROCEDURE_COMPLETE",
        {
            "procedure_code": uctypes.UINT8 | 0,
            "status": uctypes.UINT8 | 1,
            "data":
            (uctypes.ARRAY | 2, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 2)
        }
    ],
    EVT_BLUE_GAP_ADDR_NOT_RESOLVED_IDB05A1: [
        "BLUE_GAP_ADDR_NOT_RESOLVED_IDB05A1",
        {
            "conn_handle": uctypes.UINT16 | 0
        }
    ],
    EVT_BLUE_GAP_RECONNECTION_ADDRESS_IDB04A1: [
        "BLUE_GAP_RECONNECTION_ADDRESS_IDB04A1",
        {
            "reconnection_address": (uctypes.ARRAY | 0, uctypes.UINT8 | 6)
        }
    ],
    EVT_BLUE_GAP_AUTHORIZATION_REQUEST: [
        "BLUE_GAP_AUTHORIZATION_REQUEST",
        {
            "conn_handle": uctypes.UINT16 | 0
        }
    ],
    EVT_BLUE_L2CAP_CONN_UPD_RESP: [
        "BLUE_L2CAP_CONN_UPD_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "code": uctypes.UINT8 | 3,
            "identifier": uctypes.UINT8 | 4,
            "l2cap_length": uctypes.UINT16 | 5,
            "result": uctypes.UINT16 | 7
        }
    ],
    EVT_BLUE_L2CAP_PROCEDURE_TIMEOUT: [
        "BLUE_L2CAP_PROCEDURE_TIMEOUT",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2
        }
    ],
    EVT_BLUE_L2CAP_CONN_UPD_REQ: [
        "BLUE_L2CAP_CONN_UPD_REQ",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "identifier": uctypes.UINT8 | 3,
            "l2cap_length": uctypes.UINT16 | 4,
            "interval_min": uctypes.UINT16 | 6,
            "interval_max": uctypes.UINT16 | 8,
            "slave_latency": uctypes.UINT16 | 10,
            "timeout_mult": uctypes.UINT16 | 12
        }
    ],
    EVT_BLUE_GATT_ATTRIBUTE_MODIFIED: [
        "BLUE_GATT_ATTRIBUTE_MODIFIED",
        {
            "IDB05A1": {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "data_length": uctypes.UINT8 | 4,
                "offset": uctypes.UINT16 | 5,
                "att_data":
                (uctypes.ARRAY | 7, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 7)
            },
            "IDB04A1": {
                "conn_handle": uctypes.UINT16 | 0,
                "attr_handle": uctypes.UINT16 | 2,
                "data_length": uctypes.UINT8 | 4,
                "att_data":
                (uctypes.ARRAY | 5, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 5)
            }
        }
    ],
    EVT_BLUE_GATT_PROCEDURE_TIMEOUT: [
        "BLUE_GATT_PROCEDURE_TIMEOUT",
        {
            "conn_handle": uctypes.UINT16 | 0
        }
    ],
    EVT_BLUE_ATT_EXCHANGE_MTU_RESP: [
        "BLUE_ATT_EXCHANGE_MTU_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "server_rx_mtu": uctypes.UINT16 | 3
        }
    ],
    EVT_BLUE_ATT_FIND_INFORMATION_RESP: [
        "BLUE_ATT_FIND_INFORMATION_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "format": uctypes.UINT8 | 3,
            "handle_uuid_pair":
            (uctypes.ARRAY | 4, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 4)
        }
    ],
    EVT_BLUE_ATT_FIND_BY_TYPE_VAL_RESP: [
        "BLUE_ATT_FIND_BY_TYPE_VAL_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "handles_info_list":
            (uctypes.ARRAY | 3, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 3)
        }
    ],
    EVT_BLUE_ATT_READ_BY_TYPE_RESP: [
        "BLUE_ATT_READ_BY_TYPE_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "handle_value_pair_length": uctypes.UINT8 | 3,
            "handle_value_pair":
            (uctypes.ARRAY | 4, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 4)
        }
    ],
    EVT_BLUE_ATT_READ_RESP: [
        "BLUE_ATT_READ_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "attribute_value":
            (uctypes.ARRAY | 3, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 3)
        }
    ],
    EVT_BLUE_ATT_READ_BLOB_RESP: [
        "BLUE_ATT_READ_BLOB_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "part_attribute_value":
            (uctypes.ARRAY | 3, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 3)
        }
    ],
    EVT_BLUE_ATT_READ_MULTIPLE_RESP: [
        "BLUE_ATT_READ_MULTIPLE_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "set_of_values":
            (uctypes.ARRAY | 3, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 3)
        }
    ],
    EVT_BLUE_ATT_READ_BY_GROUP_TYPE_RESP: [
        "BLUE_ATT_READ_BY_GROUP_TYPE_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "attribute_data_length": uctypes.UINT8 | 3,
            "attribute_data_list":
            (uctypes.ARRAY | 4, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 4)
        }
    ],
    EVT_BLUE_ATT_PREPARE_WRITE_RESP: [
        "BLUE_ATT_PREPARE_WRITE_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "attribute_handle": uctypes.UINT16 | 3,
            "offset": uctypes.UINT16 | 5,
            "part_attr_value":
            (uctypes.ARRAY | 7, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 7)
        }
    ],
    EVT_BLUE_ATT_EXEC_WRITE_RESP: [
        "BLUE_ATT_EXEC_WRITE_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
        }
    ],
    EVT_BLUE_GATT_INDICATION: [
        "BLUE_GATT_INDICATION",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "attr_handle": uctypes.UINT16 | 3,
            "attr_value":
            (uctypes.ARRAY | 5, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 5)
        }
    ],
    EVT_BLUE_GATT_NOTIFICATION: [
        "BLUE_GATT_NOTIFICATION",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "attr_handle": uctypes.UINT16 | 3,
            "attr_value":
            (uctypes.ARRAY | 5, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 5)
        }
    ],
    EVT_BLUE_GATT_PROCEDURE_COMPLETE: [
        "BLUE_GATT_PROCEDURE_COMPLETE",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "data_length": uctypes.UINT8 | 2,
            "error_code": uctypes.UINT8 | 3
        }
    ],
    EVT_BLUE_GATT_ERROR_RESP: [
        "BLUE_GATT_ERROR_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "req_opcode": uctypes.UINT8 | 3,
            "attr_handle": uctypes.UINT16 | 4,
            "error_code":  uctypes.UINT8 | 6
        }
    ],
    EVT_BLUE_GATT_DISC_READ_CHAR_BY_UUID_RESP: [
        "BLUE_GATT_DISC_READ_CHAR_BY_UUID_RESP",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "event_data_length": uctypes.UINT8 | 2,
            "attr_handle": uctypes.UINT16 | 3,
            "attr_value":
            (uctypes.ARRAY | 5, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 5)
        }
    ],
    EVT_BLUE_GATT_WRITE_PERMIT_REQ: [
        "BLUE_GATT_WRITE_PERMIT_REQ",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "attr_handle": uctypes.UINT16 | 2,
            "data_length": uctypes.UINT8 | 4,
            "data_buffer":
            (uctypes.ARRAY | 5, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 5)
        }
    ],
    EVT_BLUE_GATT_READ_PERMIT_REQ: [
        "BLUE_GATT_READ_PERMIT_REQ",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "attr_handle": uctypes.UINT16 | 2,
            "data_length": uctypes.UINT8 | 4,
            "offset": uctypes.UINT16 | 5
        }
    ],
    EVT_BLUE_GATT_READ_MULTI_PERMIT_REQ: [
        "BLUE_GATT_READ_MULTI_PERMIT_REQ",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "data_length": uctypes.UINT8 | 2,
            "data":
            (uctypes.ARRAY | 3, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 3)
        }
    ],
    EVT_BLUE_GATT_TX_POOL_AVAILABLE: [
        "BLUE_GATT_TX_POOL_AVAILABLE",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "available_buffers": uctypes.UINT16 | 2
        }
    ],
    EVT_BLUE_GATT_SERVER_CONFIRMATION_EVENT: [
        "BLUE_GATT_SERVER_CONFIRMATION_EVENT",
        {
            "conn_handle": uctypes.UINT16 | 0,
        }
    ],
    EVT_BLUE_GATT_PREPARE_WRITE_PERMIT_REQ: [
        "BLUE_GATT_PREPARE_WRITE_PERMIT_REQ",
        {
            "conn_handle": uctypes.UINT16 | 0,
            "attr_handle": uctypes.UINT16 | 2,
            "offset": uctypes.UINT16 | 4,
            "data_length": uctypes.UINT8 | 6,
            "data":
            (uctypes.ARRAY | 7, uctypes.UINT8 | HCI_MAX_PAYLOAD_SIZE - 7)
        }
    ]
}
