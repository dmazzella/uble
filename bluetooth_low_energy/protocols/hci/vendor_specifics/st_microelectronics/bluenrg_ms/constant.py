# -*- coding: utf-8 -*-
from micropython import const

# Reset Reasons. EVT_BLUE_HAL_INITIALIZED.
# Normal startup.
RESET_NORMAL = const(1)
# Updater mode entered with ACI command
RESET_UPDATER_ACI = const(2)
# Updater mode entered due to a bad BLUE flag
RESET_UPDATER_BAD_FLAG = const(3)
# Updater mode entered with IRQ pin
RESET_UPDATER_PIN = const(4)
# Reset caused by watchdog
RESET_WATCHDOG = const(5)
# Reset due to lockup
RESET_LOCKUP = const(6)
# Brownout reset
RESET_BROWNOUT = const(7)
# Reset caused by a crash (NMI or Hard Fault)
RESET_CRASH = const(8)
# Reset caused by an ECC error
RESET_ECC_ERR = const(9)

# Config_vals Offsets and lengths for configuration values
# See aci_hal_write_config_data().

#Configuration values.

# Bluetooth public address
CONFIG_DATA_PUBADDR_OFFSET = const(0x00)
# DIV used to derive CSRK
CONFIG_DATA_DIV_OFFSET = const(0x06)
# Encryption root key used to derive LTK and CSRK
CONFIG_DATA_ER_OFFSET = const(0x08)
# Identity root key used to derive LTK and CSRK
CONFIG_DATA_IR_OFFSET = const(0x18)
# Switch on/off Link Layer only mode. Set to 1 to disable Host.
# It can be written only if aci_hal_write_config_data()
# is the first command after reset.
CONFIG_DATA_LL_WITHOUT_HOST = const(0x2C)
# Stored static random address. Read-only.
CONFIG_DATA_RANDOM_ADDRESS = const(0x80)

# Select the BlueNRG mode configurations.
# - Mode 1: slave or master, 1 connection, RAM1 only (small GATT DB)
# - Mode 2: slave or master, 1 connection, RAM1 and RAM2 (large GATT DB)
# - Mode 3: master/slave, 8 connections, RAM1 and RAM2.
# - Mode 4: master/slave, 4 connections, RAM1 and RAM2 simultaneous scanning and advertising.
CONFIG_DATA_MODE_OFFSET = const(0x2D)

# Set to 1 to disable watchdog. It is enabled by default.
CONFIG_DATA_WATCHDOG_DISABLE = const(0x2F)

# Length for configuration values.
# See aci_hal_write_config_data().

CONFIG_DATA_PUBADDR_LEN = const(6)
CONFIG_DATA_DIV_LEN = const(2)
CONFIG_DATA_ER_LEN = const(16)
CONFIG_DATA_IR_LEN = const(16)
CONFIG_DATA_LL_WITHOUT_HOST_LEN = const(1)
CONFIG_DATA_MODE_LEN = const(1)
CONFIG_DATA_WATCHDOG_DISABLE_LEN = const(1)

# Link_Status
# Status of the link
# See aci_hal_get_link_status().

STATUS_IDLE = const(0)
STATUS_ADVERTISING = const(1)
STATUS_CONNECTED_AS_SLAVE = const(2)
STATUS_SCANNING = const(3)
STATUS_CONNECTED_AS_MASTER = const(5)
STATUS_TX_TEST = const(6)
STATUS_RX_TEST = const(7)

# GAP UUIDs

GAP_SERVICE_UUID = const(0x1800)
DEVICE_NAME_UUID = const(0x2A00)
APPEARANCE_UUID = const(0x2A01)
PERIPHERAL_PRIVACY_FLAG_UUID = const(0x2A02)
RECONNECTION_ADDR_UUID = const(0x2A03)
PERIPHERAL_PREFERRED_CONN_PARAMS_UUID = const(0x2A04)

# Characteristic value lengths

DEVICE_NAME_CHARACTERISTIC_LEN = const(8)
APPEARANCE_CHARACTERISTIC_LEN = const(2)
PERIPHERAL_PRIVACY_CHARACTERISTIC_LEN = const(1)
RECONNECTION_ADDR_CHARACTERISTIC_LEN = const(6)
PERIPHERAL_PREF_CONN_PARAMS_CHARACTERISTIC_LEN = const(8)

# AD types for adv data and scan response data

# FLAGS AD type
AD_TYPE_FLAGS = const(0x01)

