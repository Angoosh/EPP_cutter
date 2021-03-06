#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 23:53:30 2019

@author: angoosh
"""

import subprocess
import RPi.GPIO as GPIO
from time import sleep

#nastaveni GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

ip_cmd = "hostname -I"
#funkce ziskani ip adresy
def run(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

while True:
    try:
        try:
            ip = run(ip_cmd)
            IP = ip.split(".")
            IP = int(IP[3])
        except:
            ip = "0.0.0.0"
            print("No IP assigned or unknown iface")
        
        address = [0,0,0,0,0,0,0,0]
        
#predelani posledniho cisla IPv4 do binarniho formatu
        if IP >= 128:
            address[0] = 1
            IP = IP%128
        if IP >= 64:
            address[1] = 1
            IP = IP%64
        if IP >= 32:
            address[2] = 1
            IP = IP%32
        if IP >= 16:
            address[3] = 1
            IP = IP%16
        if IP >= 8:
            address[4] = 1
            IP = IP%8
        if IP >= 4:
            address[5] = 1
            IP = IP%4
        if IP >= 2:
            address[6] = 1
        address[7] = IP%2
#vykresleni IP adresy
        GPIO.output(5, address[0])
        GPIO.output(6, address[1])
        GPIO.output(13, address[2])
        GPIO.output(19, address[3])
        GPIO.output(26, address[4])
        GPIO.output(16, address[5])
        GPIO.output(20, address[6])
        GPIO.output(21, address[7])
        sleep(1)
    except:
        GPIO.cleanup()
        sleep(0.2)
    
