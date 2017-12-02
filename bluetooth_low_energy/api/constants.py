# -*- coding: utf-8 -*-
# pylint: disable=C0111
from micropython import const

from bluetooth_low_energy.protocols.hci import event
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms import \
    constant as st_constant
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms import \
    event as st_event


# Device address types
ADDR_TYPE_PUBLIC = const(1)
ADDR_TYPE_RANDOM_STATIC = const(2)

# Service types
SERVICE_PRIMARY = st_constant.PRIMARY_SERVICE
SERVICE_SECONDARY = st_constant.SECONDARY_SERVICE

# UUID types
UUID_16_BIT = st_constant.UUID_TYPE_16
UUID_128_BIT = st_constant.UUID_TYPE_128

# Events
EVT_GAP_CONNECTED = event.EVT_LE_CONN_COMPLETE
EVT_GAP_DISCONNECTED = event.EVT_DISCONN_COMPLETE
EVT_GATTS_WRITE = st_event.EVT_BLUE_GATT_ATTRIBUTE_MODIFIED
EVT_GATTS_READ_PERMIT_REQ = st_event.EVT_BLUE_GATT_READ_PERMIT_REQ
EVT_GATTS_WRITE_PERMIT_REQ = st_event.EVT_BLUE_GATT_WRITE_PERMIT_REQ

# Characteristic properties
PROP_BROADCAST = st_constant.CHAR_PROP_BROADCAST
PROP_READ = st_constant.CHAR_PROP_READ
PROP_WRITE_WO_RESP = st_constant.CHAR_PROP_WRITE_WITHOUT_RESP
PROP_WRITE = st_constant.CHAR_PROP_WRITE
PROP_NOTIFY = st_constant.CHAR_PROP_NOTIFY
PROP_INDICATE = st_constant.CHAR_PROP_INDICATE
PROP_AUTH_SIGNED_WR = st_constant.CHAR_PROP_SIGNED_WRITE

# Security permissions for an attribute
PERM_NONE = st_constant.ATTR_PERMISSION_NONE
PERM_AUTHEN_READ = st_constant.ATTR_PERMISSION_AUTHEN_READ
PERM_AUTHOR_READ = st_constant.ATTR_PERMISSION_AUTHOR_READ
PERM_ENCRY_READ = st_constant.ATTR_PERMISSION_ENCRY_READ
PERM_AUTHEN_WRITE = st_constant.ATTR_PERMISSION_AUTHEN_WRITE
PERM_AUTHOR_WRITE = st_constant.ATTR_PERMISSION_AUTHOR_WRITE
PERM_ENCRY_WRITE = st_constant.ATTR_PERMISSION_ENCRY_WRITE

# Access permissions for an attribute
ACC_NO_ACCESS = st_constant.ATTR_NO_ACCESS
ACC_READ_ONLY = st_constant.ATTR_ACCESS_READ_ONLY
ACC_WRITE_REQ_ONLY = st_constant.ATTR_ACCESS_WRITE_REQ_ONLY
ACC_READ_WRITE = st_constant.ATTR_ACCESS_READ_WRITE
ACC_WRITE_WITHOUT_RESPONSE = st_constant.ATTR_ACCESS_WRITE_WITHOUT_RESPONSE
ACC_SIGNED_WRITE_ALLOWED = st_constant.ATTR_ACCESS_SIGNED_WRITE_ALLOWED

# Gatt Event Mask
MASK_DONT_NOTIFY_EVENTS = st_constant.GATT_DONT_NOTIFY_EVENTS
MASK_NOTIFY_ATTRIBUTE_WRITE = st_constant.GATT_NOTIFY_ATTRIBUTE_WRITE
MASK_NOTIFY_WRITE_REQ_AND_WAIT_FOR_APPL_RESP = \
    st_constant.GATT_NOTIFY_WRITE_REQ_AND_WAIT_FOR_APPL_RESP
MASK_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP = \
    st_constant.GATT_NOTIFY_READ_REQ_AND_WAIT_FOR_APPL_RESP