# Flags AD Type bits
FLAG_BIT_LE_LIMITED_DISCOVERABLE_MODE = const(0x01)
FLAG_BIT_LE_GENERAL_DISCOVERABLE_MODE = const(0x02)
FLAG_BIT_BR_EDR_NOT_SUPPORTED = const(0x04)
FLAG_BIT_LE_BR_EDR_CONTROLLER = const(0x08)
FLAG_BIT_LE_BR_EDR_HOST = const(0x10)


# Service UUID AD types
AD_TYPE_16_BIT_SERV_UUID = const(0x02)
AD_TYPE_16_BIT_SERV_UUID_CMPLT_LIST = const(0x03)
AD_TYPE_32_BIT_SERV_UUID = const(0x04)
AD_TYPE_32_BIT_SERV_UUID_CMPLT_LIST = const(0x05)
AD_TYPE_128_BIT_SERV_UUID = const(0x06)
AD_TYPE_128_BIT_SERV_UUID_CMPLT_LIST = const(0x07)

# Local name AD types
AD_TYPE_SHORTENED_LOCAL_NAME = const(0x08)
AD_TYPE_COMPLETE_LOCAL_NAME = const(0x09)

# TX power level AD type
AD_TYPE_TX_POWER_LEVEL = const(0x0A)

# Class of device
AD_TYPE_CLASS_OF_DEVICE = const(0x0D)

# Security manager TK value AD type
AD_TYPE_SEC_MGR_TK_VALUE = const(0x10)

# Security manager OOB flags
AD_TYPE_SEC_MGR_OOB_FLAGS = const(0x11)

# Slave connection interval AD type
AD_TYPE_SLAVE_CONN_INTERVAL = const(0x12)

# Service solicitation UUID list AD types
AD_TYPE_SERV_SOLICIT_16_BIT_UUID_LIST = const(0x14)
AD_TYPE_SERV_SOLICIT_32_BIT_UUID_LIST = const(0x1F)
AD_TYPE_SERV_SOLICIT_128_BIT_UUID_LIST = const(0x15)

# Service data AD type
AD_TYPE_SERVICE_DATA = const(0x16)

# Manufaturer specific data AD type
AD_TYPE_MANUFACTURER_SPECIFIC_DATA = const(0xFF)


MAX_ADV_DATA_LEN = const(31)

DEVICE_NAME_LEN = const(7)
BD_ADDR_SIZE = const(6)

# Privacy flag values
PRIVACY_ENABLED = const(0x01)
PRIVACY_DISABLED = const(0x00)

# Intervals
# 250ms
DIR_CONN_ADV_INT_MIN = const(0x190)
# 500ms
DIR_CONN_ADV_INT_MAX = const(0x320)
# 1.28s
UNDIR_CONN_ADV_INT_MIN = const(0x800)
# 2.56s
UNDIR_CONN_ADV_INT_MAX = const(0x1000)
# 250ms
LIM_DISC_ADV_INT_MIN = const(0x190)
# 500ms
LIM_DISC_ADV_INT_MAX = const(0x320)
# 1.28s
GEN_DISC_ADV_INT_MIN = const(0x800)
# 2.56s
GEN_DISC_ADV_INT_MAX = const(0x1000)

# Timeout values
# 180 seconds. according to the errata published
LIM_DISC_MODE_TIMEOUT = const(180000)
# 15 minutes
PRIVATE_ADDR_INT_TIMEOUT = const(900000)

# GAP Roles
GAP_PERIPHERAL_ROLE_IDB05A1 = const(0x01)
GAP_BROADCASTER_ROLE_IDB05A1 = const(0x02)
GAP_CENTRAL_ROLE_IDB05A1 = const(0x04)
GAP_OBSERVER_ROLE_IDB05A1 = const(0x08)

GAP_PERIPHERAL_ROLE_IDB04A1 = const(0x01)
GAP_BROADCASTER_ROLE_IDB04A1 = const(0x02)
GAP_CENTRAL_ROLE_IDB04A1 = const(0x03)
GAP_OBSERVER_ROLE_IDB04A1 = const(0x04)

# GAP procedure codes
# Procedure codes for EVT_BLUE_GAP_PROCEDURE_COMPLETE event
# and aci_gap_terminate_gap_procedure() command.


GAP_LIMITED_DISCOVERY_PROC = const(0x01)
GAP_GENERAL_DISCOVERY_PROC = const(0x02)
GAP_NAME_DISCOVERY_PROC = const(0x04)
GAP_AUTO_CONNECTION_ESTABLISHMENT_PROC = const(0x08)
GAP_GENERAL_CONNECTION_ESTABLISHMENT_PROC = const(0x10)
GAP_SELECTIVE_CONNECTION_ESTABLISHMENT_PROC = const(0x20)
GAP_DIRECT_CONNECTION_ESTABLISHMENT_PROC = const(0x40)

