#!/usr/bin/env python3

#skript automaticke kontroly a spusteni aplikace
import os
import subprocess
import time
import sys
import config

PATH = "logs/"
DAYS = config.glob()[7]

try:
    os.listdir(PATH)
except:
    os.system("mkdir "+PATH)

for i in range (0,3):
    
    #kontrola modulu
    try:
        import serial
    except:
        print("Module pyserial is not installed. Try: pip3 install pyserial\nand pip install pyserial")
        break
    
    #mazani starych log souboru
    now = time.time()
    for f in os.listdir(PATH):
        if os.stat(os.path.join(PATH,f)).st_mtime < now - DAYS*86400:
            os.system("rm "+str(os.path.join(PATH,f)))
    
    #login
    subprocess.call(["python3 Login.py"], shell = True)
        
    #kontrola, jestli bezi na RPi
    if os.path.exists("/home/pi"):
        subprocess.call(["clear"], shell = True)
        subprocess.call(["python3 CLI.py"], shell = True)
        break


    #kontrola, zda je zaple GUI os / ssh s parametrem -X a zda je nainstalovane kivy jinak se spusti CLI
    try:
        os.environ['DISPLAY']
        import kivy
        subprocess.call(["python3 CLI.py"], shell = True)
    except:
        subprocess.call(["clear"], shell = True)
        subprocess.call(["python3 CLI.py"], shell = True)
    break
