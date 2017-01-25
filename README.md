# uble

Lightweight Bluetooth Low Energy driver written in pure python for micropython

WARNING: this project is in beta stage and is subject to changes of the
code-base, including project-wide name changes and API changes.

Software
---------------------

Currently implemented full HCI commands from [STSW-BLUENRG-DK 2.0.2](http://www.st.com/en/embedded-software/stsw-bluenrg-dk.html)

Hardware
---------------------

Currently supported module STMicroelectronics [SPBTLE-RF](http://www.st.com/en/wireless-connectivity/spbtle-rf.html) 

Fritzing link for breakout: TODO

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
        sensor_demo: usable for test with 'BlueNRG' app
        firmware_update: update SPBTLE-RF firmware (see README)
        
