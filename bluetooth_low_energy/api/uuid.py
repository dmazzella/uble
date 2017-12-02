# -*- coding: utf-8 -*-
# pylint: disable=C0111
from bluetooth_low_energy.api.constants import *
from micropython import const
from ubinascii import hexlify, unhexlify


class UUID(object):
    """ UUID """

    def __init__(self, value):
        if isinstance(value, (str, UUID)):
            value = str(value).replace('-', '')
        else:
            raise TypeError("value must be of type UUID or str.")
        self.value = unhexlify(value)
        if len(self.value) not in (2, 16):
            raise ValueError(
                "UUID must be 2 or 16 bytes, got {:d} bytes".format(
                    len(self.value)
                )
            )
        self.value = bytes(reversed(self.value))
        self.uuid_type = UUID_16_BIT if len(self.value) == 2 else UUID_128_BIT

    def __properties__(self):
        return dict(
            uuid_type=self.uuid_type,
            value=self.value,
        )

    def __str__(self):
        value = hexlify(bytes(reversed(self.value)))
        return (
            b'-'.join(
                [
                    value[0:8],
                    value[8:12],
                    value[12:16],
                    value[16:20],
                    value[20:32]
                ]
            ) if len(self.value) == 16 else value
        ).decode('ascii')

    def __eq__(self, other):
        return self.value == UUID(other).value

    def __hash__(self):
        return hash(self.value)


__all__ = [
    'UUID'
]
