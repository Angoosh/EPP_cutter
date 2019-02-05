#!/usr/bin/env python3

#skript automaticke kontroly a spusteni aplikace
import os
import subprocess

for i in range (0,3):
    
    #kontrola modulu
    try:
        import serial
    except:
        print("Module pyserial is not installed. Try: pip3 install pyserial\nand pip install pyserial")
        break
    
    #kontrola, jestli bezi na RPi
    if os.path.exists("/home/pi"):
        subprocess.call(["clear"], shell = True)
        subprocess.call(["python3 CLI.py"], shell = True)
        break

    #login
    subprocess.call(["python3 Login.py"], shell = True)
    
    #kontrola, zda je zaple GUI os / ssh s parametrem -X a zda je nainstalovane kivy jinak se spusti CLI
    try:
        os.environ['DISPLAY']
        import kivy
        subprocess.call(["python3 GUI.py"], shell = True)
    except:
        subprocess.call(["clear"], shell = True)
        subprocess.call(["python3 CLI.py"], shell = True)
    break
