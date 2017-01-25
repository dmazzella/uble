# -*- coding: utf-8 -*-
import ustruct

from bluetooth_low_energy.protocols.hci import (
    HCI_READ_PACKET_SIZE)
from bluetooth_low_energy.protocols.hci.cmd import (
    OCF_DISCONNECT,
    OCF_LE_ADD_DEVICE_TO_WHITE_LIST,
    OCF_LE_CLEAR_WHITE_LIST,
    OCF_LE_CREATE_CONN,
    OCF_LE_CREATE_CONN_CANCEL,
    OCF_LE_ENCRYPT,
    OCF_LE_LTK_NEG_REPLY,
    OCF_LE_LTK_REPLY,
    OCF_LE_RAND,
    OCF_LE_READ_ADV_CHANNEL_TX_POWER,
    OCF_LE_READ_BUFFER_SIZE,
    OCF_LE_READ_CHANNEL_MAP,
    OCF_LE_READ_LOCAL_SUPPORTED_FEATURES,
    OCF_LE_READ_SUPPORTED_STATES,
    OCF_LE_READ_WHITE_LIST_SIZE,
    OCF_LE_RECEIVER_TEST,
    OCF_LE_REMOVE_DEVICE_FROM_WHITE_LIST,
    OCF_LE_SET_ADV_DATA,
    OCF_LE_SET_ADV_PARAMETERS,
    OCF_LE_SET_ADVERTISE_ENABLE,
    OCF_LE_SET_RANDOM_ADDRESS,
    OCF_LE_SET_SCAN_ENABLE,
    OCF_LE_SET_SCAN_PARAMETERS,
    OCF_LE_SET_SCAN_RESPONSE_DATA,
    OCF_LE_TEST_END,
    OCF_LE_TRANSMITTER_TEST,
    OCF_READ_BD_ADDR,
    OCF_READ_LOCAL_VERSION,
    OCF_READ_RSSI,
    OCF_READ_TRANSMIT_POWER_LEVEL,
    OCF_RESET, OGF_HOST_CTL,
    OGF_INFO_PARAM,
    OGF_LE_CTL,
    OGF_LINK_CTL,
    OGF_STATUS_PARAM,
    HCI_COMMAND)


# Timeout Exception
class TimeoutException(Exception):
    """TimeoutException"""
    def __init__(self, message):
        super(TimeoutException, self).__init__(message)

# Hardware Exception
class HardwareException(Exception):
    """HardwareException"""
    def __init__(self, message):
        super(HardwareException, self).__init__(message)

