
"""
Must run on python 3 
"""

import serial                               #import balicku seriove komunikace
from byteparams import parameter as par     #import balicku na vypocet checksum
import instructions as i                    #import balicku instrukcni sady rezacky
import Gcode                                #import balicku pro zpracovani gcode
import pickle                               #import balicku pro praci s pickle soubory
from time import sleep, gmtime, strftime    #import funkce sleep z balicku time pro cekani
import os                                   #import balicku operacniho systemu
import subprocess                           #import baliicku pro volani sytemovych prikazu

#zacatek logovani
log = open("logs/log.txt", "a")
log.write(strftime("%d-%m-%Y %H:%M:%S", gmtime()))
log.write("\n")
#cteni konfiguracniho souboru
f = open("comm.pickle", "rb")
serPort = pickle.load(f)
file = pickle.load(f)
f.close()
log.write("CONFIG LOAD\n")
log.write(str(serPort)+"\n")
log.write(str(file)+"\n")
log.write("\n")

#ziskani informaci o procesu a nasledne zapsani do souboru
pid = os.getpid()
f = open("comm.pickle", "wb")
pickle.dump(pid, f)
pickle.dump(serPort, f)
f.close()
sleep(1)
log.write("PROCESS INFO\n")
log.write(str(pid)+"\n")
log.write("\n")

#zapnuti EMERGENCY tlacitka
if os.path.exists("/home/pi") or os.path.exists("/home/rpi"):
    subprocess.call("python3 EMERGENCY.py &", shell = True)
    print("EMERGENCY active")
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    log.write("EMERGENCY LOAD\n")
    log.write("\n")
else:
    print("Not running on RPi")

#pripojeni k portu
try:
    ser = serial.Serial(serPort)
except:
    print("No such serial port as: " + serPort)
    os.system("kill "+str(pid))
    log.write("NO SERIAL PORT...\n")
    log.close()
    
#deklarace globalnich promennych
proceed = 0 #bezucelna promenna z brzkych stádii vyvoje
mode = "ABS" #ABS nebo REL
feedG0 = 2047 #2047 max
feedG1 = 2047 #2047 max
lastx, lasty, lasta, lastb = 0, 0, 0, 0 #posledni pozice os
st = 0.0001 #delay mezi posilanim dat
sth = 0.001 #delay pri homeni

#load emergency procesu
sleep(1)
f = open("emergency.pickle", "rb")
emerg_pid = pickle.load(f)
print("EMERGENCY PID = "+str(emerg_pid))
f.close()
log.write("EMERGENCY PID\n")
log.write(str(emerg_pid)+"\n")
log.write("\n")

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

log.write("................................................................\n")
log.write("GCODE EXECUTION\n")
log.write("\n")
#rozlysovani jednotlivych prikazu gcodu
def action(r):
    r = r.decode("utf-8")
    #import globalnich promennych do funkce
    global mode
    global st
    global proceed
    global lastx, lasty, lasta, lastb
    global feedG0, feedG1
    #zpracovani prikazu G0 pro pohyb
    if r.find("G0\n") != -1:
        log.write("G0")
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
            log.write("X "+str(xx)+"\n")
            log.write("Y "+str(yy)+"\n")
            log.write("A "+str(aa)+"\n")
            log.write("B "+str(bb)+"\n")
            
            yy = 420-yy
            bb = 420-bb
        except:
            return
        x, y, a, b = Gcode.G0(xx, yy, aa, bb)
        nx = abs(xx-lastx)
        ny = abs(yy-lasty)
        na = abs(aa-lasta)
        nb = abs(bb-lastb)
        mx = max(nx, ny, na, nb)
        log.write("new X "+str(nx)+"\n")
        log.write("new Y "+str(ny)+"\n")
        log.write("new A "+str(na)+"\n")
        log.write("new B "+str(nb)+"\n")
        log.write("max travel "+str(mx)+"\n")
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
        fx = int(feedG0/(mx/fx))
        fy = int(feedG0/(mx/fy))
        fa = int(feedG0/(mx/fa))
        fb = int(feedG0/(mx/fb))
        log.write("feed X "+str(fx)+"\n")
        log.write("feed Y "+str(fy)+"\n")
        log.write("feed A "+str(fa)+"\n")
        log.write("feed B "+str(fb)+"\n")
        
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
            print("OK1")
            log.write("OK1\n")
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
            print("OK2")
            log.write("OK2\n")
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
            print("OK3")
            log.write("OK3\n")
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
            print("OK4")
            log.write("OK4\n")
            pass
    #zpracovani prikazu G1 pro pohyb
    elif r.find("G1") != -1:
        log.write("G1\n")
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
            log.write("X "+str(xx)+"\n")
            log.write("Y "+str(yy)+"\n")
            log.write("A "+str(aa)+"\n")
            log.write("B "+str(bb)+"\n")
                        
            yy = 420-yy
            bb = 420-bb
        except:
            return
        x, y, a, b = Gcode.G0(xx, yy, aa, bb)
        nx = abs(xx-lastx)
        ny = abs(yy-lasty)
        na = abs(aa-lasta)
        nb = abs(bb-lastb)
        mx = max(nx, ny, na, nb)
        log.write("new X "+str(nx)+"\n")
        log.write("new Y "+str(ny)+"\n")
        log.write("new A "+str(na)+"\n")
        log.write("new B "+str(nb)+"\n")
        log.write("max travel "+str(mx)+"\n")
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
        fx = int(feedG1/(mx/fx))
        fy = int(feedG1/(mx/fy))
        fa = int(feedG1/(mx/fa))
        fb = int(feedG1/(mx/fb))
        log.write("feed X "+str(fx)+"\n")
        log.write("feed Y "+str(fy)+"\n")
        log.write("feed A "+str(fa)+"\n")
        log.write("feed B "+str(fb)+"\n")
        
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
            print("OK1")
            log.write("OK1\n")
            pass
        elif ny == mx:
