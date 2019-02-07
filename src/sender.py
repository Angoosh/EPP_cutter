
"""
Must run on python 3 
"""

import serial
from byteparams import parameter as par
import instructions as i
import Gcode
import pickle
from time import sleep
import os
import subprocess

#cteni konfiguracniho souboru
f = open("comm.pickle", "rb")
serPort = pickle.load(f)
file = pickle.load(f)
f.close()

#ziskani informaci o procesu a nasledne zapsani do souboru
pid = os.getpid()
f = open("comm.pickle", "wb")
pickle.dump(pid, f)
f.close()
sleep(1)

#zapnuti EMERGENCY tlacitka
if os.path.exists("/home/pi") or os.path.exists("/home/rpi"):
    subprocess.call("python3 EMERGENCY.py &", shell = True)
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
else:
    print("Not running on RPi")

#pripojeni k portu
try:
    ser = serial.Serial(serPort)
except:
    print("No such serial port as: " + serPort)
    os.system("kill "+str(pid))
#deklarace globalnich promennych
proceed = 0
mode = "ABS"
feed = 2047
lastx, lasty, lasta, lastb = 0, 0, 0, 0
st = 0.0001 #delay mezi posilanim dat

#load emergency procesu
sleep(1)
f = open("emergency.pickle", "rb")
emerg_pid = pickle.load(f)
f.close()

#funkce pro threading
def wait_until_reached():
    while True:
        global proceed
        r = ser.read(9)
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x01\x0e':
            proceed = 0
            break
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x02\x0f':
            proceed = 0
            break
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x04\x11':
            proceed = 0
            break
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x08\x15':
            proceed = 0
            break

#rozlysovani jednotlivych prikazu gcodu
def action(r):
    r = r.decode("utf-8")
    global mode
    global st
    global proceed
    global lastx, lasty, lasta, lastb
    global feed
    if r.find("G0") != -1:
        x = r.find("X")
        y = r.find("Y")
        a = r.find("A")
        b = r.find("B")
        if (x == -1) or (y == -1) or (a == -1) or (b == -1):
            return
        try:
            xx = float(r[x+1:y-1])
            yy = float(r[y+1:a-1])
            aa = float(r[a+1:b-1])
            bb = float(r[b+1:])
        except:
            return
        x, y, a, b = Gcode.G0(xx, yy, aa, bb)
        nx = abs(xx-lastx)
        ny = abs(yy-lasty)
        na = abs(aa-lasta)
        nb = abs(bb-lastb)
        mx = max(nx, ny, na, nb)
#------------------------------interpolation--------------------------------------------
        fx, fy, fa, fb = nx, ny, na, nb
        if mx == 0:
            mx = 1
        if fx == 0:
            fx = mx
        if fy == 0:
            fy = mx
        if fa == 0:
            fa = mx
        if fb == 0:
            fb = mx
        fx = int(feed/(mx/fx))
        fy = int(feed/(mx/fy))
        fa = int(feed/(mx/fa))
        fb = int(feed/(mx/fb))
        
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 0, fx)
        b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(st)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 1, fy)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(st)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 2, fa)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(st)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 3, fb)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(st)
#---------------------------interpolation-end-------------------------------------------     
        lastx, lasty, lasta, lastb = xx, yy, aa, bb
        if nx == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
            sleep(st)
            ser.write(x)
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(b)
            pass
        elif ny == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(x)
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(b)
            pass
        elif na == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(x)
            sleep(st)
            ser.write(b)
            pass
        else:
            ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
            sleep(st)
            ser.write(b)
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(x)
            pass
    elif r.find("G1") != -1:
        x = r.find("X")
        y = r.find("Y")
        a = r.find("A")
        b = r.find("B")
        if (x == -1) or (y == -1) or (a == -1) or (b == -1):
            return
        try:
            xx = float(r[x+1:y-1])
            yy = float(r[y+1:a-1])
            aa = float(r[a+1:b-1])
            bb = float(r[b+1:])
        except:
            return
        x, y, a, b = Gcode.G0(xx, yy, aa, bb)
        nx = abs(xx-lastx)
        ny = abs(yy-lasty)
        na = abs(aa-lasta)
        nb = abs(bb-lastb)
        mx = max(nx, ny, na, nb)
