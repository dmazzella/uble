# -*- coding: utf-8 -*-
import machine
import utime
import ustruct
from micropython import const, heap_lock, heap_unlock
from ubinascii import hexlify, unhexlify

from bluetooth_low_energy.modules.base_hci import (
    BaseHCI,
    HardwareException
)
from bluetooth_low_energy.protocols.hci import (
    HCI_COMMAND_PKT,
    HCI_EVENT_HDR_SIZE,
    HCI_EVENT_PKT,
    HCI_READ_PACKET_SIZE
)
from bluetooth_low_energy.protocols.hci.cmd import (
    HCI_COMMAND,
    HCI_COMMANDS,
    OGF_VENDOR_CMD
)
from bluetooth_low_energy.protocols.hci.event import (
    EVT_CMD_COMPLETE,
    EVT_CMD_STATUS,
    EVT_HARDWARE_ERROR,
    EVT_LE_META_EVENT,
    EVT_VENDOR,
    HCI_EVENT,
    HCI_EVENTS,
    HCI_VENDOR_EVENTS
)
from bluetooth_low_energy.protocols.hci.status import (
    BLE_STATUS_SUCCESS
)
from bluetooth_low_energy.protocols.hci.uart import (
    HCI_UART
)
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.cmd import (
    HCI_VENDOR_COMMANDS,
    OCF_ATT_EXECUTE_WRITE_REQ,
    OCF_ATT_FIND_BY_TYPE_VALUE_REQ,
    OCF_ATT_FIND_INFO_REQ,
    OCF_ATT_PREPARE_WRITE_REQ,
    OCF_ATT_READ_BY_GROUP_TYPE_REQ,
    OCF_ATT_READ_BY_TYPE_REQ,
    OCF_GAP_ALLOW_REBOND_DB,
    OCF_GAP_AUTHORIZATION_RESPONSE,
    OCF_GAP_CLEAR_SECURITY_DB,
    OCF_GAP_CONFIGURE_WHITELIST,
    OCF_GAP_CREATE_CONNECTION,
    OCF_GAP_DELETE_AD_TYPE,
    OCF_GAP_GET_BONDED_DEVICES,
    OCF_GAP_GET_SECURITY_LEVEL,
    OCF_GAP_INIT,
    OCF_GAP_IS_DEVICE_BONDED,
    OCF_GAP_PASSKEY_RESPONSE,
    OCF_GAP_RESOLVE_PRIVATE_ADDRESS,
    OCF_GAP_SEND_PAIRING_REQUEST,
    OCF_GAP_SET_AUTH_REQUIREMENT,
    OCF_GAP_SET_AUTHOR_REQUIREMENT,
    OCF_GAP_SET_BROADCAST_MODE,
    OCF_GAP_SET_DIRECT_CONNECTABLE,
    OCF_GAP_SET_DISCOVERABLE,
    OCF_GAP_SET_IO_CAPABILITY,
    OCF_GAP_SET_LIMITED_DISCOVERABLE,
    OCF_GAP_SET_NON_CONNECTABLE,
    OCF_GAP_SET_NON_DISCOVERABLE,
    OCF_GAP_SET_UNDIRECTED_CONNECTABLE,
    OCF_GAP_SLAVE_SECURITY_REQUEST,
    OCF_GAP_START_AUTO_CONN_ESTABLISH_PROC,
    OCF_GAP_START_CONNECTION_UPDATE,
    OCF_GAP_START_GENERAL_CONN_ESTABLISH_PROC,
    OCF_GAP_START_GENERAL_DISCOVERY_PROC,
    OCF_GAP_START_LIMITED_DISCOVERY_PROC,
    OCF_GAP_START_NAME_DISCOVERY_PROC,
    OCF_GAP_START_OBSERVATION_PROC,
    OCF_GAP_START_SELECTIVE_CONN_ESTABLISH_PROC,
    OCF_GAP_TERMINATE,
    OCF_GAP_TERMINATE_GAP_PROCEDURE,
    OCF_GAP_UPDATE_ADV_DATA,
    OCF_GATT_ADD_CHAR,
    OCF_GATT_ADD_CHAR_DESC,
    OCF_GATT_ADD_SERV,
    OCF_GATT_ALLOW_READ,
    OCF_GATT_CONFIRM_INDICATION,
    OCF_GATT_DEL_CHAR,
    OCF_GATT_DEL_INC_SERV,
    OCF_GATT_DEL_SERV,
    OCF_GATT_DISC_ALL_CHARAC_DESCRIPTORS,
    OCF_GATT_DISC_ALL_CHARAC_OF_SERV,
    OCF_GATT_DISC_ALL_PRIM_SERVICES,
    OCF_GATT_DISC_CHARAC_BY_UUID,
    OCF_GATT_DISC_PRIM_SERVICE_BY_UUID,
    OCF_GATT_EXCHANGE_CONFIG,
    OCF_GATT_FIND_INCLUDED_SERVICES,
    OCF_GATT_INCLUDE_SERV,
    OCF_GATT_INIT,
    OCF_GATT_READ_CHAR_DESC,
    OCF_GATT_READ_CHARAC_VAL,
    OCF_GATT_READ_HANDLE_VALUE,
    OCF_GATT_READ_HANDLE_VALUE_OFFSET,
    OCF_GATT_READ_LONG_CHARAC_DESC,
    OCF_GATT_READ_LONG_CHARAC_VAL,
    OCF_GATT_READ_MULTIPLE_CHARAC_VAL,
    OCF_GATT_READ_USING_CHARAC_UUID,
    OCF_GATT_SET_DESC_VAL,
    OCF_GATT_SET_EVT_MASK,
    OCF_GATT_SET_SECURITY_PERMISSION,
    OCF_GATT_SIGNED_WRITE_WITHOUT_RESPONSE,
    OCF_GATT_UPD_CHAR_VAL,
    OCF_GATT_UPD_CHAR_VAL_EXT,
    OCF_GATT_WRITE_CHAR_DESC,
    OCF_GATT_WRITE_CHAR_VALUE,
    OCF_GATT_WRITE_CHARAC_RELIABLE,
    OCF_GATT_WRITE_LONG_CHARAC_DESC,
    OCF_GATT_WRITE_LONG_CHARAC_VAL,
    OCF_GATT_WRITE_RESPONSE,
    OCF_GATT_WRITE_WITHOUT_RESPONSE,
    OCF_GET_UPDATER_BUFSIZE,
    OCF_GET_UPDATER_VERSION,
    OCF_HAL_DEVICE_STANDBY,
    OCF_HAL_GET_ANCHOR_PERIOD,
    OCF_HAL_GET_FW_BUILD_NUMBER,
    OCF_HAL_GET_LINK_STATUS,
    OCF_HAL_LE_TX_TEST_PACKET_NUMBER,
    OCF_HAL_READ_CONFIG_DATA,
    OCF_HAL_SET_TX_POWER_LEVEL,
    OCF_HAL_TONE_START,
    OCF_HAL_TONE_STOP,
    OCF_HAL_WRITE_CONFIG_DATA,
    OCF_L2CAP_CONN_PARAM_UPDATE_REQ,
    OCF_L2CAP_CONN_PARAM_UPDATE_RESP,
    OCF_UPDATER_CALC_CRC,
    OCF_UPDATER_ERASE_BLUE_FLAG,
    OCF_UPDATER_ERASE_SECTOR,
    OCF_UPDATER_HW_VERSION,
    OCF_UPDATER_PROG_DATA_BLOCK,
    OCF_UPDATER_READ_DATA_BLOCK,
    OCF_UPDATER_REBOOT,
    OCF_UPDATER_RESET_BLUE_FLAG,
    OCF_UPDATER_START
)
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.constant import (
    UUID_TYPE_16
)
from bluetooth_low_energy.protocols.hci.vendor_specifics.st_microelectronics.bluenrg_ms.event import (
    HCI_VENDOR_EVENTS as ST_HCI_VENDOR_EVENTS
)

