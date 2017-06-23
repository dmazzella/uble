# -*- coding: utf-8 -*-
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms import \
    constant as st_constant

def compute_attributes_record(service):
    """ compute the number of attributes needed by this service. """
    attribute_records = 1
    for characteristic in service.get_characteristics():
        # add two attributes, one for the characteristic declaration
        # and the other for the characteristic value.
        attribute_records += 2
        properties = characteristic.props
        # if notify or indicate are present, two attributes are needed
        if (properties & st_constant.CHAR_PROP_NOTIFY) or \
           (properties & st_constant.CHAR_PROP_INDICATE):
            attribute_records += 2

        # if broadcast is set, two attributes are needed
        if properties & st_constant.CHAR_PROP_BROADCAST:
            attribute_records += 2

        # if extended properties flag is set, two attributes are needed
        if properties & st_constant.CHAR_PROP_EXT:
            attribute_records += 2

        attribute_records += len(characteristic.get_descriptors())

    # for some reason, if there is just a service, this value should be equal to 5
    if attribute_records == 1:
        attribute_records = 5

    return attribute_records
