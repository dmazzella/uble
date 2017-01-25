# -*- coding: utf-8 -*-
from bluetooth_low_energy.protocols.hci import \
    cmd

def test_hci_command():
    names = (
        (cmd.OGF_LINK_CTL, cmd.OCF_DISCONNECT),
        (cmd.OGF_HOST_CTL, cmd.OCF_RESET),
        (cmd.OGF_HOST_CTL, cmd.OCF_READ_TRANSMIT_POWER_LEVEL),
        (cmd.OGF_INFO_PARAM, cmd.OCF_READ_LOCAL_VERSION),
        (cmd.OGF_INFO_PARAM, cmd.OCF_READ_BD_ADDR),
        (cmd.OGF_STATUS_PARAM, cmd.OCF_READ_RSSI),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_READ_BUFFER_SIZE),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_SET_ADV_PARAMETERS),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_SET_ADV_DATA),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_SET_ADVERTISE_ENABLE),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_SET_SCAN_PARAMETERS),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_SET_SCAN_ENABLE),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_RAND),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_SET_SCAN_RESPONSE_DATA),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_READ_ADV_CHANNEL_TX_POWER),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_SET_RANDOM_ADDRESS),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_CREATE_CONN),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_CREATE_CONN_CANCEL),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_ENCRYPT),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_LTK_REPLY),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_LTK_NEG_REPLY),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_READ_WHITE_LIST_SIZE),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_CLEAR_WHITE_LIST),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_ADD_DEVICE_TO_WHITE_LIST),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_REMOVE_DEVICE_FROM_WHITE_LIST),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_READ_LOCAL_SUPPORTED_FEATURES),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_READ_CHANNEL_MAP),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_READ_SUPPORTED_STATES),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_RECEIVER_TEST),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_TRANSMITTER_TEST),
        (cmd.OGF_LE_CTL, cmd.OCF_LE_TEST_END)
    )
    for ogf, ocf in names:
        hci_command = cmd.HCI_COMMAND(ogf=ogf, ocf=ocf)
        print(hci_command)

if __name__ == "__main__":
    test_hci_command()
