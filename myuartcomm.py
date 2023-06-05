#!/usr/bin/python3

import serial
import time

def uart_init(portname="/dev/ttyS5", baudrate=115200, bytesize=8, parity='N', stopbits=1):
    serial_port = serial.Serial(portname, baudrate, bytesize, parity, stopbits)
    return serial_port

def send_data(boardport, data):
    write_count = boardport.write(data)
    #print(write_count)
    return

def recv_data(boardport):
    recved_data = bytearray()

    #print("waiting", end='', flush=True)
    while boardport.in_waiting ==0:
        time.sleep(0.002)
    #    print(".", end="", flush=True)
    #print("")

    while boardport.in_waiting > 0:
        recved_data.extend(boardport.read(boardport.in_waiting))
        time.sleep(0.01)

    #print("Recv: ", recved_data.hex(' '))
    return recved_data

def close_port(boardport):
    boardport.close()
    return

#ser = serial.Serial("/dev/ttyUSB0", 115200, 8, 'N', 1)
#recv_data(ser)
#ser.close()