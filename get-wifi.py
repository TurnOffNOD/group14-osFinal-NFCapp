#!/usr/bin/env python3

import nfcheader
from nfcheader import _DEBUG
#print(_DEBUG)
import serial
import argparse
import ndef

get_opts = argparse.ArgumentParser(description='avoid duplicate wake up with args')

get_opts.add_argument('--wakeup', type=bool, default=False, help="set it to boolean True when need to wake up")

args = get_opts.parse_args()

comm_method = "UART"
comm_dev    = "/dev/ttyS5"
baudrate    = 115200
bytesize    = 8
pairity     = 'N'
stopbits    = 1

card_key_b = bytearray.fromhex("FFFFFFFFFFFF")
#card_key_a = b'\xFF\xFF\xFF\xFF\xFF\xFF'
#print(card_key_a.hex())

os_final_exp3_nfc = nfcheader.PN532_board(comm_method, comm_dev, baudrate, bytesize, pairity, stopbits)

if args.wakeup:
    os_final_exp3_nfc.wake_up()

card_uid = os_final_exp3_nfc.det_card()[13:-2]
#card_uid = bytearray.fromhex("01234567")
print(card_uid.hex(' '))

data = bytearray()

for blk_i in range(4, 64):
    if blk_i % 4 == 3:
        continue
    data += os_final_exp3_nfc.read_card_data(blk_num=blk_i, key=card_key_b, uid=card_uid)
    
    if _DEBUG == True:
        print(blk_i, ": ", data)

data = data[2:]
#print("data from card: ")
#print(len(data))
#print(data.hex(' '))

os_final_exp3_nfc.finishjob()

data_prased = ndef.message_decoder(data)
d=[]
while True:
    try:
        d.append(next(data))
    except StopIteration:
        break
print(d)
