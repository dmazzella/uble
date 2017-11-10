# -*- coding: utf-8 -*-
from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.uuid import UUID


class Descriptor(object):
    """ Descriptor """

    def __init__(self, uuid, value,
                 perms=PERM_NONE,
                 acc=ACC_NO_ACCESS,
                 mask=MASK_DONT_NOTIFY_EVENTS):
        if not isinstance(uuid, UUID):
            raise TypeError("uuid must be of type UUID")
        if not isinstance(acc, int):
            raise TypeError("acc must be of type int")
        if not isinstance(perms, int):
            raise TypeError("perms must be of type int")
        if not isinstance(mask, int):
            raise TypeError("mask must be of type int")

        self.service_handle = None
        self.char_handle = None
        self.handle = None
        self.uuid = uuid
        self.value = value
        self.perms = perms
        self.acc = acc
        self.mask = mask

    def __properties__(self, service_handle=None, char_handle=None):
        self.service_handle = service_handle
        self.char_handle = char_handle
        return dict(
            service_handle=self.service_handle,
            char_handle=self.char_handle,
            desc_uuid_type=self.uuid.uuid_type,
            uuid=self.uuid.value,
            desc_value_max_len=len(self.value),
            desc_value_len=len(self.value),
            desc_value=self.value,
            sec_permissions=self.perms,
            acc_permissions=self.acc,
            gatt_evt_mask=self.mask,
            encry_key_size=st_constant.MAX_ENCRY_KEY_SIZE,
            is_variable=True
        )

    def __str__(self):
        return "<Descriptor uuid={!s}>".format(self.uuid)

    def __write_proprerties__(self, buffer=None, offset=0):
        if not isinstance(buffer, (bytes, bytearray)):
            raise TypeError("buffer must of type bytes or bytearray.")
        return dict(
            serv_handle=self.service_handle,
            char_handle=self.char_handle,
            char_desc_handle=self.handle,
            char_desc_val_offset=offset,
            char_desc_value_len=len(buffer),
            char_desc_value=buffer
        )

__all__ = [
    'Descriptor'
]
