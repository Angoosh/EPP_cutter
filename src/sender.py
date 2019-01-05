
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

#cteni konfiguracniho souboru
f = open("comm.pickle", "rb")
serPort = pickle.load(f)
file = pickle.load(f)
f.close()


pid = os.getpid()
f = open("comm.pickle", "wb")
pickle.dump(pid, f)
f.close()

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
lastx, lasty, lastz, lasta = 0, 0, 0, 0

#funkce pro threading
def wait_until_reached():
    while True:
        global proceed
        r = ser.read(9)
        print(r)
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x01\x0e':
            proceed = 0
            print("x")
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
    print("i = "+r)
    global mode
    global proceed
    global lastx, lasty, lastz, lasta
    global feed
    if r.find("G0") != -1:
        print("G0")
        x = r.find("X")
        y = r.find("Y")
        z = r.find("Z")
        a = r.find("A")
        if (x == -1) or (y == -1) or (z == -1) or (a == -1):
            print("Command must be in form: G0 X Y Z A")
            return
        try:
            xx = float(r[x+1:y-1])
            yy = float(r[y+1:z-1])
            zz = float(r[z+1:a-1])
            aa = float(r[a+1:])
        except:
            print("Command must be in form: G0 X Y Z A")
            return
        x, y, z, a = Gcode.G0(xx, yy, zz, aa)
        nx = abs(xx-lastx)
        ny = abs(yy-lasty)
        nz = abs(zz-lastz)
        na = abs(aa-lasta)
        mx = max(nx, ny, nz, na)
        print(mx)
#------------------------------interpolation--------------------------------------------
        fx, fy, fz, fa = nx, ny, nz, na
        if fx == 0:
            fx = mx
        if fy == 0:
            fy = mx
        if fz == 0:
            fz = mx
        if fa == 0:
            fa = mx
        fx = int(feed/(mx/fx))
        fy = int(feed/(mx/fy))
        fz = int(feed/(mx/fz))
        fa = int(feed/(mx/fa))
        
        print(fx, fy, fz, fa)
        
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 0, fx)
        b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        print("exxxx: "+str(byte))
        sleep(0.001)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 1, fy)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(0.003)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 2, fz)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(0.003)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 3, fa)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(0.003)
#---------------------------interpolation-end-------------------------------------------     
        lastx, lasty, lastz, lasta = xx, yy, zz, aa
        if nx == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
            sleep(0.001)
            ser.write(x)
            sleep(0.001)
            ser.write(y)
            sleep(0.001)
            ser.write(z)
            sleep(0.001)
            ser.write(a)
            print("first")
            pass
        elif ny == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
            sleep(0.001)
            ser.write(y)
            sleep(0.001)
            ser.write(x)
            sleep(0.001)
            ser.write(z)
            sleep(0.001)
            ser.write(a)
            print("second")
            pass
        elif nz == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
            sleep(0.001)
            ser.write(z)
            sleep(0.001)
            ser.write(y)
            sleep(0.001)
            ser.write(x)
            sleep(0.001)
            ser.write(a)
            print("third")
            pass
        else:
            ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
            sleep(0.001)
            ser.write(a)
            sleep(0.001)
            ser.write(y)
            sleep(0.001)
            ser.write(z)
            sleep(0.001)
            ser.write(x)
            print("fourth")
            pass
    elif r.find("G1") != -1:
        print("G1")
        x = r.find("X")
        y = r.find("Y")
        z = r.find("Z")
        a = r.find("A")
        if (x == -1) or (y == -1) or (z == -1) or (a == -1):
            print("Command must be in form: G1 X Y Z A")
            return
        try:
            xx = float(r[x+1:y-1])
            yy = float(r[y+1:z-1])
            zz = float(r[z+1:a-1])
            aa = float(r[a+1:])
        except:
            print("Command must be in form: G1 X Y Z A")
            return
        x, y, z, a = Gcode.G0(xx, yy, zz, aa)
        nx = abs(xx-lastx)
        ny = abs(yy-lasty)
        nz = abs(zz-lastz)
        na = abs(aa-lasta)
        mx = max(nx, ny, nz, na)
        print(mx)
