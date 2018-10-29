#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 08:15:34 2018

@author: angoosh
"""

import instructions as i
from byteparams import parameter as par
import serial
#from GUI.Widgets import __init__ as gui

def connection(port):
    try:
        #port = "/dev/ttyACM0"
        ser = serial.Serial(port)
        print("Connected")
        return ser
    except:
        print(port + " does not exist")
        ser = ""
        return ser
    



mode = "ABS"


def G0(X, Y, Z, A):
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,0,X)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,1,Y)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,2,Z)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    z = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,3,A)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    return(x, y, z, a)
    
def G1(X, Y, Z, A):
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,0,X)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,1,Y)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,2,Z)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    z = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,3,A)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    return(x, y, z, a)
    
def G28():
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,0,0,0,0,0)
    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,1,0,0,0,0)
    y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,2,0,0,0,0)
    z = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,3,0,0,0,0)
    a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    return(x, y, z, a)
    
def G90():
    mode = "ABS"
    return(mode)
    
def G91():
    mode = "REL"
    return(mode)
        
def M104(temp):
    return(temp)
    