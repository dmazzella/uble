# uble

Lightweight Bluetooth Low Energy driver written in pure python for micropython.

WARNING: this project is in beta stage and is subject to changes of the
code-base, including project-wide name changes and API changes.

Features
---------------------

- Parsing and Building of HCI packets
- Allows PyBoard to control BLE chips using HCI packets

Usage
---------------------

- Parsing of HCI packets:

        MicroPython v1.8.7-79-g221f88d-dirty on 2017-01-26; PYBv1.1 with STM32F405RG
        Type "help()" for more information.
        >>> from bluetooth_low_energy.protocols.hci import (cmd, uart)
        >>> buf = b'\x01\x03\x0c\x00'
        >>> hci_uart = uart.HCI_UART.from_buffer(buf)
        >>> print(hci_uart)
        <HCI_UART pkt_type=COMMAND(0x01) data=030c00>
        >>> hci_cmd = cmd.HCI_COMMAND.from_buffer(hci_uart.data)
        >>> print(hci_cmd)
        <HCI_COMMAND opcode=0x0c03 ogf=HOST_CTL(0x03) ocf=RESET(0x03) request_data= response_data=>
        >>> hci_cmd.to_buffer()
        b'\x03\x0c\x00'        
        >>>

        
- Building of HCI Packets:

        MicroPython v1.8.7-79-g221f88d-dirty on 2017-01-26; PYBv1.1 with STM32F405RG
        Type "help()" for more information.
        >>> from bluetooth_low_energy.protocols.hci import cmd
        >>> hci_cmd = cmd.HCI_COMMAND(ogf=cmd.OGF_LE_CTL, ocf=cmd.OCF_LE_RAND)
        >>> print(hci_cmd)
        <HCI_COMMAND opcode=0x2018 ogf=LE_CTL(0x08) ocf=LE_RAND(0x18) request_data= response_data=>
        >>> hci_cmd.to_buffer()
        b'\x18 \x00'
        >>>

- Control BLE chips see 'examples'

Software
---------------------

Currently implemented full HCI commands from [STSW-BLUENRG-DK 2.0.2](http://www.st.com/en/embedded-software/stsw-bluenrg-dk.html)

User manual [BlueNRG-MS Bluetooth® LE stack application command interface](http://www.st.com/resource/en/user_manual/dm00162667.pdf)

Programming manual [BlueNRG, BlueNRG-MS stacks programming guidelines](http://www.st.com/resource/en/programming_manual/dm00141271.pdf)


Hardware
---------------------

Currently supported module STMicroelectronics [SPBTLE-RF](http://www.st.com/en/wireless-connectivity/spbtle-rf.html) 

From STMicroelectronics [X-NUCLEO-IDB05A1](http://www.st.com/en/ecosystems/x-nucleo-idb05a1.html):

<img src="https://raw.githubusercontent.com/dmazzella/uble/master/hardware/MicroPython_SPBTLERF_Breakout_v01/X_Nucleo_IDB05A1_mbed_pinout_v1.jpg" width="80%" height="80%" alt="X_Nucleo_IDB05A1_mbed_pinout_v1"/>

or

Availabe breakout board:
</br>
<table>
  <tr>
    <th>
        <img src="https://github.com/dmazzella/uble/raw/master/hardware/MicroPython_SPBTLERF_Breakout_v01/MicroPython_SPBTLERF_Breakout_v01_mod_TOP.png" width="30%" height="30%" alt="MicroPython_SPBTLERF_Breakout_v01_mod_TOP"/>
    <img src="https://github.com/dmazzella/uble/raw/master/hardware/MicroPython_SPBTLERF_Breakout_v01/MicroPython_SPBTLERF_Breakout_v01_mod_BOTTOM.png" width="30%" height="30%" alt="MicroPython_SPBTLERF_Breakout_v01_mod_BOTTOM"/>
    </th>
    <th>
    <a href="https://oshpark.com/shared_projects/ST79grRm"><img src="https://oshpark.com/assets/badge-5b7ec47045b78aef6eb9d83b3bac6b1920de805e9a0c227658eac6e19a045b9c.png" alt="Order from OSH Park"/></a>
    </th>
  </tr>
</table>
</br>


Fritzing for breakout: [MicroPython_SPBTLERF_Breakout_v01_mod.fzz](https://github.com/dmazzella/uble/raw/master/hardware/MicroPython_SPBTLERF_Breakout_v01/MicroPython_SPBTLERF_Breakout_v01_mod.fzz)


Gerber for breakout: [MicroPython_SPBTLERF_Breakout_v01_mod.zip](https://github.com/dmazzella/uble/raw/master/hardware/MicroPython_SPBTLERF_Breakout_v01/MicroPython_SPBTLERF_Breakout_v01_mod.zip)

If have interest into preassembled breakout board contact me at damianomazzella@gmail.com

External dependencies
---------------------

Only for examples:
'logging' already available into folder 'micropython-lib' of this repository

Install 'bluetooth_low_energy' into the pyboard
---------------------

To enable the functionality you need to freeze the package 'bluetooth_low_energy',
to do this, copy the package 'bluetooth_low_energy' into 'micropython-lib'.

Navigate to the folder containing the repository [micropython](https://github.com/micropython/micropython):

        $ cd stmhal
        $ make FROZEN_MPY_DIR="~/uble/micropython-lib"


Examples
---------------------

        basic: print BlueNRG FW versions
        bluest_protocol: implements the BlueST protocol usable for test with 'ST BlueMS' app
        eddystone: implement an Eddystone Beacon device
        sensor_demo: usable for test with 'BlueNRG' app
        firmware_update: update SPBTLE-RF firmware (see README)
        
