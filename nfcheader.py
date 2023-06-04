#!/usr/bin/python3

from myuartcomm import *

# Data direction
__HOSTtoPN532 = 0xD4

# frame strcuture header and tailor
_PREAMBLE       = 0x00
_STARTCODE1     = 0x00
_STARTCODE2     = 0xFF
_POSTAMBLE      = 0x00

# PN532 commands
__CMD_SAMCONFIGURATION  = 0x14

_WAKE_UP               = 0x55


class PN532_board:


    def __init__(self, comm_type="UART", portname="/dev/ttyS5", baudrate=115200, bytesize=8, parity='N', stopbits=1):

        if comm_type == "UART" or comm_type == "uart" or comm_type == 'serial':
            self.portobj = uart_init(portname, baudrate, bytesize, parity, stopbits)
        else:
            raise NotImplementedError

    def wake_up(self):
        wake_up_frame = bytearray(24);
        wake_up_frame[0]        = _WAKE_UP;
        wake_up_frame[1]        = _WAKE_UP;
        wake_up_frame[-1]       = _POSTAMBLE;
        wake_up_frame[-9:-2]    = bytearray.fromhex("00 FF 03 FD D4 14 01 17")

        print("wake_up_frame: ",wake_up_frame)
        
        send_data(self.portobj, wake_up_frame)
        wakeup_ack_frame = recv_data(self.portobj)

        print(wakeup_ack_frame.hex(' '))

        return
    
    def det_card(self):
        start_det_frame = bytearray(11)
        start_det_frame[0]  = _PREAMBLE;
        start_det_frame[1]  = _STARTCODE1;
        start_det_frame[2]  = _STARTCODE2;
        start_det_frame[-1] = _POSTAMBLE
        start_det_frame[3:-1] = bytearray.fromhex("04 FC D4 4A 01 00 E1")
        
        print("start_det_frame: ", start_det_frame)

        send_data(self.portobj, start_det_frame)

        recv_ack =recv_data(self.portobj)
        print(recv_ack.hex(' '))

        card_info = recv_data(self.portobj)
        print(card_info.hex(' '))

        return