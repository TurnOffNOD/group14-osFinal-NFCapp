#!/usr/bin/python3

import serial

def uart_init(portname="/dev/ttyS5", baudrate=115200, bytesize=8, parity='N', stopbits=1):
    serial_port = serial.Serial(portname, baudrate, bytesize, parity, stopbits)
    return serial_port

def send_data(board, data):
    write_count = board.write(data)
    #print(write_count)
    return

def recv_data(board):
    while board.in_waiting == 0:
        #print("Waiting for data")
        pass
    
    recv_data =board.read(board.in_waiting)
    #print("Recv: ", recv_data)
    return recv_data