class BaseHCI(object):
    """
    AbstractBaseClass
    """
    def read(self, size=HCI_READ_PACKET_SIZE):
        """
        Abstract read method
        """
        raise NotImplementedError()

    def write(self, header, param):
        """
        Abstract write method
        """
        raise NotImplementedError()

    def __start__(self):
        raise NotImplementedError()

    def __stop__(self):
        raise NotImplementedError()

    def __process__(self, event):
        raise NotImplementedError()

    def run(self, timeout=100):
        """
        BLE event loop

        Note: This function call __start__() when invoked and __stop__() when
              KeyboardInterrupt, StopIteration or an Exception
              is raised.

              __process__() called whenever there is an event to be processed
        """
        try:
            self.__start__()
            while True:
                for event in self.hci_isr(timeout):
                    self.__process__(event)
        except (KeyboardInterrupt, StopIteration):
            pass
        finally:
            self.__stop__()

    def hci_isr(self, timeout=100):
        """
        Abstract hci_isr method
        """
        raise NotImplementedError()

    def hci_verify(self, hci_pckt):
        """
        Abstract hci_verify method
        """
        raise NotImplementedError()

    def hci_send_cmd(self, cmd, is_async=False):
        """
        Abstract hci_send_cmd method
        """
        raise NotImplementedError()

    def hci_send(self, header, param=b'', retry=10):
        """
        Abstract hci_send method
        """
        raise NotImplementedError()

    ###########################################################################
    #                         HCI Library Functions                           #
    ###########################################################################

    def hci_reset(self):
        """hci_reset"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_HOST_CTL,
            ocf=OCF_RESET)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_disconnect(self, handle=0, reason=0):
        """hci_disconnect"""
        data = ustruct.pack(
            "<HB",
            handle, reason)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LINK_CTL,
            ocf=OCF_DISCONNECT,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_read_local_version(self):
        """hci_le_read_local_version"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_INFO_PARAM,
            ocf=OCF_READ_LOCAL_VERSION)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_read_buffer_size(self):
        """hci_le_read_buffer_size"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_READ_BUFFER_SIZE)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_set_advertising_parameters(
            self, min_interval=0, max_interval=0, advtype=0, own_bdaddr_type=0,
            direct_bdaddr_type=0, direct_bdaddr=b'', chan_map=0, filter_=0):
        """hci_le_set_advertising_parameters"""
        data = ustruct.pack(
            "<HHBBB6sBB",
            min_interval, max_interval, advtype, own_bdaddr_type,
            direct_bdaddr_type, direct_bdaddr, chan_map, filter_)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_SET_ADV_PARAMETERS,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_set_advertising_data(self, length=0, data=b''):
        """hci_le_set_advertising_data"""
        data = ustruct.pack(
            "<B{:d}s".format(length),
            length, data)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_SET_ADV_DATA,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_set_advertise_enable(self, enable=False):
        """hci_le_set_advertise_enable"""
        data = ustruct.pack(
            "<B",
            int(enable))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_SET_ADVERTISE_ENABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_set_scan_parameters(
            self, type_=0, interval=0, window=0, own_bdaddr_type=0, filter_=0):
        """hci_le_set_scan_parameters"""
        data = ustruct.pack(
            "<BHHBB",
            type_, interval, window, own_bdaddr_type, filter_)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_SET_SCAN_PARAMETERS,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_set_scan_enable(self, enable=False, filter_dup=0):
        """hci_le_set_scan_enable"""
        data = ustruct.pack(
            "<BB",
            int(enable), filter_dup)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_SET_SCAN_ENABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_rand(self):
        """hci_le_rand"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_RAND)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_set_scan_resp_data(self, length=0, data=b''):
        """hci_le_set_scan_resp_data"""
        data = ustruct.pack(
            "<B{:d}s".format(length),
            length, data)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_SET_SCAN_RESPONSE_DATA,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_read_advertising_channel_tx_power(self):
        """hci_le_read_advertising_channel_tx_power"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_READ_ADV_CHANNEL_TX_POWER)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_set_random_address(self, bdaddr=b''):
        """hci_le_set_random_address"""
        data = ustruct.pack(
            "<6s",
            bdaddr)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_SET_RANDOM_ADDRESS,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_read_bd_addr(self):
        """hci_read_bd_addr"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_INFO_PARAM,
            ocf=OCF_READ_BD_ADDR)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_create_connection(
            self, interval=0, window=0, initiator_filter=0, peer_bdaddr_type=0,
            peer_bdaddr=b'', own_bdaddr_type=0, min_interval=0, max_interval=0,
            latency=0, supervision_timeout=0, min_ce_length=0, max_ce_length=0):
        """hci_le_create_connection"""
        data = ustruct.pack(
            "<HHBB6sBHHHHHH",
            interval, window, initiator_filter,
            peer_bdaddr_type, peer_bdaddr, own_bdaddr_type,
            min_interval, max_interval, latency,
            supervision_timeout,
            min_ce_length, max_ce_length)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_CREATE_CONN,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_create_connection_cancel(self):
        """hci_le_create_connection_cancel"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_CREATE_CONN_CANCEL)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_encrypt(self, key=b'', plaintext_data=b''):
        """hci_le_encrypt"""
        data = ustruct.pack(
            "<16s16s",
            key, plaintext_data)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_ENCRYPT,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_ltk_request_reply(self, handle=0, key=b''):
        """hci_le_ltk_request_reply"""
        data = ustruct.pack(
            "<H16s",
            handle, key)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_LTK_REPLY,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_ltk_request_neg_reply(self, handle=0):
        """hci_le_ltk_request_neg_reply"""
        data = ustruct.pack(
            "<H",
            handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_LTK_NEG_REPLY,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_read_white_list_size(self):
        """hci_le_read_white_list_size"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_READ_WHITE_LIST_SIZE)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_clear_white_list(self):
        """hci_le_clear_white_list"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_CLEAR_WHITE_LIST)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_add_device_to_white_list(self, bdaddr_type=0, bdaddr=b''):
        """hci_le_add_device_to_white_list"""
        data = ustruct.pack(
            "<B6s",
            bdaddr_type, bdaddr)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_ADD_DEVICE_TO_WHITE_LIST,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_remove_device_from_white_list(self, bdaddr_type=0, bdaddr=b''):
        """hci_le_remove_device_from_white_list"""
        data = ustruct.pack(
            "<B6s",
            bdaddr_type, bdaddr)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_REMOVE_DEVICE_FROM_WHITE_LIST,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_read_transmit_power_level(self, handle=0, type_=0):
        """hci_read_transmit_power_level"""
        data = ustruct.pack(
            "<HB",
            handle, type_)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_HOST_CTL,
            ocf=OCF_READ_TRANSMIT_POWER_LEVEL,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_read_rssi(self, handle=0):
        """hci_read_rssi"""
        data = ustruct.pack(
            "<H",
            handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_STATUS_PARAM,
            ocf=OCF_READ_RSSI,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_read_local_supported_features(self):
        """hci_le_read_local_supported_features"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_READ_LOCAL_SUPPORTED_FEATURES)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_read_channel_map(self, handle=0):
        """hci_le_read_channel_map"""
        data = ustruct.pack(
            "<H",
            handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_READ_CHANNEL_MAP,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_read_supported_states(self):
        """hci_le_read_supported_states"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_READ_SUPPORTED_STATES)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_receiver_test(self, frequency=0):
        """hci_le_receiver_test"""
        data = ustruct.pack(
            "<B",
            frequency)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_RECEIVER_TEST,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_transmitter_test(self, frequency=0, length=0, payload=0):
        """hci_le_transmitter_test"""
        data = ustruct.pack(
            "<BBB",
            frequency, length, payload)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_TRANSMITTER_TEST,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def hci_le_test_end(self):
        """hci_le_test_end"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_LE_CTL,
            ocf=OCF_LE_TEST_END)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd
