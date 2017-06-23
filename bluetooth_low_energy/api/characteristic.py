# -*- coding: utf-8 -*-
from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.descriptor import Descriptor
from bluetooth_low_energy.api.uuid import UUID

class Characteristic(object):
    """ Characteristic """

    def __init__(self, uuid,
                 char_value_len=20,
                 props=PROP_READ | PROP_WRITE,
                 perms=PERM_NONE,
                 mask=MASK_DONT_NOTIFY_EVENTS,
                 descriptors=None):

        if not isinstance(uuid, UUID):
            raise TypeError("uuid must be of type UUID")
        if not isinstance(props, int):
            raise TypeError("props must be of type int")
        if not isinstance(perms, int):
            raise TypeError("perms must be of type int")
        if not isinstance(mask, int):
            raise TypeError("mask must be of type int")

        self.uuid = uuid
        self.service_handle = None
        self.char_value_len = char_value_len
        self.handle = None
        self.props = props
        self.perms = perms
        self.mask = mask
        self.descriptors = []
        if descriptors:
            for descriptor in descriptors:
                self.add_descriptor(descriptor)

    def __properties__(self, service_handle=None, char_value_len=20):
        self.service_handle = service_handle
        self.char_value_len = char_value_len
        return dict(
            service_handle=self.service_handle,
            char_uuid_type=self.uuid.uuid_type,
            char_uuid=self.uuid.value,
            char_value_len=self.char_value_len,
            char_properties=self.props,
            sec_permissions=self.perms,
            gatt_evt_mask=self.mask,
            encry_key_size=st_constant.MAX_ENCRY_KEY_SIZE,
            is_variable=True
        )

    def __str__(self):
        descriptors = self.get_descriptors()
        return "<Characteristic uuid={!s} handle={:02x} descriptors=[{:s}]".format(
            self.uuid,
            self.handle or 0,
            "".join(
                "{!s}{:s}".format(
                    c, (", " if i < len(descriptors) - 1 else "")
                ) for i, c in enumerate(descriptors)
            )
        )

    def add_descriptor(self, descriptor):
        """ add_descriptor """
        if isinstance(descriptor, Descriptor):
            self.descriptors.append(descriptor)
        else:
            raise TypeError("descriptor must of type Descriptor.")

    def get_descriptors(self):
        """ get_descriptors """
        return self.descriptors

    def __write_proprerties__(self, buffer=None, offset=0):
        if not isinstance(buffer, (bytes, bytearray)):
            raise TypeError("buffer must of type bytes or bytearray.")
        return dict(
            serv_handle=self.service_handle,
            char_handle=self.handle,
            char_val_offset=offset,
            char_value_len=len(buffer),
            char_value=buffer
        )

    def __read_proprerties__(self):
        return dict(attr_handle=self.handle)


__all__ = [
    'Characteristic'
]
