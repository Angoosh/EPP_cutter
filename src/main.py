#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 23:16:12 2018

@author: angoosh
"""

import math
import serial
import instructions as ins
from time import sleep

ser = serial.Serial("/dev/ttyACM0")

"""
def parameter(b1, b2, b3, b4, b5, b6, b7, b8):
	CHECKSUM = b1+b2+b3+b4+b5+b6+b7+b8
	b9 = CHECKSUM
	if b9 > 256:
		i = b9/256
		i = math.floor(i)
		b9 = b9-i*256
	return(b1, b2, b3, b4, b5, b6, b7, b8, b9)
"""


def sender(b1, b2, b3, b4, b5, b6, b7, b8):
    CHECKSUM = b1+b2+b3+b4+b5+b6+b7+b8
    b9 = CHECKSUM
    if b9 > 256:
        i = b9/256
        i = math.floor(i)
        b9 = b9-i*256
    ser.write(bytearray([b1, b2, b3, b4, b5, b6, b7, b8, b9]))
    sleep(10)
    ser.write(bytearray([0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04])) #motor0 stop
    
sender(1,2,0,0,0,0,7,186)