#------------------------------interpolation--------------------------------------------
        fx, fy, fz, fa = nx, ny, nz, na
        if fx == 0:
            fx = mx
        if fy == 0:
            fy = mx
        if fz == 0:
            fz = mx
        if fa == 0:
            fa = mx
        fx = int(feed/(mx/fx))
        fy = int(feed/(mx/fy))
        fz = int(feed/(mx/fz))
        fa = int(feed/(mx/fa))
        
        print(fx, fy, fz, fa)
        
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 0, fx)
        b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        print("exxxx: "+str(byte))
        sleep(0.001)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 1, fy)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(0.003)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 2, fz)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(0.003)
        b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 3, fa)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(byte)
        sleep(0.003)
#---------------------------interpolation-end-------------------------------------------
        lastx, lasty, lastz, lasta = xx, yy, zz, aa
        if nx == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
            sleep(0.001)
            ser.write(x)
            sleep(0.001)
            ser.write(y)
            sleep(0.001)
            ser.write(z)
            sleep(0.001)
            ser.write(a)
            print("first")
            pass
        elif ny == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
            sleep(0.001)
            ser.write(y)
            sleep(0.001)
            ser.write(x)
            sleep(0.001)
            ser.write(z)
            sleep(0.001)
            ser.write(a)
            print("second")
            pass
        elif nz == mx:
            ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
            sleep(0.001)
            ser.write(z)
            sleep(0.001)
            ser.write(y)
            sleep(0.001)
            ser.write(x)
            sleep(0.001)
            ser.write(a)
            print("third")
            pass
        else:
            ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
            sleep(0.001)
            ser.write(a)
            sleep(0.001)
            ser.write(y)
            sleep(0.001)
            ser.write(z)
            sleep(0.001)
            ser.write(x)
            print("fourth")
            pass
    elif r.find("G28") != -1:
        print("G28")
        for motor in range (0,4):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(193,motor,1)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(194,motor,2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            s = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(s)
            sleep(0.001)
        x, y, z, a = Gcode.G28()
        ser.write(x)
        sleep(0.001)
        ser.write(y)
        sleep(0.001)
        ser.write(z)
        sleep(0.001)
        ser.write(a)
    elif r.find("G90") != -1:
        global mode
        mode = Gcode.G90()
        print("G90")
    elif r.find("G91") != -1:
        mode = Gcode.G91()
        print("G91")
    elif r.find("M104") != -1:
        a = r.find("S")
        if a == -1:
            print("Command must be in form: M104 S")
            return
        temp = int(r[a+1:])
        heat, send = Gcode.M104(temp)
        print(heat)
        ser.write(send)
        sleep(0.001)
    elif r.find("MST") != -1:
        for motor in range (0,4):
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,3, 0, motor, 0, 0, 0, 0)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            sleep(0.001)
            print("MST")
    elif r == "":
        print("No command specified")
    elif r == "#":
        print("Finished")
    else:
        print("Unknown command")


with open(file, "rb") as t:
    for line in t:
        print(line)
        a = line.decode("utf-8")
        if (a.find("G0") != -1) or (a.find("G1") != -1):
            action(line)
            while True:
                r = ser.read(9)
                print(r)
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
            Zh = 0
            Ah = 0
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
                    Zh = 1
                else:
                    Zh = 0
                sleep(0.1)
                b2,b3,b4,b5,b6,b7,b8 = i.GAP(11,3)
                b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
                x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                ser.write(x)
                a = ser.read(9)
                if a == b'\x02\x01\x64\x06\x00\x00\x00\x01\x6e':
                    Ah = 1
                else:
                    Ah = 0
                sleep(0.1)
                if (Xh == 1) and (Yh == 1) and (Zh == 1) and (Ah == 1):
                    sleep(2)
                    print("home finished")
                    break
        else:
            action(line)
