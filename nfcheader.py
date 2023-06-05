#!/usr/bin/env python3

from myuartcomm import *

_DEBUG = False

# Data direction
_HOSTtoPN532 = 0xD4

# frame strcuture header and tailor
_PREAMBLE       = 0x00
_STARTCODE1     = 0x00
_STARTCODE2     = 0xFF
_POSTAMBLE      = 0x00

# PN532 commands
_CMD_SAMConfiguration   = 0x14
_WAKE_UP                = 0x55
_CMD_InDataExchange     = 0x40

# Card commands
_AUTH_WITH_KEY_A   = 0x60
_AUTH_WITH_KEY_B   = 0x61
_CMD_CARD_READ     = 0x30


class PN532_board:

    def __init__(self, comm_type="UART", portname="/dev/ttyS5", baudrate=115200, bytesize=8, parity='N', stopbits=1):

        if comm_type == "UART" or comm_type == "uart" or comm_type == 'serial':
            self.portobj = uart_init(portname, baudrate, bytesize, parity, stopbits)
        else:
            raise NotImplementedError

    def wake_up(self):
        wake_up_frame = bytearray(24);
        wake_up_frame[0]        = _WAKE_UP
        wake_up_frame[1]        = _WAKE_UP
        wake_up_frame[-1]       = _POSTAMBLE
        wake_up_frame[-9]       = _STARTCODE1
        wake_up_frame[-8]       = _STARTCODE2
        wake_up_frame[-7:-1]    = bytearray.fromhex("03 FD D4 14 01 17")
        
        if _DEBUG == True:
            print("wake_up_frame: ",wake_up_frame.hex(' ').upper())
        
        send_data(self.portobj, wake_up_frame)
        wakeup_ack_frame = recv_data(self.portobj)

        if _DEBUG == True:
            print("wakeup_ack_frame: ", wakeup_ack_frame.hex(' '))

        return
    
    def det_card(self):
        start_det_frame = bytearray(11)
        start_det_frame[0]  = _PREAMBLE;
        start_det_frame[1]  = _STARTCODE1;
        start_det_frame[2]  = _STARTCODE2;
        start_det_frame[-1] = _POSTAMBLE
        start_det_frame[3:-1] = bytearray.fromhex("04 FC D4 4A 01 00 E1")
        
        if _DEBUG == True:
            print("start_det_frame: ", start_det_frame)

        send_data(self.portobj, start_det_frame)

        recv_ack =recv_data(self.portobj)
        if _DEBUG == True:
            print(recv_ack.hex(' '))

        card_info = recv_data(self.portobj)
        if _DEBUG == True:
            print(card_info.hex(' '))

        return card_info

    def auth_card(self, blk_num, key_num, key, uid):

        if _DEBUG == True:
            print("uid: ", uid.hex(" "))
            print("key: ", key.hex(" "))
            print("key_num: ", key_num)
            print("blk_num: ", blk_num)

        uid_len = len(uid)
        key_len = len(key)

        card_auth_frame = bytearray(2 + uid_len + key_len)
        card_auth_frame[0]   = key_num & 0xFF
        card_auth_frame[1]   = blk_num & 0xFF
        card_auth_frame[2: 2+key_len]   = key
        card_auth_frame[2+key_len: ]    = uid

        if _DEBUG == True:
            print("card_auth_frame: ", card_auth_frame.hex(" "))
        
        auth_frame = bytearray(len(card_auth_frame) + 10)
        auth_frame[0]   = _PREAMBLE
        auth_frame[1]   = _STARTCODE1
        auth_frame[2]   = _STARTCODE2
        checksum        = sum(auth_frame[0:3])
        auth_frame[3]   = len(card_auth_frame) +3
        auth_frame[4]   = (~auth_frame[3] +1) & 0xFF
        auth_frame[5]   = _HOSTtoPN532
        auth_frame[6]   = _CMD_InDataExchange
        auth_frame[7]   = 0x01
        auth_frame[8: 8 + len(card_auth_frame)] = card_auth_frame
        checksum        += sum(auth_frame[5:-2])
        if _DEBUG == True:
            print("checksum to be bitnot+1: ", hex(checksum))
        #auth_frame[-2]  = (~checksum +1) & 0xFF
        auth_frame[-2]  = (~checksum) & 0xFF    #When sums up [0:3], no need to plus 1
        auth_frame[-1]  = _POSTAMBLE

        #auth_frame =bytearray.fromhex("00 00 FF 04 FC D4 4A 01 00 E1 00")

        if _DEBUG == True:
            print("auth_send_frame: ", auth_frame.hex(" "))

        send_data(self.portobj, auth_frame)

        auth_ack = recv_data(self.portobj)
        if _DEBUG == True:
            print("auth_ack: ", auth_ack.hex(" "))

        return auth_ack
    
    def read_card_data(self, blk_num=0, key_num=_AUTH_WITH_KEY_B, key=0xFFFFFFFFFFFF, uid=0x01234567):

        auth_result = self.auth_card(blk_num, key_num, key, uid)
        #print("auth_result: ", auth_result.hex(' '))

        card_readcmd_frame = bytearray(2)
        card_readcmd_frame[0]   = _CMD_CARD_READ
        card_readcmd_frame[1]   = blk_num
        
        if _DEBUG == True:
            print(card_readcmd_frame)

        read_card_frame     = bytearray(len(card_readcmd_frame) + 10)
        read_card_frame[0]  = _PREAMBLE
        read_card_frame[1]  = _STARTCODE1
        read_card_frame[2]  = _STARTCODE2
        read_card_frame[3]  = len(card_readcmd_frame) + 3
        read_card_frame[4]  = (~read_card_frame[3] +1) & 0xFF
        read_card_frame[5]  = _HOSTtoPN532
        read_card_frame[6]  = _CMD_InDataExchange
        read_card_frame[7]  = 0x01
        read_card_frame[8: 8+len(card_readcmd_frame)] =card_readcmd_frame
        checksum            = sum(read_card_frame[5:-2])
        read_card_frame[-2] = (~checksum +1) & 0xFF
        read_card_frame[-1] =_POSTAMBLE

        if _DEBUG == True:
            print("read_card_frame: ", read_card_frame.hex(' '))
        
        send_data(self.portobj, read_card_frame)
        card_data_recv = recv_data(self.portobj)

        return card_data_recv[14:-2]


    def finishjob(self):
        close_port(self.portobj)
        return
