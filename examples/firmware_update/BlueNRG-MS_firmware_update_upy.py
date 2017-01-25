import os
from binascii import hexlify

## Program constants
SECTOR_SIZE = 2048     # Flash sector size
BASE_ADDRESS = 0x10010000
FW_OFFSET = 0
FULL_STACK_SIZE = (66*1024) # 66 KB (including IFR)
IFR_OFFSET = (64*1024) # IFR sector will contain both code and IFR data
IFR_DATA_SIZE = 192
BLUEFLAG_OFFSET = 0x8C0

DATA_SIZE = 64        # 64 bytes

def generate_csv_firmware(fw_filename, ifr_filename):

    csv_filename = os.path.basename(fw_filename.replace('.img', '.csv'))
    with open(fw_filename, 'r') as fw_file:
        fw_image = []
        for line in fw_file:
            fw_image.append(int(line[6:], 16))
            fw_image.append(int(line[4:6], 16))
            fw_image.append(int(line[2:4], 16))
            fw_image.append(int(line[:2], 16))

    # Read IFR file
    with open(ifr_filename, 'r') as ifr_file:
        ifr_data = []
        for line in ifr_file:
            ifr_data.append(int(line[6:], 16))
            ifr_data.append(int(line[4:6], 16))
            ifr_data.append(int(line[2:4], 16))
            ifr_data.append(int(line[:2], 16))

    # Take last 192 bytes and add replace them in the firmware image
    fw_image = fw_image[:-IFR_DATA_SIZE] + ifr_data[-IFR_DATA_SIZE:]

    # Patch image to set blue flag to 0xFFFFFFFF
    fw_image[BLUEFLAG_OFFSET] = 0xFF
    fw_image[BLUEFLAG_OFFSET+1] = 0xFF
    fw_image[BLUEFLAG_OFFSET+2] = 0xFF
    fw_image[BLUEFLAG_OFFSET+3] = 0xFF

    # Calculate the number of sectors necessary to contain the fw image.
    number_sectors = ((len(fw_image) + SECTOR_SIZE - 1) // SECTOR_SIZE)
    with open(csv_filename, "wb") as file_out:
        for i in range(FW_OFFSET, (number_sectors * SECTOR_SIZE), SECTOR_SIZE):
            for j in range(i, SECTOR_SIZE+i, DATA_SIZE):
                file_out.write(hexlify(bytearray(fw_image[j:j+DATA_SIZE])))
                file_out.write(b'\n')
    print("CSV Firmware: {:s}".format(csv_filename))

def main():
    fw_version = "7.2c"
    fw_filename = r"c:\Program Files (x86)\STMicroelectronics\BlueNRG GUI 2.2.1\Firmware\BlueNRG-MS_stack\bluenrg_7_2_c_Mode_2-32MHz-XO32K_4M.img"
    # IFR is included in the .img above, but customers may would like to update it according to their specific board, the example show the good IFR for ST EVal kit.
    ifr_filename = r"c:\Program Files (x86)\STMicroelectronics\BlueNRG GUI 2.2.1\Firmware\BlueNRG-MS_stack\ifr_3v1_003_mode02-32MHz-XO32K_4M.dat"
    generate_csv_firmware(fw_filename, ifr_filename)

main()