GAP_OBSERVATION_PROC_IDB05A1 = const(0x80)

# Advertising filter
# Process scan and connection requests from all devices
# (i.e., the White List is not in use)
NO_WHITE_LIST_USE = const(0x00)
# Process connection requests from all devices and only scan requests from
# devices that are in the White List
WHITE_LIST_FOR_ONLY_SCAN = const(0x01)
# Process scan requests from all devices and only connection requests from
# devices that are in the White List
WHITE_LIST_FOR_ONLY_CONN = const(0x02)
# Process scan and connection requests only from devices in the White List.
WHITE_LIST_FOR_ALL = const(0x03)

# Bluetooth address types
PUBLIC_ADDR = const(0)
RANDOM_ADDR = const(1)
STATIC_RANDOM_ADDR = const(1)
RESOLVABLE_PRIVATE_ADDR = const(2)
NON_RESOLVABLE_PRIVATE_ADDR = const(3)

# Directed advertising types
HIGH_DUTY_CYCLE_DIRECTED_ADV = const(1)
LOW_DUTY_CYCLE_DIRECTED_ADV = const(4)

# Advertising type
# undirected scannable and connectable
ADV_IND = const(0x00)
# directed non scannable
ADV_DIRECT_IND = const(0x01)
# scannable non connectable
ADV_SCAN_IND = const(0x02)
# non-connectable and no scan response
ADV_NONCONN_IND = const(0x03)
# scan response
SCAN_RSP = const(0x04)
# 0x05-0xFF RESERVED

# Advertising ranges
# Lowest allowed interval value for connectable types(20ms)..multiple of 625us
ADV_INTERVAL_LOWEST_CONN = const(0x0020)
# Highest allowed interval value (10.24s)..multiple of 625us.
ADV_INTERVAL_HIGHEST = const(0x4000)
#lowest allowed interval value for non connectable types (100ms)..multiple of 625us.
ADV_INTERVAL_LOWEST_NONCONN = const(0x00a0)

# Advertising channels
ADV_CH_37 = const(0x01)
ADV_CH_38 = const(0x02)
ADV_CH_39 = const(0x04)

# Scan_types Scan types
PASSIVE_SCAN = const(0)
ACTIVE_SCAN = const(1)

# Well-Known UUIDs
PRIMARY_SERVICE_UUID = const(0x2800)
SECONDARY_SERVICE_UUID = const(0x2801)
INCLUDE_SERVICE_UUID = const(0x2802)
CHARACTERISTIC_UUID = const(0x2803)
CHAR_EXTENDED_PROP_DESC_UUID = const(0x2900)
CHAR_USER_DESC_UUID = const(0x2901)
CHAR_CLIENT_CONFIG_DESC_UUID = const(0x2902)
CHAR_SERVER_CONFIG_DESC_UUID = const(0x2903)
CHAR_FORMAT_DESC_UUID = const(0x2904)
CHAR_AGGR_FMT_DESC_UUID = const(0x2905)
GATT_SERVICE_UUID = const(0x1801)
SERVICE_CHANGED_UUID = const(0x2A05)


# Access permissions for an attribute
ATTR_NO_ACCESS = const(0x00)
ATTR_ACCESS_READ_ONLY = const(0x01)
ATTR_ACCESS_WRITE_REQ_ONLY = const(0x02)
ATTR_ACCESS_READ_WRITE = const(0x03)
ATTR_ACCESS_WRITE_WITHOUT_RESPONSE = const(0x04)
ATTR_ACCESS_SIGNED_WRITE_ALLOWED = const(0x08)


# Allows all write procedures
ATTR_ACCESS_WRITE_ANY = const(0x0E)


# Characteristic properties
CHAR_PROP_BROADCAST = const(0x01)
CHAR_PROP_READ = const(0x02)
CHAR_PROP_WRITE_WITHOUT_RESP = const(0x04)
CHAR_PROP_WRITE = const(0x08)
CHAR_PROP_NOTIFY = const(0x10)
CHAR_PROP_INDICATE = const(0x20)
CHAR_PROP_SIGNED_WRITE = const(0x40)
CHAR_PROP_EXT = const(0x80)


# Security permissions for an attribute
# No security.
ATTR_PERMISSION_NONE = const(0x00)
# Need authentication to read
ATTR_PERMISSION_AUTHEN_READ = const(0x01)
# Need authorization to read
ATTR_PERMISSION_AUTHOR_READ = const(0x02)
# Link must be encrypted to read
ATTR_PERMISSION_ENCRY_READ = const(0x04)
# Need authentication to write
ATTR_PERMISSION_AUTHEN_WRITE = const(0x08)
# Need authorization to write
ATTR_PERMISSION_AUTHOR_WRITE = const(0x10)
# Link must be encrypted for write
ATTR_PERMISSION_ENCRY_WRITE = const(0x20)


