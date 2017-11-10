# -*- coding: utf-8 -*-
from micropython import const

# Bluetooth Status/Error Codes

# Vendor-specific error codes
# Error codes defined by ST related to BlueNRG stack

# The command cannot be executed due to the current state of the device.
BLE_STATUS_FAILED = const(0x41)

# Some parameters are invalid.
BLE_STATUS_INVALID_PARAMS = const(0x42)

# It is not allowed to start the procedure (e.g. another the procedure is
# ongoing or cannot be started on the given handle).
BLE_STATUS_NOT_ALLOWED = const(0x46)

# Unexpected error.
BLE_STATUS_ERROR = const(0x47)
BLE_STATUS_ADDR_NOT_RESOLVED = const(0x48)

FLASH_READ_FAILED = const(0x49)
FLASH_WRITE_FAILED = const(0x4A)
FLASH_ERASE_FAILED = const(0x4B)

BLE_STATUS_INVALID_CID = const(0x50)

TIMER_NOT_VALID_LAYER = const(0x54)
TIMER_INSUFFICIENT_RESOURCES = const(0x55)

BLE_STATUS_CSRK_NOT_FOUND = const(0x5A)
BLE_STATUS_IRK_NOT_FOUND = const(0x5B)
BLE_STATUS_DEV_NOT_FOUND_IN_DB = const(0x5C)
BLE_STATUS_SEC_DB_FULL = const(0x5D)
BLE_STATUS_DEV_NOT_BONDED = const(0x5E)
BLE_STATUS_DEV_IN_BLACKLIST = const(0x5F)

BLE_STATUS_INVALID_HANDLE = const(0x60)
BLE_STATUS_INVALID_PARAMETER = const(0x61)
BLE_STATUS_OUT_OF_HANDLE = const(0x62)
BLE_STATUS_INVALID_OPERATION = const(0x63)
BLE_STATUS_INSUFFICIENT_RESOURCES = const(0x64)
BLE_INSUFFICIENT_ENC_KEYSIZE = const(0x65)
BLE_STATUS_CHARAC_ALREADY_EXISTS = const(0x66)

# Returned when no valid slots are available
# (e.g. when there are no available state machines).
BLE_STATUS_NO_VALID_SLOT = const(0x82)

# Returned when a scan window shorter than minimum allowed value has been
# requested (i.e. 2ms)
BLE_STATUS_SCAN_WINDOW_SHORT = const(0x83)

# Returned when the maximum requested interval to be allocated is shorter then
# the current anchor period and there is no submultiple for the current anchor
# period that is between the minimum and the maximum requested intervals.
BLE_STATUS_NEW_INTERVAL_FAILED = const(0x84)

# Returned when the maximum requested interval to be allocated is greater than
# the current anchor period and there is no multiple of the anchor period that
# is between the minimum and the maximum requested intervals.
BLE_STATUS_INTERVAL_TOO_LARGE = const(0x85)

# Returned when the current anchor period or a new one can be found that is
# compatible to the interval range requested by the new slot but the maximum
# available length that can be allocated is less than the minimum requested
# slot length.
BLE_STATUS_LENGTH_FAILED = const(0x86)

# Library Error Codes
# Error codes defined by ST related to MCU library.
BLE_STATUS_TIMEOUT = const(0xFF)
BLE_STATUS_PROFILE_ALREADY_INITIALIZED = const(0xF0)
BLE_STATUS_NULL_PARAM = const(0xF1)

# Hardware error event codes
# See EVT_HARDWARE_ERROR.

# Error on the SPI bus has been detected, most likely caused by incorrect SPI
# configuration on the external micro-controller.
SPI_FRAMING_ERROR = const(0)

# Caused by a slow crystal startup and they are an indication that the
# HS_STARTUP_TIME in the device configuration needs to be tuned.
# After this event is recommended to hardware reset the device.
RADIO_STATE_ERROR = const(1)

# Caused by a slow crystal startup and they are an indication that the
# HS_STARTUP_TIME in the device configuration needs to be tuned.
# After this event is recommended to hardware reset the device.
TIMER_OVERRUN_ERROR = const(2)
