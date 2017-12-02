# -*- coding: utf-8 -*-
# pylint: disable=C0111
from micropython import const
from bluetooth_low_energy.api.characteristic import Characteristic
from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.util import compute_attributes_record
from bluetooth_low_energy.api.uuid import UUID


class Service(object):
    """ Service """

    def __init__(self, uuid, service_type=SERVICE_PRIMARY, characteristics=None):
        if not isinstance(uuid, UUID):
            raise TypeError("uuid must be of type UUID")

        self.uuid = uuid
        self.service_type = service_type
        self.handle = None
        self.characteristics = []
        if characteristics:
            for characteristic in characteristics:
                self.add_characteristic(characteristic)

    def __properties__(self, max_attr_records=0):
        return dict(
            service_uuid_type=self.uuid.uuid_type,
            service_uuid=self.uuid.value,
            service_type=self.service_type,
            max_attr_records=max_attr_records or compute_attributes_record(
                self)
        )

    def __str__(self):
        characteristics = self.get_characteristics()
        return "<Service uuid={!s} handle={:02x} characteristics=[{:s}]".format(
            self.uuid,
            self.handle or 0,
            "".join(
                "{!s}{:s}".format(
                    c, (", " if i < len(characteristics) - 1 else "")
                ) for i, c in enumerate(characteristics)
            )
        )

    def add_characteristic(self, characteristic):
        """ add_characteristic """
        if isinstance(characteristic, Characteristic):
            self.characteristics.append(characteristic)
        else:
            raise TypeError("characteristic must of type Characteristic.")

    def get_characteristic(self, uuid):
        """ get_characteristic """
        if isinstance(uuid, UUID):
            for characteristic in self.characteristics:
                if characteristic.uuid == uuid:
                    return characteristic
        else:
            raise TypeError("uuid must of type UUID.")

    def get_characteristics(self):
        """ get_characteristics """
        return self.characteristics


__all__ = [
    'Service'
]
