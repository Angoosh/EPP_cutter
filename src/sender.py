import serial
from byteparams import parameter as par
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
#serPort = "/dev/ttyACM0"
#file = "maxx.gcode"
#pripojeni k portu
ser = serial.Serial(serPort)

#deklarace globalnich promennych
proceed = 0
mode = "ABS"
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
def action(i):
    i = i.decode("utf-8")
    print("i = "+i)
    global mode
    global proceed
    global lastx, lasty, lastz, lasta
    if i.find("G0") != -1:
        print("G0")
        x = i.find("X")
        y = i.find("Y")
        z = i.find("Z")
        a = i.find("A")
        if (x == -1) or (y == -1) or (z == -1) or (a == -1):
            print("Command must be in form: G0 X Y Z A")
            return
        try:
            xx = int(i[x+1:y-1])
            yy = int(i[y+1:z-1])
            zz = int(i[z+1:a-1])
            aa = int(i[a+1:])
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
    elif i.find("G1") != -1:
        print("G1")
        x = i.find("X")
        y = i.find("Y")
        z = i.find("Z")
        a = i.find("A")
        if (x == -1) or (y == -1) or (z == -1) or (a == -1):
            print("Command must be in form: G1 X Y Z A")
            return
        try:
            xx = int(i[x+1:y-1])
            yy = int(i[y+1:z-1])
            zz = int(i[z+1:a-1])
            aa = int(i[a+1:])
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
    elif i.find("G28") != -1:
        print("G28")
        x, y, z, a = Gcode.G28()
        ser.write(x)
        sleep(0.001)
        ser.write(y)
        sleep(0.001)
        ser.write(z)
        sleep(0.001)
        ser.write(a)
    elif i.find("G90") != -1:
        global mode
        mode = Gcode.G90()
        print("G90")
    elif i.find("G91") != -1:
        mode = Gcode.G91()
        print("G91")
    elif i.find("M104") != -1:
        a = i.find("S")
        if a == -1:
            print("Command must be in form: M104 S")
            return
        temp = int(i[a+1:])
        heat, send = Gcode.M104(temp)
        print(heat)
        ser.write(send)
        sleep(0.001)
    elif i.find("MST") != -1:
        for motor in range (0,4):
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,3, 0, motor, 0, 0, 0, 0)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            sleep(0.001)
            print("MST")
    elif i == "":
        print("No command specified")
    else:
        print("Unknown command")


with open(file, "rb") as i:
    for line in i:
        print(line)
        a = line.decode("utf-8")
        if (a.find("G0") != -1) or (a.find("G1") != -1):
            action(line)
            while True:
                r = ser.read(9)
                print(r)
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x01\x0e':
                    print("x")
                    break
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x02\x0f':
                    break
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x04\x11':
                    break
                if r == b'\x02\x01\x80\x8a\x00\x00\x00\x08\x15':
                    break
        else:
            action(line)