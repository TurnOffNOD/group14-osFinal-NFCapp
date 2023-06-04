#!/usr/bin/python3

import nfcheader
import serial

comm_method = "UART"
comm_dev    = "/dev/ttyS5"
baudrate    = 115200
bytesize    = 8
pairity     = 'N'
stopbits    = 1

os_final_exp3_nfc = nfcheader.PN532_board(comm_method, comm_dev, baudrate, bytesize, pairity, stopbits)

os_final_exp3_nfc.wake_up()
os_final_exp3_nfc.det_card()