#------------------------------interpolation--------------------------------------------
        fx, fy, fa, fb = nx, ny, na, nb
        if mx == 0:
            mx = 1
        if fx == 0:
            fx = mx
        if fy == 0:
            fy = mx
        if fa == 0:
            fa = mx
        if fb == 0:
            fb = mx
        fx = int(feed/(mx/fx))
        fy = int(feed/(mx/fy))
        fa = int(feed/(mx/fa))
        fb = int(feed/(mx/fb))
        
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 0, fx)
        b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(st)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 1, fy)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(st)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 2, fa)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(st)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 3, fb)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(st)
#---------------------------interpolation-end-------------------------------------------
        lastx, lasty, lasta, lastb = xx, yy, aa, bb
        if nx == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
            sleep(st)
            ser.write(x)
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(b)
            print("first")
            pass
        elif ny == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(x)
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(b)
            print("second")
            pass
        elif na == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(x)
            sleep(st)
            ser.write(b)
            print("third")
            pass
        else:
            ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
            sleep(st)
            ser.write(b)
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(x)
            print("fourth")
            pass
    elif r.find("G28") != -1:
        for motor in range (0,4):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(193,motor,1)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(194,motor,2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            s = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(s)
            sleep(st)
        x, y, a, b = Gcode.G28()
        ser.write(x)
        sleep(st)
        ser.write(y)
        sleep(st)
        ser.write(a)
        sleep(st)
        ser.write(b)
        sleep(st)
    elif r.find("G90") != -1:
        global mode
        mode = Gcode.G90()
    elif r.find("G91") != -1:
        mode = Gcode.G91()
    elif r.find("M104") != -1:
        a = r.find("S")
        if a == -1:
            return
        temp = int(r[a+1:])
        heat, send = Gcode.M104(temp)
        ser.write(send)
        sleep(st)
    elif r.find("MST") != -1:
        for motor in range (0,4):
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,3, 0, motor, 0, 0, 0, 0)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            sleep(st)
    elif r == "":
        nothing, temp = Gcode.M104(0)
        if os.path.exists("/home/pi") or os.path.exists("/home/rpi"):
            os.system("kill "+str(emerg_pid))
            GPIO.output(4, GPIO.LOW)
        ser.write(temp)
    elif r == "#":
        nothing, temp = Gcode.M104(0)
        if os.path.exists("/home/pi") or os.path.exists("/home/rpi"):
            os.system("kill "+str(emerg_pid))
            GPIO.output(4, GPIO.LOW)
        ser.write(temp)
    else:
        nothing, temp = Gcode.M104(0)
        if os.path.exists("/home/pi") or os.path.exists("/home/rpi"):
            os.system("kill "+str(emerg_pid))
            GPIO.output(4, GPIO.LOW)
        ser.write(temp)


with open(file, "rb") as t:
    for line in t:
        print(line)
        a = line.decode("utf-8")
        if (a.find("G0") != -1) or (a.find("G1") != -1):
            action(line)
            while True:
                r = ser.read(9)
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x01\x0e':
                    break
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x02\x0f':
                    break
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x04\x11':
                    break
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x08\x15':
                    break
        elif a.find("G28") != -1:
            action(line)
            Xh = 0
            Yh = 0
            Ah = 0
            Bh = 0
            while True:
                b2,b3,b4,b5,b6,b7,b8 = i.GAP(11,0)
                b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
                x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                ser.write(x)
                a = ser.read(9)
                if a == b'\x02\x01\x64\x06\x00\x00\x00\x01\x6e':
                    Xh = 1
                else:
                    Xh = 0
                sleep(0.1)
                b2,b3,b4,b5,b6,b7,b8 = i.GAP(11,1)
                b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
                x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                ser.write(x)
                a = ser.read(9)
                if a == b'\x02\x01\x64\x06\x00\x00\x00\x01\x6e':
                    Yh = 1
                else:
                    Yh = 0
                sleep(0.1)
                b2,b3,b4,b5,b6,b7,b8 = i.GAP(11,2)
                b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
                x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                ser.write(x)
                a = ser.read(9)
                if a == b'\x02\x01\x64\x06\x00\x00\x00\x01\x6e':
                    Ah = 1
                else:
                    Ah = 0
                sleep(0.1)
                b2,b3,b4,b5,b6,b7,b8 = i.GAP(11,3)
                b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
                x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                ser.write(x)
                a = ser.read(9)
                if a == b'\x02\x01\x64\x06\x00\x00\x00\x01\x6e':
                    Bh = 1
                else:
                    Bh = 0
                sleep(0.1)
                if (Xh == 1) and (Yh == 1) and (Ah == 1) and (Bh == 1):
                    sleep(2)
                    print("home finished")
                    break
        else:
            action(line)
