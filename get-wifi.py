#!/usr/bin/python3

import nfcheader
import serial
import argparse

comm_method = "UART"
comm_dev    = "/dev/ttyS5"
baudrate    = 115200
bytesize    = 8
pairity     = 'N'
stopbits    = 1

os_final_exp3_nfc = nfcheader.PN532_board(comm_method, comm_dev, baudrate, bytesize, pairity, stopbits)

get_opts = argparse.ArgumentParser(description='avoid duplicate wake up with args')

get_opts.add_argument('--wakeup', type=bool, default=False, help="set it to boolean True when need to wake up")

args = get_opts.parse_args()

if args.wakeup:
    os_final_exp3_nfc.wake_up()

os_final_exp3_nfc.det_card()