#            ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
            ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(x)
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(b)
            print("OK2")
            log.write("OK2\n")
            pass
        elif na == mx:
#            ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
            ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(x)
            sleep(st)
            ser.write(b)
            print("OK3")
            log.write("OK3\n")
            pass
        else:
#            ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
            ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
            sleep(st)
            ser.write(b)
            sleep(st)
            ser.write(y)
            sleep(st)
            ser.write(a)
            sleep(st)
            ser.write(x)
            print("OK4")
            log.write("OK4\n")
            pass
    #zpracovani prikazu G28 pro homeni
    elif r.find("G28") != -1:
        log.write("G28\n")
        for motor in range (0,4):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(193,motor,1)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            sleep(sth)
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(194,motor,2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            s = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(s)
            sleep(sth)
        x, y, a, b = Gcode.G28()
        ser.write(x)
        sleep(sth)
        ser.write(y)
        sleep(sth)
        ser.write(a)
        sleep(sth)
        ser.write(b)
        sleep(sth)
    #zpracovani prikazu G90 pro zmenu modu na ABS
    elif r.find("G90") != -1:
        global mode
        mode = Gcode.G90()
        log.write("G90\n")
    #zpracovani prikazu G91 pro zmenu modu na REL 
    elif r.find("G91") != -1:
        mode = Gcode.G91()
        log.write("G91\n")
    #zpracovani prikazu M104 pro nahrivani
    elif r.find("M104") != -1:
        a = r.find("S")
        if a == -1:
            return
        temp = int(r[a+1:])
        heat, send = Gcode.M104(temp)
        ser.write(send)
        sleep(st)
        log.write("M104\n")
        log.write("Temp "+str(temp)+"\n")
    #zpracovani prikazu M600 pro cekani
    elif r.find("M600") != -1:
        a = r.find("S")
        if a == -1:
            return
        t = int(r[a+1:])
        Gcode.M600(t)
        log.write("M600\n")
        log.write("Time "+str(t)+"\n")
    #zpracovani prikazu F, pro feedrate
    elif r.find("F") != -1:
        a = r.find("F")
        if a == -1:
            return
        t = int(r[a+1:])
        if t <= 2047:
            feedG1 = t
            log.write("Feedrate "+str(feedG1)+"\n")
        else:
            print("Too much feedrate!")
            log.write("Too much feedrate!\n")
    #zpracovani prikazu MST pro okamzite zastaveni motoru (nepouzivane)
    elif r.find("MST") != -1:
        log.write("MST\n")
        for motor in range (0,4):
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,3, 0, motor, 0, 0, 0, 0)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            sleep(st)
    #reseni prazdnych radku a radku s "#"
    elif r == "":
        nothing, temp = Gcode.M104(0)
        for motor in range (0,4):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, motor, 2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(byte)
            sleep(0.001)
        if os.path.exists("/home/pi") or os.path.exists("/home/rpi"):
            os.system("kill "+str(emerg_pid))
            GPIO.output(4, GPIO.LOW)
        ser.write(temp)
        log.write("Empty string\n")
        log.close()
    elif r == "#":
        nothing, temp = Gcode.M104(0)
        for motor in range (0,4):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, motor, 2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(byte)
            sleep(0.001)
        if os.path.exists("/home/pi") or os.path.exists("/home/rpi"):
            os.system("kill "+str(emerg_pid))
            GPIO.output(4, GPIO.LOW)
        ser.write(temp)
        log.write("String = #\n")
        log.close()
    else:
        nothing, temp = Gcode.M104(0)
        for motor in range (0,4):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, motor, 2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(byte)
            sleep(0.001)
        if os.path.exists("/home/pi") or os.path.exists("/home/rpi"):
            os.system("kill "+str(emerg_pid))
            GPIO.output(4, GPIO.LOW)
        ser.write(temp)
        log.write("Unknown string\n")
        log.close()

#nacteni souboru gcodu a postupne jeho cteni radek po radku a reseni jednotlivych cekacich procedur
with open(file, "rb") as t:
    for line in t:
        print(line)
        log.write("\n")
        a = line.decode("utf-8")
        log.write(str(a[0:4])+"\n")
        if (a.find("G0") != -1) or (a.find("G1") != -1):
            action(line) #provedeni prislusnych vypocetnich procedur
            while True:
                r = ser.read(9)
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x01\x0e':
                    log.write("Got first read\n")
                    sleep(0.5)
                    break
                    
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x02\x0f':
                    log.write("Got second read\n")
                    break
                    
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x04\x11':
                    log.write("Got third read\n")
                    break
                    
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x08\x15':
                    log.write("Got fourth read\n")
                    break
                    
        elif a.find("G28") != -1:
            action(line) #provedeni prislusnych vypocetnich procedur
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
