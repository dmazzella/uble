# -*- coding: utf-8 -*-
import gc; gc.threshold(4096)
from micropython import const
from binascii import hexlify, unhexlify

import ustruct
from bluetooth_low_energy.api.characteristic import Characteristic
from bluetooth_low_energy.api.constants import *
from bluetooth_low_energy.api.service import Service
from bluetooth_low_energy.api.uuid import UUID
from bluetooth_low_energy.modules.st_microelectronics.spbtle_rf import \
    SPBTLE_RF
from bluetooth_low_energy.protocols.hci import (HCI_EVENT_PKT, event, status,
                                                uart)


class Peripheral(SPBTLE_RF):
    """ Peripheral """

    def __init__(self, address, *args, **kwargs):
        address_type = kwargs.pop('address_type', ADDR_TYPE_PUBLIC)
        name = kwargs.pop('name', '')
        connectable = kwargs.pop('connectable', False)
        interval = kwargs.pop('interval', 0)
        data = kwargs.pop('data', None)
        services = kwargs.pop('services', [])
        event_handler = kwargs.pop('event_handler', None)
        super(Peripheral, self).__init__(*args, **kwargs)
        address = address if isinstance(address, bytes) else unhexlify(address)

        self.address = address
        self.address_type = address_type
        self.name = name
        self.connectable = connectable
        self.interval = interval
        self.data = data
        self.event_handler = None
        self.connection_handle = None
        self.services = []
        self.service_handle = None
        self.dev_name_char_handle = None
        self.appearance_char_handle = None

        if services:
            for _service in services:
                self.add_service(_service)

        if event_handler:
            self.set_event_handler(event_handler)

    def run(self, *args, **kwargs):
        super(Peripheral, self).run(*args, **kwargs)

    def __start__(self):
        # Reset BlueNRG-MS
        self.reset()

        evt_blue_hal_init = self.hci_wait_event(
            subevtcode=st_event.EVT_BLUE_HAL_INITIALIZED
        )
        # Check BlueNRG-MS ready
        if evt_blue_hal_init is None:
            raise ValueError("BlueNRG-MS not ready")

        # Check Evt_Blue_Initialized
        if evt_blue_hal_init.struct.reason_code != st_constant.RESET_NORMAL:
            raise ValueError("reason_code")

        # Reset BlueNRG again otherwise we won't be able to change its MAC address.
        # aci_hal_write_config_data() must be the first command after reset
        # otherwise it will fail.
        self.reset()

        # Check Evt_Blue_Initialized
        if self.hci_wait_event(
                subevtcode=st_event.EVT_BLUE_HAL_INITIALIZED
            ).struct.reason_code != st_constant.RESET_NORMAL:
            raise ValueError("reason_code")

        # Configure BlueNRG-MS address as public (its public address is used)
        result = self.aci_hal_write_config_data(
            offset=st_constant.CONFIG_DATA_PUBADDR_OFFSET,
            length=st_constant.CONFIG_DATA_PUBADDR_LEN,
            data=self.address
        ).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError(
                "aci_hal_write_config_data status: {:02x}".format(
                    result.status
                )
            )

        # Configure BlueNRG Mode
        result = self.aci_hal_write_config_data(
            offset=st_constant.CONFIG_DATA_MODE_OFFSET,
            length=st_constant.CONFIG_DATA_MODE_LEN,
            data=b'\x02').response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_write_config_data status: {:02x}".format(
                result.status))

        # Init BlueNRG GATT layer
        result = self.aci_gatt_init().response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_init status: {:02x}".format(
                result.status))

        # Init BlueNRG GAP layer as peripheral
        result = self.aci_gap_init_IDB05A1(
            role=st_constant.GAP_PERIPHERAL_ROLE_IDB05A1,
            privacy_enabled=bool(st_constant.PRIVACY_DISABLED),
            device_name_char_len=len(self.name)).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_init status: {:02x}".format(
                result.status))

        self.service_handle = result.service_handle
        self.dev_name_char_handle = result.dev_name_char_handle
        self.appearance_char_handle = result.appearance_char_handle

        # Init BlueNRG GATT layer
        result = self.aci_gatt_update_char_value(
            serv_handle=self.service_handle,
            char_handle=self.dev_name_char_handle,
            char_val_offset=0,
            char_value_len=len(self.name),
            char_value=self.name).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gatt_update_char_value status: {:02x}".format(
                result.status))

        result = self.aci_gap_set_auth_requirement(
            mitm_mode=st_constant.MITM_PROTECTION_REQUIRED,
            oob_enable=bool(st_constant.OOB_AUTH_DATA_ABSENT),
            oob_data=b'\x00' * 16,
            min_encryption_key_size=st_constant.MIN_ENCRY_KEY_SIZE,
            max_encryption_key_size=st_constant.MAX_ENCRY_KEY_SIZE,
            use_fixed_pin=bool(st_constant.USE_FIXED_PIN_FOR_PAIRING),
            fixed_pin=123456,
            bonding_mode=st_constant.BONDING).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_set_auth_requirement status: {:02x}".format(
                result.status))

        # Set output power level
        result = self.aci_hal_set_tx_power_level(
            en_high_power=1,
            pa_level=5).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_hal_set_tx_power_level status: {:02x}".format(
                result.status))

        # Add Services
        for _service in self.services:
            result = self.aci_gatt_add_serv(
                **_service.__properties__()
            ).response_struct
            if result.status != status.BLE_STATUS_SUCCESS:
                raise ValueError("aci_gatt_add_serv status: {:02x}".format(
                    result.status))
            _service.handle = result.handle

            # Add Characteristics
            for _characteristic in _service.get_characteristics():
                result = self.aci_gatt_add_char(
                    **_characteristic.__properties__(
                        service_handle=_service.handle,
                        char_value_len=_characteristic.char_value_len
                    )
                ).response_struct
                if result.status != status.BLE_STATUS_SUCCESS:
                    raise ValueError("aci_gatt_add_char status: {:02x}".format(
                        result.status))
                _characteristic.handle = result.handle

                # Add Descriptors
                for _descriptor in _characteristic.get_descriptors():
                    result = self.aci_gatt_add_char_desc(
                        **_descriptor.__properties__(
                            service_handle=_service.handle,
                            char_handle=_characteristic.handle
                        )
                    ).response_struct
                    _descriptor.handle = result.handle
                    if result.status != status.BLE_STATUS_SUCCESS:
                        raise ValueError(
                            "aci_gatt_add_char_desc status: {:02x}".format(
                                result.status))

        self.set_discoverable()

    def __stop__(self):
        """ __stop__ """
        # Reset BlueNRG-MS
        self.reset()

    def __process__(self, evt):
        """ Process event received from BlueNRG-MS """
        hci_uart = uart.HCI_UART.from_buffer(evt)
        if hci_uart.pkt_type == HCI_EVENT_PKT:
            hci_evt = event.HCI_EVENT.from_buffer(hci_uart.data)
            if hci_evt.evtcode == event.EVT_DISCONN_COMPLETE:
                self.connection_handle = None
                if callable(self.event_handler):
                    self.event_handler(
                        EVT_GAP_DISCONNECTED,
                        handler=self.connection_handle,
                        data=None
                    )
            elif hci_evt.evtcode == event.EVT_LE_META_EVENT:
                if hci_evt.subevtcode == event.EVT_LE_CONN_COMPLETE:
                    self.connection_handle = hci_evt.struct.handle
                    if callable(self.event_handler):
                        self.event_handler(
                            EVT_GAP_CONNECTED,
                            handler=self.connection_handle,
                            data=hci_evt.struct.peer_bdaddr
                        )
            elif hci_evt.evtcode == event.EVT_VENDOR:
                if hci_evt.subevtcode == st_event.EVT_BLUE_GATT_ATTRIBUTE_MODIFIED:
                    if callable(self.event_handler):
                        self.event_handler(
                            EVT_GATTS_WRITE,
                            handler=hci_evt.struct.attr_handle,
                            data=hci_evt.struct.att_data[
                                :hci_evt.struct.data_length]
                        )
                elif hci_evt.subevtcode == st_event.EVT_BLUE_GATT_WRITE_PERMIT_REQ:
                    result = self.aci_gatt_write_response(
                        conn_handle=self.connection_handle,
                        attr_handle=hci_evt.struct.attr_handle,
                        write_status=False,
                        err_code=0,
                        att_val_len=hci_evt.struct.data_length,
                        att_val=hci_evt.struct.data_buffer[
                            :hci_evt.struct.data_length]
                    ).response_struct
                    if result.status != status.BLE_STATUS_SUCCESS:
                        raise ValueError(
                            "aci_gatt_write_response status: {:02x}".format(
                                result.status))
                    elif result.status == status.BLE_STATUS_SUCCESS:
                        if callable(self.event_handler):
                            self.event_handler(
                                EVT_GATTS_WRITE_PERMIT_REQ,
                                handler=hci_evt.struct.attr_handle,
                                data=hci_evt.struct.data_buffer[
                                    :hci_evt.struct.data_length]
                            )
                elif hci_evt.subevtcode == st_event.EVT_BLUE_GATT_READ_PERMIT_REQ:
                    if self.connection_handle is not None:
                        result = self.aci_gatt_allow_read(
                            conn_handle=self.connection_handle).response_struct
                        if result.status != status.BLE_STATUS_SUCCESS:
                            raise ValueError(
                                "aci_gatt_allow_read status: {:02x}".format(
                                    result.status))
                        elif result.status == status.BLE_STATUS_SUCCESS:
                            if callable(self.event_handler):
                                self.event_handler(
                                    EVT_GATTS_READ_PERMIT_REQ,
                                    handler=hci_evt.struct.attr_handle,
                                    data=None
                                )


    def set_discoverable(self):
        """ set_discoverable """
        local_name = ustruct.pack(
            "<B{:d}s".format(len(self.name)),
            st_constant.AD_TYPE_COMPLETE_LOCAL_NAME, self.name
        ) if len(self.name) else b''

        # disable scan response
        result = self.hci_le_set_scan_resp_data(
            length=st_constant.MAX_ADV_DATA_LEN,
            data=b'\x00' * st_constant.MAX_ADV_DATA_LEN).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("hci_le_set_scan_resp_data status: {:02x}".format(
                result.status))

        # General Discoverable Mode
        result = self.aci_gap_set_discoverable(
            adv_type=(
                st_constant.ADV_IND if self.connectable
                else st_constant.ADV_SCAN_IND
            ),
            adv_interv_min=self.interval,
            adv_interv_max=self.interval,
            own_addr_type=self.address_type,
            adv_filter_policy=st_constant.NO_WHITE_LIST_USE,
            local_name_len=len(local_name),
            local_name=local_name,
            service_uuid_len=0,
            service_uuid_list=b'',
            slave_conn_interv_min=0,
            slave_conn_interv_max=0).response_struct
        if result.status != status.BLE_STATUS_SUCCESS:
            raise ValueError("aci_gap_set_discoverable status: {:02x}".format(
                result.status))

        if isinstance(self.data, (bytes, bytearray)):
            result = self.aci_gap_update_adv_data(
                adv_len=len(self.data),
                adv_data=self.data).response_struct
            if result.status != status.BLE_STATUS_SUCCESS:
                raise ValueError("aci_gap_update_adv_data status: {:02x}".format(
                    result.status))

    def add_service(self, _service):
        """ add_service """
        if isinstance(_service, Service):
            self.services.append(_service)
        else:
            raise TypeError("service must of type Service.")

    def set_event_handler(self, callback):
        """ set_event_handler """
        if not callable(callback):
            raise TypeError("callback must be a callable.")
        self.event_handler = callback

    def write_uuid(self, uuid_value, buffer=None, offset=0):
        """ write_characteristic """
        if not isinstance(uuid_value, UUID):
            raise TypeError("uuid must of type UUID.")

        if self.connection_handle is None:
            return

        for _service in self.services:
            for _characteristic in _service.get_characteristics():
                if uuid_value == _characteristic.uuid:
                    result = self.aci_gatt_update_char_value(
                        **_characteristic.__write_proprerties__(
                            buffer=buffer, offset=offset
                        )).response_struct
                    if result.status != status.BLE_STATUS_SUCCESS:
                        raise ValueError(
                            "aci_gatt_update_char_value status: {:02x}".format(
                                result.status))
                    return
                for _descriptor in _characteristic.get_descriptors():
                    if uuid_value == _descriptor.uuid:
                        result = self.aci_gatt_set_desc_value(
                            **_descriptor.__write_proprerties__(
                                buffer=buffer, offset=offset
                            )).response_struct
                        if result.status != status.BLE_STATUS_SUCCESS:
                            raise ValueError(
                                "aci_gatt_set_desc_value status: {:02x}".format(
                                    result.status))
                        return

    def read_uuid(self, uuid_value):
        """ read_uuid """
        if not isinstance(uuid_value, UUID):
            raise TypeError("uuid must of type UUID.")

        if self.connection_handle is None:
            return

        for _service in self.services:
            for _characteristic in _service.get_characteristics():
                if uuid_value == _characteristic.uuid:
                    result = self.aci_gatt_read_handle_value(
                        **_characteristic.__read_proprerties__()
                    ).response_struct
                    if result.status != status.BLE_STATUS_SUCCESS:
                        raise ValueError(
                            "aci_gatt_read_handle_value status: {:02x}".format(
                                result.status))
                    return result.value[:result.value_len]

    def uuid_from_handle(self, handle):
        """ uuid_from_handle """
        for _service in self.services:
            if handle == (_service.handle):
                return _service.uuid
            for _characteristic in _service.get_characteristics():
                if handle == (_characteristic.handle):
                    return _characteristic.uuid
                for _descriptor in _characteristic.get_descriptors():
                    if handle == (_descriptor.handle):
                        return _characteristic.uuid


__all__ = [
    'Peripheral'
]
