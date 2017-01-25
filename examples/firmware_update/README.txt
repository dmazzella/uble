FIRMWARE UPDATE:
1) edit the script "BlueNRG-MS_firmware_update_upy.py":
    - fw_version = "7.2c"
    - fw_filename = "bluenrg_7_2_c_Mode_2-32MHz-XO32K_4M.img"
    - ifr_filename = "ifr_3v1_003_mode02-32MHz-XO32K_4M.dat"
2) run the script on pc  "BlueNRG-MS_firmware_update_upy.py"
3) Copiare il file generato sulla PyBoard:
    Es. "bluenrg_7_2_c_Mode_2-32MHz-XO32K_4M.csv"
4) edit the script "firmware_update.py":
    - FW_FILENAME = "bluenrg_7_2_c_Mode_2-32MHz-XO32K_4M.csv"
5) copy the script "firmware_update.py" and "bluenrg_7_2_c_Mode_2-32MHz-XO32K_4M.csv" on the PyBoard
6) run the script "firmware_update.py" on PyBoard:
    MicroPython v1.8.6-6-g1375c52-dirty on 2016-11-11; PYBv1.0 with STM32F405RG
    Type "help()" for more information.
    >>> from firmware_update import FirmwareUpdate
    >>> ble = FirmwareUpdate()
    >>> ble.run()    
