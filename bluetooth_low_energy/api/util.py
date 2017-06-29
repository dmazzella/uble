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


def format_advertisement(data):
    """ format advertisement data and scan response data. """
    resolve_dict = {
        # FLAGS AD type
        st_constant.AD_TYPE_FLAGS:'FLAGS',
        # Service UUID AD types
        st_constant.AD_TYPE_16_BIT_SERV_UUID:'16_BIT_SERV_UUID',
        st_constant.AD_TYPE_16_BIT_SERV_UUID_CMPLT_LIST:'16_BIT_SERV_UUID_CMPLT_LIST',
        st_constant.AD_TYPE_32_BIT_SERV_UUID:'32_BIT_SERV_UUID',
        st_constant.AD_TYPE_32_BIT_SERV_UUID_CMPLT_LIST:'32_BIT_SERV_UUID_CMPLT_LIST',
        st_constant.AD_TYPE_128_BIT_SERV_UUID:'128_BIT_SERV_UUID',
        st_constant.AD_TYPE_128_BIT_SERV_UUID_CMPLT_LIST:'128_BIT_SERV_UUID_CMPLT_LIST',
        # Local name AD types
        st_constant.AD_TYPE_SHORTENED_LOCAL_NAME:'SHORTENED_LOCAL_NAME',
        st_constant.AD_TYPE_COMPLETE_LOCAL_NAME:'COMPLETE_LOCAL_NAME',
        # TX power level AD type
        st_constant.AD_TYPE_TX_POWER_LEVEL:'TX_POWER_LEVEL',
        # Class of device
        st_constant.AD_TYPE_CLASS_OF_DEVICE:'CLASS_OF_DEVICE',
        # Security manager TK value AD type
        st_constant.AD_TYPE_SEC_MGR_TK_VALUE:'SEC_MGR_TK_VALUE',
        # Security manager OOB flags
        st_constant.AD_TYPE_SEC_MGR_OOB_FLAGS:'SEC_MGR_OOB_FLAGS',
        # Slave connection interval AD type
        st_constant.AD_TYPE_SLAVE_CONN_INTERVAL:'SLAVE_CONN_INTERVAL',
        # Service solicitation UUID list AD types
        st_constant.AD_TYPE_SERV_SOLICIT_16_BIT_UUID_LIST:'SERV_SOLICIT_16_BIT_UUID_LIST',
        st_constant.AD_TYPE_SERV_SOLICIT_32_BIT_UUID_LIST:'SERV_SOLICIT_32_BIT_UUID_LIST',
        st_constant.AD_TYPE_SERV_SOLICIT_128_BIT_UUID_LIST:'SERV_SOLICIT_128_BIT_UUID_LIST',
        # Service data AD type
        st_constant.AD_TYPE_SERVICE_DATA:'SERVICE_DATA',
        # Manufaturer specific data AD type
        st_constant.AD_TYPE_MANUFACTURER_SPECIFIC_DATA:'MANUFACTURER_SPECIFIC_DATA'
    }
    offset = 0
    size = len(data)
    advertisement_dict = {}
    while offset < size:
        field_len = int.from_bytes(data[offset:offset+1], 'little')
        if field_len == 0 or offset + field_len > size:
            return advertisement_dict

        field_type = int.from_bytes(data[offset+1:offset+2], 'little')
        field_value = data[offset+2:offset+2+field_len-1]

        advertisement_dict.update({resolve_dict[field_type]:field_value})

        offset += field_len + 1

    return advertisement_dict