# Type of UUID (16 bit or 128 bit).
UUID_TYPE_16 = const(0x01)
UUID_TYPE_128 = const(0x02)


# Type of service (primary or secondary)
PRIMARY_SERVICE = const(0x01)
SECONDARY_SERVICE = const(0x02)


# Gatt Event Mask. Type of event generated by GATT server
# Do not notify events.
GATT_DONT_NOTIFY_EVENTS = const(0x00)
# The application will be notified when a client writes to this attribute.
# An EVT_BLUE_GATT_ATTRIBUTE_MODIFIED will be issued.
GATT_NOTIFY_ATTRIBUTE_WRITE = const(0x01)
# The application will be notified when a write request, a write cmd or a signed
# write cmd are received by the server for this attribute.
# An EVT_BLUE_GATT_WRITE_PERMIT_REQ will be issued.
GATT_NOTIFY_WRITE_REQ_AND_WAIT_FOR_APPL_RESP = const(0x02)
# The application will be notified when a read request of any type is received
# for this attribute. An EVT_BLUE_GATT_READ_PERMIT_REQ will be issued.
GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP = const(0x04)


# Type of characteristic length. See aci_gatt_add_char()
CHAR_VALUE_LEN_CONSTANT = const(0x00)
CHAR_VALUE_LEN_VARIABLE = const(0x01)


# Encryption key size
MIN_ENCRY_KEY_SIZE = const(7)
MAX_ENCRY_KEY_SIZE = const(0x10)

# Format
FORMAT_UINT8 = const(0x04)
FORMAT_UINT16 = const(0x06)
FORMAT_SINT16 = const(0x0E)
FORMAT_SINT24 = const(0x0F)
# Unit
UNIT_UNITLESS = const(0x2700)
UNIT_TEMP_CELSIUS = const(0x272F)
UNIT_PRESSURE_BAR = const(0x2780)

# ATT MTU size
ATT_MTU = const(23)

NOTIFICATION = const(1)
INDICATION = const(2)

# IO capabilities
O_CAP_DISPLAY_ONLY = const(0x00)
O_CAP_DISPLAY_YES_NO = const(0x01)
O_CAP_KEYBOARD_ONLY = const(0x02)
O_CAP_NO_INPUT_NO_OUTPUT = const(0x03)
O_CAP_KEYBOARD_DISPLAY = const(0x04)

# Authentication requirements
BONDING = const(0x01)
NO_BONDING = const(0x00)

# MITM protection requirements
MITM_PROTECTION_NOT_REQUIRED = const(0x00)
MITM_PROTECTION_REQUIRED = const(0x01)

# OOB_Data: Out-Of-Band data
OOB_AUTH_DATA_ABSENT = const(0x00)
OOB_AUTH_DATA_PRESENT = const(0x01)

# Authorization requirements
AUTHORIZATION_NOT_REQUIRED = const(0x00)
AUTHORIZATION_REQUIRED = const(0x01)

# Connection authorization
CONNECTION_AUTHORIZED = const(0x01)
CONNECTION_REJECTED = const(0x02)

# Use fixed pin
USE_FIXED_PIN_FOR_PAIRING = const(0x00)
DONOT_USE_FIXED_PIN_FOR_PAIRING = const(0x01)

# Link security status
SM_LINK_AUTHENTICATED = const(0x01)
SM_LINK_AUTHORIZED = const(0x02)
SM_LINK_ENCRYPTED = const(0x04)

# SMP pairing failed reason codes
PASSKEY_ENTRY_FAILED = const(0x01)
OOB_NOT_AVAILABLE = const(0x02)
AUTH_REQ_CANNOT_BE_MET = const(0x03)
CONFIRM_VALUE_FAILED = const(0x04)
PAIRING_NOT_SUPPORTED = const(0x05)
INSUFF_ENCRYPTION_KEY_SIZE = const(0x06)
CMD_NOT_SUPPORTED = const(0x07)
UNSPECIFIED_REASON = const(0x08)
VERY_EARLY_NEXT_ATTEMPT = const(0x09)
SM_INVALID_PARAMS = const(0x0A)

# Pairing failed error codes. Error codes in EVT_BLUE_GAP_PAIRING_CMPLT event
SM_PAIRING_SUCCESS = const(0x00)
SM_PAIRING_TIMEOUT = const(0x01)
SM_PAIRING_FAILED = const(0x02)