# Add ST Microelectronics Vendor Specific HCI_COMMANDS
HCI_COMMANDS[OGF_VENDOR_CMD] = HCI_VENDOR_COMMANDS
# Add ST Microelectronics Vendor Specific HCI_EVENTS
HCI_VENDOR_EVENTS.update(ST_HCI_VENDOR_EVENTS)

HCI_PCK_TYPE_OFFSET = const(0)
EVENT_PARAMETER_TOT_LEN_OFFSET = const(2)


class CSContext(object):

    def __init__(self, pin):
        self._pin = pin

    def __enter__(self):
        # Assert CS line
        self._pin.off()

    def __exit__(self, exc_type, exc_value, traceback):
        # Release CS line
        self._pin.on()
        return all(map(lambda x: x is None, [exc_type, exc_value, traceback]))


class BlueNRG_MS(BaseHCI):
    """
    Bluetooth Low Energy Network Processor supporting
    Bluetooth 4.1 core specification
    """

    def __init__(
        self,
        spi_bus=machine.SPI(2, baudrate=8000000, polarity=0),
        irq_pin=machine.Pin('Y3', machine.Pin.IN, machine.Pin.PULL_DOWN),
        rst_pin=machine.Pin('Y4', machine.Pin.OUT_PP),
        nss_pin=machine.Pin('Y5', machine.Pin.OUT_PP),
    ):
        """
        Defaults:
            - SPI(2) on the Y position:
                (NSS, SCK, MISO, MOSI) = (Y5, Y6, Y7, Y8) = (PB12, PB13, PB14, PB15)
              Params:
                phase: 0
                dir: SPI_DIRECTION_2LINES
                bits: 8
                nss: SPI_NSS_SOFT
                firstbit: SPI_FIRSTBIT_MSB
                ti: SPI_TIMODE_DISABLED
                crc:
                crc_calc: SPI_CRCCALCULATION_DISABLED

            - IRQ  on Y3 Pin
            - RST  on Y4 Pin
            - NSS  on Y5 Pin
            - SCK  on Y6 Pin
            - MISO on Y7 Pin
            - MOSI on Y8 Pin
        """

        if not isinstance(spi_bus, machine.SPI):
            raise TypeError("")

        m_pins = (irq_pin, rst_pin, nss_pin)
        if not all([isinstance(pin, machine.Pin) for pin in m_pins]):
            raise TypeError("")

        self._spi_bus = spi_bus

        self._irq_pin = irq_pin
        self._rst_pin = rst_pin
        self._nss_pin = nss_pin

        # Release CS line
        self._nss_pin.on()

    def reset(self):
        """
        Reset BlueNRG-MS module
        """
        self._rst_pin.off()
        utime.sleep_us(5)
        self._rst_pin.on()
        utime.sleep_us(5)

    def any(self):
        """any"""
        return bool(self._irq_pin.value())

    def set_spi_irq_as_output(self):
        """Pull IRQ high"""
        self._irq_pin.init(mode=machine.Pin.OUT_PP,
                           pull=machine.Pin.PULL_NONE, value=1)

    def set_spi_irq_as_input(self):
        """IRQ input"""
        self._irq_pin.init(mode=machine.Pin.IN, pull=machine.Pin.PULL_DOWN)

    def hw_bootloader(self):
        """hw_bootloader"""
        self.set_spi_irq_as_output()
        self.reset()
        utime.sleep_ms(4)
        self.set_spi_irq_as_input()

    def run(self, callback=None, callback_time=1000):
        """
        BLE event loop

        Note: This function call __start__() when invoked and __stop__() when
              KeyboardInterrupt, StopIteration or an Exception
              is raised.

              __process__() called whenever there is an event to be processed
        """
        try:
            self.__start__()
            start = utime.ticks_ms()
            while True:
                event = self.read(retry=5)
                if self.hci_verify(event):
                    self.__process__(event)
                # user defined periodic callback
                if callable(callback) and utime.ticks_diff(utime.ticks_ms(), start) >= callback_time:
                    callback()
                    start = utime.ticks_ms()

        except (KeyboardInterrupt, StopIteration) as ex:
            raise ex
        except Exception as ex:
            raise ex
        finally:
            self.__stop__()

    def __start__(self):
        raise NotImplementedError()

    def __stop__(self):
        raise NotImplementedError()

    def __process__(self, event):
        raise NotImplementedError()

    def read(self, size=HCI_READ_PACKET_SIZE, retry=5):
        """
        Read packet from BlueNRG-MS module
        """
        result = None
        # Exchange header
        header_master = b'\x0B\x00\x00\x00\x00'
        header_slave = bytearray(len(header_master))
        while retry:
            with CSContext(self._nss_pin):
                self._spi_bus.write_readinto(header_master, header_slave)
                rx_read_bytes = (header_slave[4] << 8) | header_slave[3]
                if header_slave[0] == 0x02 and rx_read_bytes > 0:
                    # SPI is ready
                    # avoid to read more data that size of the buffer
                    if rx_read_bytes > size:
                        rx_read_bytes = size
                    data = b'\xFF' * rx_read_bytes
                    result = bytearray(rx_read_bytes)
                    self._spi_bus.write_readinto(data, result)
                    break
                else:
                    utime.sleep_us(150)
            retry -= 1

        # Add a small delay to give time to the BlueNRG to set the IRQ pin low
        # to avoid a useless SPI read at the end of the transaction
        utime.sleep_us(150)
        return result

    def write(self, header, param, retry=5):
        """
        Write packet to BlueNRG-MS module
        """
        result = None
        # Exchange header
        header_master = b'\x0A\x00\x00\x00\x00'
        header_slave = bytearray(len(header_master))
        while retry:
            with CSContext(self._nss_pin):
                self._spi_bus.write_readinto(header_master, header_slave)
                rx_write_bytes = header_slave[1]
                rx_read_bytes = (header_slave[4] << 8) | header_slave[3]
                if header_slave[0] == 0x02 and (
                    rx_write_bytes > 0 or rx_read_bytes > 0
                ):
                    # SPI is ready
                    if header:
                        # avoid to write more data that size of the buffer
                        if rx_write_bytes >= len(header):
                            result = bytearray(len(header))
                            self._spi_bus.write_readinto(header, result)
                            if param:
                                rx_write_bytes -= len(header)
                                # avoid to read more data that size of the
                                # buffer
                                if len(param) > rx_write_bytes:
                                    tx_bytes = rx_write_bytes
                                else:
                                    tx_bytes = len(param)
                                result = bytearray(tx_bytes)
                                self._spi_bus.write_readinto(param, result)
                                break
                            else:
                                break
                        else:
                            break
                    else:
                        break
                else:
                    utime.sleep_us(150)
            retry -= 1

        return result

    def hci_verify(self, hci_pckt):
        """
        Verify HCI packet
        """
        if hci_pckt is None:
            return False

        if hci_pckt[HCI_PCK_TYPE_OFFSET] != HCI_EVENT_PKT:
            return False

        if hci_pckt[EVENT_PARAMETER_TOT_LEN_OFFSET] != \
                len(hci_pckt) - (1 + HCI_EVENT_HDR_SIZE):
            return False

        return True

    def hci_wait_event(self, evtcode=0, subevtcode=0, timeout=1000, retry=5):
        """
        Wait for event and filter it if needed
        """
        # Maximum timeout is 1 seconds
        start = utime.ticks_ms()
        while utime.ticks_diff(utime.ticks_ms(), start) <= min(timeout, 1000):
            event = self.read(retry=retry)
            if self.hci_verify(event) and isinstance(event, (bytearray, bytes)):
                hci_uart = HCI_UART.from_buffer(event)
                if hci_uart.pkt_type == HCI_EVENT_PKT:
                    hci_evt = HCI_EVENT.from_buffer(hci_uart.data)
                    if not evtcode and not subevtcode:
                        return hci_evt
                    if subevtcode:
                        if hci_evt.evtcode in (EVT_LE_META_EVENT, EVT_VENDOR):
                            if hci_evt.subevtcode == subevtcode:
                                return hci_evt
                            else:
                                raise ValueError("unexpected subevtcode")
                    if evtcode:
                        if hci_evt.evtcode == evtcode:
                            return hci_evt
                        else:
                            raise ValueError("unexpected evtcode")
                else:
                    raise TypeError("not HCI_EVENT_PKT")
            else:
                continue

    def hci_send_cmd(self, cmd, is_async=False, timeout=1000, retry=5):
        """hci_send_cmd"""
        if not isinstance(cmd, HCI_COMMAND):
            raise TypeError("HCI_COMMAND")

        header, param = cmd.to_buffer(split=True)
        if len(header) == cmd._struct_size:
            header = ustruct.pack("<B3s", HCI_COMMAND_PKT, header)
        self.hci_send(header, param)

        if is_async:
            return

        # Maximum timeout is 1 seconds
        start = utime.ticks_ms()
        while utime.ticks_diff(utime.ticks_ms(), start) <= min(timeout, 1000):
            event = self.read(retry=retry)
            if self.hci_verify(event) and isinstance(event, (bytearray, bytes)):
                hci_uart = HCI_UART.from_buffer(event)
                if hci_uart.pkt_type == HCI_EVENT_PKT:
                    hci_evt = HCI_EVENT.from_buffer(hci_uart.data)
                    if hci_evt.evtcode == EVT_CMD_STATUS:
                        if hci_evt.struct.opcode != cmd.opcode:
                            raise ValueError(hci_evt.struct.opcode)
                        if cmd.evtcode != hci_evt.evtcode:
                            if hci_evt.struct.status != BLE_STATUS_SUCCESS:
                                raise ValueError(hci_evt.struct.status)
                        cmd.response_data = hci_evt.data[hci_evt.struct_size:]
                        return event
                    elif hci_evt.evtcode == EVT_CMD_COMPLETE:
                        if hci_evt.struct.opcode != cmd.opcode:
                            raise ValueError(hci_evt.struct.opcode)
                        cmd.response_data = hci_evt.data[hci_evt.struct_size:]
                        return event
                    elif hci_evt.evtcode == EVT_LE_META_EVENT:
                        if hci_evt.subevtcode != cmd.evtcode:
                            raise ValueError(hci_evt.subevtcode)
                        cmd.response_data = hci_evt.data[hci_evt.struct_size:]
                        return event
                    elif hci_evt.evtcode == EVT_HARDWARE_ERROR:
                        cmd.response_data = hci_evt.data[hci_evt.struct_size:]
                        raise HardwareException(cmd.response_data)
            else:
                continue

    def hci_send(self, header, param=b'', retry=5):
        """
        Send HCI Header, if data available send it
        """
        return self.write(header, param, retry=retry)

    def get_version(self):
        """
        Get BlueNRG-MS firmware version
        """
        hci_cmd = self.hci_le_read_local_version()
        response = hci_cmd.response_struct
        if response.status != BLE_STATUS_SUCCESS:
            raise ValueError("status")
        fw_major = response.hci_revision & 0xFF
        fw_minor = (response.lmp_pal_subversion & 0xF0) >> 4
        fw_qualifier = (response.lmp_pal_subversion & 0xF)
        patch = ('' if fw_qualifier == 0 else chr(96 + fw_qualifier))
        dev = ('dev' if response.lmp_pal_subversion & 0x8000 else '')
        return ''.join(['.'.join(map(str, [fw_major, fw_minor])), patch, dev])

    ###########################################################################
    #                         HCI Library Functions                           #
    ###########################################################################

    ###########################################################################
    #                                GAP                                      #
    ###########################################################################

    def aci_gap_init_IDB04A1(self, role=0):
        """aci_gap_init_IDB04A1"""
        data = ustruct.pack(
            "<B",
            role)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_INIT,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_init_IDB05A1(
            self, role=0, privacy_enabled=False, device_name_char_len=0):
        """aci_gap_init_IDB05A1"""
        data = ustruct.pack(
            "<BBB",
            role, int(privacy_enabled), device_name_char_len)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_INIT,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_non_discoverable(self):
        """aci_gap_set_non_discoverable"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_NON_DISCOVERABLE)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_limited_discoverable(
            self, adv_type=0, adv_interv_min=0, adv_interv_max=0,
            own_addr_type=0, adv_filter_policy=0, local_name_len=0,
            local_name=b'', service_uuid_len=0, service_uuid_list=b'',
            slave_conn_interv_min=0, slave_conn_interv_max=0):
        """aci_gap_set_limited_discoverable"""
        data = ustruct.pack(
            "<BHHBBB{:d}sB{:d}sHH".format(local_name_len, service_uuid_len),
            adv_type, adv_interv_min, adv_interv_max,
            own_addr_type,
            adv_filter_policy,
            local_name_len,
            local_name,
            service_uuid_len,
            service_uuid_list,
            slave_conn_interv_min, slave_conn_interv_max)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_LIMITED_DISCOVERABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_discoverable(
            self, adv_type=0, adv_interv_min=0, adv_interv_max=0,
            own_addr_type=0, adv_filter_policy=0, local_name_len=0,
            local_name=b'', service_uuid_len=0, service_uuid_list=b'',
            slave_conn_interv_min=0, slave_conn_interv_max=0):
        """aci_gap_set_discoverable"""
        data = ustruct.pack(
            "<BHHBBB{:d}sB{:d}sHH".format(local_name_len, service_uuid_len),
            adv_type, adv_interv_min, adv_interv_max,
            own_addr_type, adv_filter_policy,
            local_name_len,
            local_name,
            service_uuid_len,
            service_uuid_list,
            slave_conn_interv_min, slave_conn_interv_max)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_DISCOVERABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_direct_connectable_IDB05A1(
            self, own_addr_type=0, directed_adv_type=0, initiator_addr_type=0,
            initiator_addr=b'', adv_interv_min=0, adv_interv_max=0):
        """aci_gap_set_direct_connectable_IDB05A1"""
        data = ustruct.pack(
            "<BBB6sHH",
            own_addr_type, directed_adv_type,
            initiator_addr_type, initiator_addr,
            adv_interv_min, adv_interv_max)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_DIRECT_CONNECTABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_direct_connectable_IDB04A1(
            self, own_addr_type=0, initiator_addr_type=0, initiator_addr=b''):
        """aci_gap_set_direct_connectable_IDB04A1"""
        data = ustruct.pack(
            "<BB6s",
            own_addr_type, initiator_addr_type,
            initiator_addr)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_DIRECT_CONNECTABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_io_capability(self, io_capability=0):
        """aci_gap_set_io_capability"""
        data = ustruct.pack(
            "<B",
            io_capability)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_IO_CAPABILITY,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_auth_requirement(
            self, mitm_mode=0, oob_enable=False, oob_data=b'',
            min_encryption_key_size=0, max_encryption_key_size=0,
            use_fixed_pin=False, fixed_pin=0, bonding_mode=0):
        """aci_gap_set_auth_requirement"""
        data = ustruct.pack(
            "<BB16sBBBIB",
            mitm_mode, int(oob_enable), oob_data,
            min_encryption_key_size, max_encryption_key_size,
            int(use_fixed_pin), fixed_pin, bonding_mode)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_AUTH_REQUIREMENT,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_author_requirement(
            self, conn_handle=0, authorization_enable=False):
        """aci_gap_set_author_requirement"""
        data = ustruct.pack(
            "<HB",
            conn_handle, int(authorization_enable))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_AUTHOR_REQUIREMENT,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_pass_key_response(self, conn_handle=0, passkey=0):
        """aci_gap_pass_key_response"""
        data = ustruct.pack(
            "<HI",
            conn_handle, passkey)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_PASSKEY_RESPONSE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_authorization_response(self, conn_handle=0, authorize=0):
        """aci_gap_authorization_response"""
        data = ustruct.pack(
            "<HB",
            conn_handle, authorize)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_AUTHORIZATION_RESPONSE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_non_connectable_IDB05A1(
            self, adv_type=0, own_address_type=0):
        """aci_gap_set_non_connectable_IDB05A1"""
        data = ustruct.pack(
            "<BB",
            adv_type, own_address_type)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_NON_CONNECTABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_non_connectable_IDB04A1(
            self, adv_type=0):
        """aci_gap_set_non_connectable_IDB04A1"""
        data = ustruct.pack(
            "<B",
            adv_type)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_NON_CONNECTABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_undirected_connectable(
            self, own_addr_type=0, adv_filter_policy=0):
        """aci_gap_set_undirected_connectable"""
        data = ustruct.pack(
            "<BB",
            own_addr_type, adv_filter_policy)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_UNDIRECTED_CONNECTABLE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_slave_security_request(
            self, conn_handle=0, bonding=0, mitm_protection=0):
        """aci_gap_slave_security_request"""
        data = ustruct.pack(
            "<HBB",
            conn_handle, bonding, mitm_protection)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SLAVE_SECURITY_REQUEST,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_update_adv_data(self, adv_len=0, adv_data=b''):
        """aci_gap_update_adv_data"""
        data = ustruct.pack(
            "<B{:d}s".format(adv_len),
            adv_len, adv_data)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_UPDATE_ADV_DATA,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_delete_ad_type(self, ad_type=0):
        """aci_gap_delete_ad_type"""
        data = ustruct.pack(
            "<B",
            ad_type)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_DELETE_AD_TYPE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_get_security_level(self):
        """aci_gap_get_security_level"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_GET_SECURITY_LEVEL)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_configure_whitelist(self):
        """aci_gap_configure_whitelist"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_CONFIGURE_WHITELIST)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_terminate(self, conn_handle=0, reason=0):
        """aci_gap_terminate"""
        data = ustruct.pack(
            "<HB",
            conn_handle, reason)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_TERMINATE,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_clear_security_database(self):
        """aci_gap_clear_security_database"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_CLEAR_SECURITY_DB)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_allow_rebond_IDB05A1(self, conn_handle=0):
        """aci_gap_allow_rebond_IDB05A1"""
        data = ustruct.pack(
            "<H",
            conn_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_ALLOW_REBOND_DB,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_allow_rebond_IDB04A1(self):
        """aci_gap_allow_rebond_IDB04A1"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_ALLOW_REBOND_DB)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_limited_discovery_proc(
            self, scan_interval=0, scan_window=0,
            own_address_type=0, filter_duplicates=0):
        """aci_gap_start_limited_discovery_proc"""
        data = ustruct.pack(
            "<HHBB",
            scan_interval, scan_window, own_address_type, filter_duplicates)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_LIMITED_DISCOVERY_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_general_discovery_proc(
            self, scan_interval=0, scan_window=0,
            own_address_type=0, filter_duplicates=0):
        """aci_gap_start_general_discovery_proc"""
        data = ustruct.pack(
            "<HHBB",
            scan_interval, scan_window, own_address_type, filter_duplicates)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_GENERAL_DISCOVERY_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_name_discovery_proc(
            self, scan_interval=0, scan_window=0, peer_bdaddr_type=0,
            peer_bdaddr=b'', own_bdaddr_type=0, conn_min_interval=0,
            conn_max_interval=0, conn_latency=0, supervision_timeout=0,
            min_conn_length=0, max_conn_length=0):
        """aci_gap_start_name_discovery_proc"""
        data = ustruct.pack(
            "<HHB6sBHHHHHH",
            scan_interval, scan_window,
            peer_bdaddr_type, peer_bdaddr, own_bdaddr_type,
            conn_min_interval, conn_max_interval, conn_latency,
            supervision_timeout, min_conn_length, max_conn_length)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_NAME_DISCOVERY_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_auto_conn_establish_proc_IDB05A1(
            self, scan_interval=0, scan_window=0, own_bdaddr_type=0,
            conn_min_interval=0, conn_max_interval=0, conn_latency=0,
            supervision_timeout=0, min_conn_length=0, max_conn_length=0,
            num_whitelist_entries=0, addr_array=b''):
        """aci_gap_start_auto_conn_establish_proc_IDB05A1"""
        data = ustruct.pack(
            "<HHBHHHHHHB{:d}s".format(num_whitelist_entries * 7),
            scan_interval, scan_window,
            own_bdaddr_type,
            conn_min_interval, conn_max_interval, conn_latency,
            supervision_timeout,
            min_conn_length, max_conn_length,
            num_whitelist_entries,
            addr_array)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_AUTO_CONN_ESTABLISH_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_auto_conn_establish_proc_IDB04A1(
            self, scan_interval=0, scan_window=0, own_bdaddr_type=0,
            conn_min_interval=0, conn_max_interval=0, conn_latency=0,
            supervision_timeout=0, min_conn_length=0, max_conn_length=0,
            use_reconn_addr=False, reconn_addr=b'', num_whitelist_entries=0,
            addr_array=b''):
        """aci_gap_start_auto_conn_establish_proc_IDB04A1"""
        data = ustruct.pack(
            "<HHBHHHHHHB6sB{:d}s".format(num_whitelist_entries * 7),
            scan_interval, scan_window,
            own_bdaddr_type,
            conn_min_interval, conn_max_interval, conn_latency,
            supervision_timeout,
            min_conn_length, max_conn_length,
            int(use_reconn_addr), reconn_addr,
            num_whitelist_entries,
            addr_array)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_AUTO_CONN_ESTABLISH_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_general_conn_establish_proc_IDB05A1(
            self, scan_type=0, scan_interval=0, scan_window=0,
            own_address_type=0, filter_duplicates=False):
        """aci_gap_start_general_conn_establish_proc_IDB05A1"""
        data = ustruct.pack(
            "<BHHBB",
            scan_type, scan_interval, scan_window,
            own_address_type, int(filter_duplicates))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_GENERAL_CONN_ESTABLISH_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_general_conn_establish_proc_IDB04A1(
            self, scan_type=0, scan_interval=0, scan_window=0,
            own_address_type=0, filter_duplicates=False, reconn_addr=b''):
        """aci_gap_start_general_conn_establish_proc_IDB04A1"""
        data = ustruct.pack(
            "<BHHBB6s",
            scan_type, scan_interval, scan_window,
            own_address_type, int(filter_duplicates),
            reconn_addr)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_GENERAL_CONN_ESTABLISH_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_selective_conn_establish_proc(
            self, scan_type=0, scan_interval=0, scan_window=0,
            own_address_type=0, filter_duplicates=False,
            num_whitelist_entries=0, addr_array=b''):
        """aci_gap_start_selective_conn_establish_proc"""
        data = ustruct.pack(
            "<BHHBBB{:d}s".format(num_whitelist_entries * 7),
            scan_type, scan_interval, scan_window, own_address_type,
            int(filter_duplicates), num_whitelist_entries, addr_array)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_SELECTIVE_CONN_ESTABLISH_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_create_connection(
            self, scan_interval=0, scan_window=0, peer_bdaddr_type=0,
            peer_bdaddr=b'', own_bdaddr_type=0, conn_min_interval=0,
            conn_max_interval=0, conn_latency=0, supervision_timeout=0,
            min_conn_length=0, max_conn_length=0):
        """aci_gap_create_connection"""
        data = ustruct.pack(
            "<HHB6sBHHHHHH",
            scan_interval, scan_window,
            peer_bdaddr_type, peer_bdaddr,
            own_bdaddr_type,
            conn_min_interval, conn_max_interval, conn_latency,
            supervision_timeout,
            min_conn_length, max_conn_length)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_CREATE_CONNECTION,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_terminate_gap_procedure(self, procedure_code=0):
        """aci_gap_terminate_gap_procedure"""
        data = ustruct.pack(
            "<B",
            procedure_code)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_TERMINATE_GAP_PROCEDURE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_connection_update(
            self, conn_handle=0, conn_min_interval=0, conn_max_interval=0,
            conn_latency=0, supervision_timeout=0, min_conn_length=0,
            max_conn_length=0):
        """aci_gap_start_connection_update"""
        data = ustruct.pack(
            "<HHHHHHH",
            conn_handle,
            conn_min_interval, conn_max_interval, conn_latency,
            supervision_timeout, min_conn_length, max_conn_length)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_CONNECTION_UPDATE,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_send_pairing_request(self, conn_handle=0, force_rebond=False):
        """aci_gap_send_pairing_request"""
        data = ustruct.pack(
            "<HB",
            conn_handle, int(force_rebond))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SEND_PAIRING_REQUEST,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_resolve_private_address_IDB05A1(self, private_address=b''):
        """aci_gap_resolve_private_address_IDB05A1"""
        data = ustruct.pack(
            "<6s",
            private_address)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_RESOLVE_PRIVATE_ADDRESS,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_resolve_private_address_IDB04A1(self):
        """aci_gap_resolve_private_address_IDB04A1"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_RESOLVE_PRIVATE_ADDRESS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_set_broadcast_mode(
            self, adv_interv_min=0, adv_interv_max=0, adv_type=0,
            own_addr_type=0, adv_data_length=0, adv_data=b'',
            num_whitelist_entries=0, addr_array=b''):
        """aci_gap_set_broadcast_mode"""
        data = ustruct.pack(
            "<HHBBB{:d}sB{:d}s".format(
                adv_data_length, num_whitelist_entries * 7),
            adv_interv_min, adv_interv_max,
            adv_type, own_addr_type,
            adv_data_length,
            adv_data,
            num_whitelist_entries,
            addr_array)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_SET_BROADCAST_MODE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_start_observation_procedure(
            self, scan_interval=0, scan_window=0, scan_type=0,
            own_address_type=0, filter_duplicates=False):
        """aci_gap_start_observation_procedure"""
        data = ustruct.pack(
            "<HHBBB",
            scan_interval, scan_window, scan_type,
            own_address_type, int(filter_duplicates))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_START_OBSERVATION_PROC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_is_device_bonded(self, peer_address_type=0, peer_address=b''):
        """aci_gap_is_device_bonded"""
        data = ustruct.pack(
            "<B6s",
            peer_address_type, peer_address)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_IS_DEVICE_BONDED,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gap_get_bonded_devices(self):
        """aci_gap_get_bonded_devices"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GAP_GET_BONDED_DEVICES)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    ###########################################################################
    #                               GATT                                      #
    ###########################################################################

    def aci_gatt_init(self):
        """aci_gatt_init"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_INIT)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_add_serv(
            self, service_uuid_type=0, service_uuid=b'', service_type=0,
            max_attr_records=0):
        """aci_gatt_add_serv"""
        uuid_len = 2 if service_uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<B{:d}sBB".format(uuid_len),
            service_uuid_type, service_uuid,
            service_type, max_attr_records)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_ADD_SERV,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_include_service(
            self, service_handle=0, included_start_handle=0,
            included_end_handle=0, included_uuid_type=0, included_uuid=b''):
        """aci_gatt_include_service"""
        uuid_len = 2 if included_uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<HHHB{:d}s".format(uuid_len),
            service_handle, included_start_handle,
            included_end_handle, included_uuid_type,
            included_uuid)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_INCLUDE_SERV,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_add_char(
            self, service_handle=0, char_uuid_type=0, char_uuid=b'',
            char_value_len=0, char_properties=0, sec_permissions=0,
            gatt_evt_mask=0, encry_key_size=0, is_variable=False):
        """aci_gatt_add_char"""
        uuid_len = 2 if char_uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<HB{:d}sBBBBBB".format(uuid_len),
            service_handle, char_uuid_type, char_uuid,
            char_value_len, char_properties, sec_permissions,
            gatt_evt_mask, encry_key_size, int(is_variable))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_ADD_CHAR,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_add_char_desc(
            self, service_handle=0, char_handle=0, desc_uuid_type=0,
            uuid=b'', desc_value_max_len=0, desc_value_len=0, desc_value=b'',
            sec_permissions=0, acc_permissions=0, gatt_evt_mask=0,
            encry_key_size=0, is_variable=False):
        """aci_gatt_add_char_desc"""
        uuid_len = 2 if desc_uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<HHB{:d}sBB{:d}sBBBBB".format(uuid_len, desc_value_len),
            service_handle, char_handle, desc_uuid_type,
            uuid, desc_value_max_len, desc_value_len,
            desc_value, sec_permissions,
            acc_permissions, gatt_evt_mask, encry_key_size,
            int(is_variable))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_ADD_CHAR_DESC,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_update_char_value(
            self, serv_handle=0, char_handle=0, char_val_offset=0,
            char_value_len=0, char_value=b''):
        """aci_gatt_update_char_value"""
        data = ustruct.pack(
            "<HHBB{:d}s".format(char_value_len),
            serv_handle, char_handle, char_val_offset,
            char_value_len, char_value)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_UPD_CHAR_VAL,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_del_char(self, serv_handle=0, char_handle=0):
        """aci_gatt_del_char"""
        data = ustruct.pack(
            "<HH",
            serv_handle, char_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_DEL_CHAR,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_del_service(self, serv_handle=0):
        """aci_gatt_del_service"""
        data = ustruct.pack(
            "<H",
            serv_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_DEL_SERV,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_del_include_service(
            self, serv_handle=0, include_serv_handle=0):
        """aci_gatt_del_include_service"""
        data = ustruct.pack(
            "<HH",
            serv_handle, include_serv_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_DEL_INC_SERV,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_set_event_mask(self, event_mask=0):
        """aci_gatt_set_event_mask"""
        data = ustruct.pack(
            "<I",
            event_mask)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_SET_EVT_MASK,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_exchange_configuration(self, conn_handle=0):
        """aci_gatt_exchange_configuration"""
        data = ustruct.pack(
            "<H",
            conn_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_EXCHANGE_CONFIG,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_att_find_information_req(
            self, conn_handle=0, start_handle=0, end_handle=0):
        """aci_att_find_information_req"""
        data = ustruct.pack(
            "<HHH",
            conn_handle, start_handle, end_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_ATT_FIND_INFO_REQ,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_att_find_by_type_value_req(
            self, conn_handle=0, start_handle=0, end_handle=0,
            uuid=b'', attr_val_len=0, attr_val=b''):
        """aci_att_find_by_type_value_req"""
        data = ustruct.pack(
            "<HHH2sB{:d}s".format(attr_val_len),
            conn_handle, start_handle, end_handle, uuid,
            attr_val_len, attr_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_ATT_FIND_BY_TYPE_VALUE_REQ,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_att_read_by_type_req(
            self, conn_handle=0, start_handle=0, end_handle=0,
            uuid_type=0, uuid=b''):
        """aci_att_read_by_type_req"""
        uuid_len = 2 if uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<HHHB{:d}s".format(uuid_len),
            conn_handle, start_handle, end_handle,
            uuid_type, uuid)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_ATT_READ_BY_TYPE_REQ,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_att_read_by_group_type_req(
            self, conn_handle=0, start_handle=0, end_handle=0,
            uuid_type=0, uuid=b''):
        """aci_att_read_by_group_type_req"""
        uuid_len = 2 if uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<HHHB{:d}s".format(uuid_len),
            conn_handle, start_handle, end_handle,
            uuid_type, uuid)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_ATT_READ_BY_GROUP_TYPE_REQ,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_att_prepare_write_req(
            self, conn_handle=0, attr_handle=0, value_offset=0,
            attr_val_len=0, attr_val=b''):
        """aci_att_prepare_write_req"""
        data = ustruct.pack(
            "<HHHB{:d}s".format(attr_val_len),
            conn_handle, attr_handle, value_offset,
            attr_val_len, attr_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_ATT_PREPARE_WRITE_REQ,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_att_execute_write_req(self, conn_handle=0, execute=0):
        """aci_att_execute_write_req"""
        data = ustruct.pack(
            "<HB",
            conn_handle, execute)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_ATT_EXECUTE_WRITE_REQ,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_disc_all_prim_services(self, conn_handle=0):
        """aci_gatt_disc_all_prim_services"""
        data = ustruct.pack(
            "<H",
            conn_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_DISC_ALL_PRIM_SERVICES,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_disc_prim_service_by_uuid(
            self, conn_handle=0, uuid_type=0, uuid=b''):
        """aci_gatt_disc_prim_service_by_uuid"""
        uuid_len = 2 if uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<HB{:d}s".format(uuid_len),
            conn_handle, uuid_type, uuid)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_DISC_PRIM_SERVICE_BY_UUID,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_find_included_services(
            self, conn_handle=0, start_handle=0, end_handle=0):
        """aci_gatt_find_included_services"""
        data = ustruct.pack(
            "<HHH",
            conn_handle, start_handle, end_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_FIND_INCLUDED_SERVICES,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_disc_all_charac_of_serv(
            self, conn_handle=0, start_attr_handle=0, end_attr_handle=0):
        """aci_gatt_disc_all_charac_of_serv"""
        data = ustruct.pack(
            "<HHH",
            conn_handle, start_attr_handle, end_attr_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_DISC_ALL_CHARAC_OF_SERV,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_disc_charac_by_uuid(
            self, conn_handle=0, start_handle=0, end_handle=0,
            uuid_type=0, uuid=b''):
        """aci_gatt_disc_charac_by_uuid"""
        uuid_len = 2 if uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<HHHB{:d}s".format(uuid_len),
            conn_handle, start_handle, end_handle, uuid_type, uuid)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_DISC_CHARAC_BY_UUID,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_disc_all_charac_descriptors(
            self, conn_handle=0, char_val_handle=0, char_end_handle=0):
        """aci_gatt_disc_all_charac_descriptors"""
        data = ustruct.pack(
            "<HHH",
            conn_handle, char_val_handle, char_end_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_DISC_ALL_CHARAC_DESCRIPTORS,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_read_charac_val(self, conn_handle=0, attr_handle=0):
        """aci_gatt_read_charac_val"""
        data = ustruct.pack(
            "<HH",
            conn_handle, attr_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_READ_CHARAC_VAL,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_read_using_charac_uuid(
            self, conn_handle=0, start_handle=0, end_handle=0,
            uuid_type=0, uuid=b''):
        """aci_gatt_read_using_charac_uuid"""
        uuid_len = 2 if uuid_type == UUID_TYPE_16 else 16
        data = ustruct.pack(
            "<HHHB{:d}s".format(uuid_len),
            conn_handle, start_handle, end_handle, uuid_type, uuid)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_READ_USING_CHARAC_UUID,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_read_long_charac_val(
            self, conn_handle=0, attr_handle=0, val_offset=0):
        """aci_gatt_read_long_charac_val"""
        data = ustruct.pack(
            "<HHH",
            conn_handle, attr_handle, val_offset)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_READ_LONG_CHARAC_VAL,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_read_multiple_charac_val(
            self, conn_handle=0, num_handles=0, set_of_handles=b''):
        """aci_gatt_read_multiple_charac_val"""
        data = ustruct.pack(
            "<HB{:d}s".format(num_handles * 2),
            conn_handle, num_handles, set_of_handles)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_READ_MULTIPLE_CHARAC_VAL,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_write_charac_value(
            self, conn_handle=0, attr_handle=0, val_len=0, attr_value=b''):
        """aci_gatt_write_charac_value"""
        data = ustruct.pack(
            "<HHB{:d}s".format(val_len),
            conn_handle, attr_handle, val_len, attr_value)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_WRITE_CHAR_VALUE,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_write_long_charac_val(
            self, conn_handle=0, attr_handle=0, val_offset=0,
            val_len=0, attr_val=b''):
        """aci_gatt_write_long_charac_val"""
        data = ustruct.pack(
            "<HHHB{:d}s".format(val_len),
            conn_handle, attr_handle, val_offset, val_len, attr_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_WRITE_LONG_CHARAC_VAL,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_write_charac_reliable(
            self, conn_handle=0, attr_handle=0, val_offset=0,
            val_len=0, attr_val=b''):
        """aci_gatt_write_charac_reliable"""
        data = ustruct.pack(
            "<HHHB{:d}s".format(val_len),
            conn_handle, attr_handle, val_offset, val_len, attr_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_WRITE_CHARAC_RELIABLE,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_write_long_charac_desc(
            self, conn_handle=0, attr_handle=0,
            val_offset=0, val_len=0, attr_val=b''):
        """aci_gatt_write_long_charac_desc"""
        data = ustruct.pack(
            "<HHHB{:d}s".format(val_len),
            conn_handle, attr_handle, val_offset, val_len, attr_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_WRITE_LONG_CHARAC_DESC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_read_long_charac_desc(
            self, conn_handle=0, attr_handle=0, val_offset=0):
        """aci_gatt_read_long_charac_desc"""
        data = ustruct.pack(
            "<HHH",
            conn_handle, attr_handle, val_offset)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_READ_LONG_CHARAC_DESC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_write_charac_descriptor(
            self, conn_handle=0, attr_handle=0, val_len=0, attr_val=b''):
        """aci_gatt_write_charac_descriptor"""
        data = ustruct.pack(
            "<HHB{:d}s".format(val_len),
            conn_handle, attr_handle, val_len, attr_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_WRITE_CHAR_DESC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_read_charac_desc(self, conn_handle=0, attr_handle=0):
        """aci_gatt_read_charac_desc"""
        data = ustruct.pack(
            "<HH",
            conn_handle, attr_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_READ_CHAR_DESC,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_write_without_response(
            self, conn_handle=0, attr_handle=0, val_len=0, attr_val=b''):
        """aci_gatt_write_without_response"""
        data = ustruct.pack(
            "<HHB{:d}s".format(val_len),
            conn_handle, attr_handle, val_len, attr_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_WRITE_WITHOUT_RESPONSE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_signed_write_without_resp(
            self, conn_handle=0, attr_handle=0, val_len=0, attr_val=b''):
        """aci_gatt_signed_write_without_resp"""
        data = ustruct.pack(
            "<HHB{:d}s".format(val_len),
            conn_handle, attr_handle, val_len, attr_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_SIGNED_WRITE_WITHOUT_RESPONSE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_confirm_indication(self, conn_handle=0):
        """aci_gatt_confirm_indication"""
        data = ustruct.pack(
            "<H",
            conn_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_CONFIRM_INDICATION,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_write_response(
            self, conn_handle=0, attr_handle=0, write_status=False, err_code=0,
            att_val_len=0, att_val=b''):
        """aci_gatt_write_response"""
        data = ustruct.pack(
            "<HHBBB{:d}s".format(att_val_len),
            conn_handle, attr_handle, int(write_status), err_code, att_val_len,
            att_val)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_WRITE_RESPONSE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_allow_read(self, conn_handle=0):
        """aci_gatt_allow_read"""
        data = ustruct.pack(
            "<H",
            conn_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_ALLOW_READ,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_set_security_permission(
            self, service_handle=0, attr_handle=0, security_permission=0):
        """aci_gatt_set_security_permission"""
        data = ustruct.pack(
            "<HHB",
            service_handle, attr_handle, security_permission)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_SET_SECURITY_PERMISSION,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_set_desc_value(
            self, serv_handle=0, char_handle=0, char_desc_handle=0,
            char_desc_val_offset=0, char_desc_value_len=0, char_desc_value=b''):
        """aci_gatt_set_desc_value"""
        data = ustruct.pack(
            "<HHHHB{:d}s".format(char_desc_value_len),
            serv_handle, char_handle, char_desc_handle, char_desc_val_offset,
            char_desc_value_len, char_desc_value)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_SET_DESC_VAL,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_read_handle_value(self, attr_handle=0):
        """aci_gatt_read_handle_value"""
        data = ustruct.pack(
            "<H",
            attr_handle)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_READ_HANDLE_VALUE,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_read_handle_value_offset_IDB05A1(
            self, attr_handle=0, offset=0):
        """aci_gatt_read_handle_value_offset_IDB05A1"""
        data = ustruct.pack(
            "<HH",
            attr_handle, offset)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_READ_HANDLE_VALUE_OFFSET,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_gatt_update_char_value_ext_IDB05A1(
            self, service_handle=0, char_handle=0, update_type=0, char_length=0,
            value_offset=0, value_length=0, value=b''):
        """aci_gatt_update_char_value_ext_IDB05A1"""
        data = ustruct.pack(
            "<HHBHHB{:d}s".format(value_length),
            service_handle, char_handle, update_type, char_length,
            value_offset, value_length, value)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GATT_UPD_CHAR_VAL_EXT,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    ###########################################################################
    #                                HAL                                      #
    ###########################################################################

    def aci_hal_get_fw_build_number(self):
        """aci_hal_get_fw_build_number"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_GET_FW_BUILD_NUMBER)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_write_config_data(self, offset=0, length=0, data=b''):
        """aci_hal_write_config_data"""
        data = ustruct.pack(
            "<BB{:d}s".format(length),
            offset, length, data)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_WRITE_CONFIG_DATA,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_read_config_data(self, offset=0):
        """aci_hal_read_config_data"""
        data = ustruct.pack(
            "<B",
            offset)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_READ_CONFIG_DATA,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_set_tx_power_level(self, en_high_power=0, pa_level=0):
        """aci_hal_set_tx_power_level"""
        data = ustruct.pack(
            "<BB",
            en_high_power, pa_level)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_SET_TX_POWER_LEVEL,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_le_tx_test_packet_number(self):
        """aci_hal_le_tx_test_packet_number"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_LE_TX_TEST_PACKET_NUMBER)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_device_standby(self):
        """aci_hal_device_standby"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_DEVICE_STANDBY)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_tone_start(self, rf_channel=0):
        """aci_hal_tone_start"""
        data = ustruct.pack(
            "<B",
            rf_channel)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_TONE_START,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_tone_stop(self):
        """aci_hal_tone_stop"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_TONE_STOP)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_get_link_status(self):
        """aci_hal_get_link_status"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_GET_LINK_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_hal_get_anchor_period(self):
        """aci_hal_get_anchor_period"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_HAL_GET_ANCHOR_PERIOD)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    ###########################################################################
    #                                L2CAP                                    #
    ###########################################################################

    def aci_l2cap_connection_parameter_update_request(
            self, conn_handle=0, interval_min=0, interval_max=0,
            slave_latency=0, timeout_multiplier=0):
        """aci_l2cap_connection_parameter_update_request"""
        data = ustruct.pack(
            "<HHHHH",
            conn_handle, interval_min, interval_max, slave_latency,
            timeout_multiplier)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_L2CAP_CONN_PARAM_UPDATE_REQ,
            data=data,
            evtcode=EVT_CMD_STATUS)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_l2cap_connection_parameter_update_response_IDB05A1(
            self, conn_handle=0, interval_min=0, interval_max=0,
            slave_latency=0, timeout_multiplier=0,
            min_ce_length=0, max_ce_length=0, id_=0, accept=False):
        """aci_l2cap_connection_parameter_update_response_IDB05A1"""
        data = ustruct.pack(
            "<HHHHHHHBB",
            conn_handle, interval_min, interval_max, slave_latency,
            timeout_multiplier, min_ce_length, max_ce_length, id_, int(accept))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_L2CAP_CONN_PARAM_UPDATE_RESP,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_l2cap_connection_parameter_update_response_IDB04A1(
            self, conn_handle=0, interval_min=0, interval_max=0,
            slave_latency=0, timeout_multiplier=0, id_=0, accept=False):
        """aci_l2cap_connection_parameter_update_response_IDB04A1"""
        data = ustruct.pack(
            "<HHHHHBB",
            conn_handle, interval_min, interval_max, slave_latency,
            timeout_multiplier, id_, int(accept))
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_L2CAP_CONN_PARAM_UPDATE_RESP,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    ###########################################################################
    #                                UPDATER                                  #
    ###########################################################################

    def aci_updater_start(self):
        """aci_updater_start"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_START)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_updater_reboot(self):
        """aci_updater_reboot"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_REBOOT)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_get_updater_version(self):
        """aci_get_updater_version"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GET_UPDATER_VERSION)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_get_updater_buffer_size(self):
        """aci_get_updater_buffer_size"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_GET_UPDATER_BUFSIZE)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_erase_blue_flag(self):
        """aci_erase_blue_flag"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_ERASE_BLUE_FLAG)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_reset_blue_flag(self):
        """aci_reset_blue_flag"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_RESET_BLUE_FLAG)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_updater_erase_sector(self, address=0):
        """aci_updater_erase_sector"""
        data = ustruct.pack(
            "<I",
            address)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_ERASE_SECTOR,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_updater_program_data_block(self, address=0, data_len=0, data=b''):
        """aci_updater_program_data_block"""
        data = ustruct.pack(
            "<IH{:d}s".format(data_len),
            address, data_len, data)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_PROG_DATA_BLOCK,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_updater_read_data_block(self, address=0, data_len=0):
        """aci_updater_read_data_block"""
        data = ustruct.pack(
            "<IH",
            address, data_len)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_READ_DATA_BLOCK,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_updater_calc_crc(self, address=0, num_sectors=0):
        """aci_updater_calc_crc"""
        data = ustruct.pack(
            "<IH",
            address, num_sectors)
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_CALC_CRC,
            data=data)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd

    def aci_updater_hw_version(self):
        """aci_updater_hw_version"""
        hci_cmd = HCI_COMMAND(
            ogf=OGF_VENDOR_CMD,
            ocf=OCF_UPDATER_HW_VERSION)
        self.hci_send_cmd(hci_cmd)
        return hci_cmd
