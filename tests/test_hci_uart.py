# -*- coding: utf-8 -*-
import logging

from bluetooth_low_energy.protocols.hci import (
    acl,
    att,
    cmd,
    event,
    l2cap,
    sco,
    smp,
    uart)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("test_hci_uart")


def test_hci_uart():
    buffers = (
        b'\x01\x03\x0c\x00',
        b'\x04\x13\x05\x01@\x00\x01\x00',
        b'\x02@ \x07\x00\x03\x00\x04\x00\x0b@\x04',
        b'\x01\x01\x10\x00',
        b'\x04\x0e\x0c\x01\x01\x10\x00\x07\x071\x070\x00\x13\x00',
        b'\x04>\x13\x01\x00\x01\x08\x01\x01\xc5l\x0c\xc36T\x18\x00\x00\x00H\x00\x05'
    )

    for buffer in buffers:
        log.debug("%s", buffer)
        hci_uart = uart.HCI_UART.from_buffer(buffer)
        if hci_uart.pkt_type == uart.COMMAND:
            hci_cmd = cmd.HCI_COMMAND.from_buffer(hci_uart.data)
            log.info("%s", hci_cmd)
        elif hci_uart.pkt_type == uart.ACLDATA:
            hci_acl = acl.HCI_ACL.from_buffer(hci_uart.data)
            log.info("%s", hci_acl)
            hci_l2cap = l2cap.L2CAP.from_buffer(hci_acl.data)
            log.info("%s", hci_l2cap)
            if hci_l2cap.cid == l2cap.L2CAP_CID_ATT:
                attp = att.ATT.from_buffer(hci_l2cap.data)
                log.info("%s", attp)
            elif hci_l2cap.cid == l2cap.L2CAP_CID_SMP:
                smpp = smp.SMP.from_buffer(hci_l2cap.data)
                log.info("%s", smpp)
            elif hci_l2cap.cid == (l2cap.L2CAP_CID_SCH, l2cap.L2CAP_CID_SCH):
                l2cap_sch = l2cap.L2CAP_SCH.from_buffer(hci_l2cap.data)
                log.info("%s", l2cap_sch)
        elif hci_uart.pkt_type == uart.SCODATA:
            hci_sco = sco.HCI_SCO.from_buffer(hci_uart.data)
            log.info("%s", hci_sco)
        elif hci_uart.pkt_type == uart.EVENT:
            hci_evt = event.HCI_EVENT.from_buffer(hci_uart.data)
            log.info("%s", hci_evt)

if __name__ == "__main__":
    test_hci_uart()
