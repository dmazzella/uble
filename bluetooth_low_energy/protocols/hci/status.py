# -*- coding: utf-8 -*-
# pylint: disable=C0111
from micropython import const

# Error Codes as specified by the specification
# according to the spec the error codes range
# from 0x00 to 0x3F


# Standard error codes
# See Core v 4.1, Vol. 2, part D.

ERR_CMD_SUCCESS = const(0x00)
BLE_STATUS_SUCCESS = const(0x00)
ERR_UNKNOWN_HCI_COMMAND = const(0x01)
ERR_UNKNOWN_CONN_IDENTIFIER = const(0x02)
ERR_AUTH_FAILURE = const(0x05)
ERR_PIN_OR_KEY_MISSING = const(0x06)
ERR_MEM_CAPACITY_EXCEEDED = const(0x07)
ERR_CONNECTION_TIMEOUT = const(0x08)
ERR_COMMAND_DISALLOWED = const(0x0C)
ERR_UNSUPPORTED_FEATURE = const(0x11)
ERR_INVALID_HCI_CMD_PARAMS = const(0x12)
ERR_RMT_USR_TERM_CONN = const(0x13)
ERR_RMT_DEV_TERM_CONN_LOW_RESRCES = const(0x14)
ERR_RMT_DEV_TERM_CONN_POWER_OFF = const(0x15)
ERR_LOCAL_HOST_TERM_CONN = const(0x16)
ERR_UNSUPP_RMT_FEATURE = const(0x1A)
ERR_INVALID_LMP_PARAM = const(0x1E)
ERR_UNSPECIFIED_ERROR = const(0x1F)
ERR_LL_RESP_TIMEOUT = const(0x22)
ERR_LMP_PDU_NOT_ALLOWED = const(0x24)
ERR_INSTANT_PASSED = const(0x28)
ERR_PAIR_UNIT_KEY_NOT_SUPP = const(0x29)
ERR_CONTROLLER_BUSY = const(0x3A)
ERR_DIRECTED_ADV_TIMEOUT = const(0x3C)
ERR_CONN_END_WITH_MIC_FAILURE = const(0x3D)
ERR_CONN_FAILED_TO_ESTABLISH = const(0x3E)
