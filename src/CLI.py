
"""
Must run on python 3 
"""

import Gcode
from time import sleep
import instructions as i
from byteparams import parameter as par
import pickle
import os
import subprocess
import config

#kontrola zda je uzivatel prihlasen
prog_pid = os.getpid()
try:
    log = open("sec.pickle", "rb")
    login = pickle.load(log)
    log.close()
    os.system("rm -rf sec.pickle")
    if login == "OK":
        pass
except:
    os.system("kill "+str(prog_pid))

#nacteni config promennych
mode = config.glob()[0]
travel = config.glob()[1]
negtravel = config.glob()[2]
sender = config.glob()[6]
globX = 0
globY = 0
globA = 0
globB = 0

serPort = "/dev/ttyACM0"
file = ""

def openSender():
    os.system("python3 "+sender)

def sendComm():
    f = open("comm.pickle", "wb")
    pickle.dump(serPort, f)
    pickle.dump(file, f)
    f.close()
    
class Exceptions():
    def write(self, ser):
        print("No Connection")
    def read(dd, aa):
        print("No connection")
ser = Exceptions()

def gcoload(x):
            global file
            s = x
            try:
                if (".g" in s) or (".gco" in s) or (".gcode" in s):
                    try:
                        with open(s) as f:
                            file = s
                            f.read()
                            print("Gcode loaded\n")
                    except:
                        s = "gcodes/"+s
                        with open(s) as f:
                            file = s
                            f.read()
                            print("Gcode loaded\n")
                else:
                    print("Not a gcode\n")
            except:
                print("Path: "+s+" does not exist\n")

def STOP():
    print("STOP!")
    try:
        f = open("comm.pickle", "rb")
        pid = pickle.load(f)
        f.close()
        os.system("rm comm.pickle")
        os.system("kill "+str(pid))
    except:
        print("no comm.pickle")
    for motor in range (0,4):
        b2,b3,b4,b5,b6,b7,b8 = i.MST(motor)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(x)
        sleep(0.001)
        b2, b3, b4, b5, b6, b7, b8 = i.SAP(1,motor,0)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
        p = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(p)
        sleep(0.001)
    sleep(0.001)
    send = Gcode.M104(0)[1]
    ser.write(send)   

def RESET():
    global globX, globY, globA, globB
    globX, globY, globA, globB = 0,0,0,0
    b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,255, 0, 0, 0, 0, 4, 210)
    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    ser.write(x)
    print("RESET!")
    
def cli(x):
    """
    This is CLI for hot wire EPP cutter. For help enter help.
    
    Instructions are:
        help - shows help
        port - takes one argument, for connecting to selected port
        connect - connect to port on which cutter is, no arguments
        disconnect - to disconnect from cutter, no arguments
        gcode - takes one argument, gcode which will be printing from
        cut - for cutting, no arguments
        stop - immediate stop of cutting, no arguments
        exit - to exit application, note that sender will continue sending gcode to the cutter
        G0, G1, G28, G90, G91, M104, MST - as genetral cutter commands, arguments:
            G0 X Y A B
            G1 X Y A B
            G28
            G90
            G91
            M104 S
        
        RESET - for resetting TMCM-6110, reconnect required    
        command - for direct single line shell command input. If needed more commands
                  it must be in form: <first command> ; <second command> ; ...
                  
    Default port is /dev/ttyACM0
    """
    t = x
    global mode
    global serPort
    global ser
    global file
    global globX, globY, globA, globB
    
    if t.find("G0") != -1:
        x = t.find("X")
        y = t.find("Y")
        a = t.find("A")
        b = t.find("B")
        if (x == -1) or (y == -1) or (a == -1) or (b == -1):
            print("Command must be in form: G0 X Y A B\n")
            return
        try:
            xx = int(t[x+1:y-1])
            yy = int(t[y+1:a-1])
            aa = int(t[a+1:b-1])
            bb = int(t[b+1:])
        except:
            print("Command must be in form: G0 X Y A B\n")
            return
        x, y, a, b = Gcode.G0(xx, yy, aa, bb)
        if mode == "REL":
            globX = globX + xx
            globY = globY + yy
            globA = globA + aa
            globB = globB + bb
            if globX <= 900 and globY <= 420 and globA <=900 and globB <=420:
                ser.write(x)
                sleep(0.001)
                ser.write(y)
                sleep(0.001)
                ser.write(a)
                sleep(0.001)
                ser.write(b)
            else:
                print("max travel X,A = 900 Y,B = 420")
                print("X = "+str(globX))
                print("Y = "+str(globY))
                print("A = "+str(globA))
                print("B = "+str(globB))
        else:
            if xx <= 900 and yy <= 420 and aa <= 900 and bb <= 420:
                globX = xx
                globY = yy
                globA = aa
                globB = bb
                ser.write(x)
                sleep(0.001)
                ser.write(y)
                sleep(0.001)
                ser.write(a)
                sleep(0.001)
                ser.write(b)
            else:
                print("max travel X,A = 900 Y,B = 420")
    elif t.find("G1") != -1:
        x = t.find("X")
        y = t.find("Y")
        a = t.find("A")
        b = t.find("B")
        if (x == -1) or (y == -1) or (a == -1) or (b == -1):
            print("Command must be in form: G1 X Y A B\n")
            return
        try:
            xx = int(t[x+1:y-1])
            yy = int(t[y+1:a-1])
            aa = int(t[a+1:b-1])
            bb = int(t[b+1:])
        except:
            print("Command must be in form: G1 X Y A B\n")
            return
        x, y, a, b = Gcode.G1(xx, yy, aa, bb)
        if mode == "REL":
            globX = globX + xx
            globY = globY + yy
            globA = globA + aa
            globB = globB + bb
            if globX <= 900 and globY <= 420 and globA <= 900 and globB <= 420:
                ser.write(x)
                sleep(0.001)
                ser.write(y)
                sleep(0.001)
                ser.write(a)
                sleep(0.001)
                ser.write(b)
            else:
                print("max travel X,A = 900 Y,B = 420")
                print("X = "+str(globX))
                print("Y = "+str(globY))
                print("A = "+str(globA))
                print("B = "+str(globB))
        else:
            if xx <= 900 and yy <= 420 and aa <= 900 and bb <= 420:
                globX = xx
                globY = yy
                globA = aa
                globB = bb
                ser.write(x)
                sleep(0.001)
                ser.write(y)
                sleep(0.001)
                ser.write(a)
                sleep(0.001)
                ser.write(b)
            else:
                print("max travel X,A = 900 Y,B = 420")
    elif t.find("G28") != -1:
        x, y, a, b = Gcode.G28()
        for motor in range (0,4):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(193,motor,1)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            m = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(m)
            sleep(0.001)
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(194,motor,2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            s = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(s)
            sleep(0.001)
        globX, globY, globA, globB = 0,0,0,0
        ser.write(x)
        sleep(0.001)
        ser.write(y)
        sleep(0.001)
        ser.write(a)
        sleep(0.001)
        ser.write(b)
        sleep(0.001)
    elif t.find("G90") != -1:
        global mode
        mode = Gcode.G90()
    elif t.find("G91") != -1:               
        mode = Gcode.G91()
    elif t.find("M104") != -1:
        a = t.find("S")
        if a == -1:
            print("Command must be in form: M104 S\n")
            return
        temp = int(t[a+1:])
        heat, send = Gcode.M104(temp)
        ser.write(send)
    elif t.find("RESET") != -1:
        RESET()
    elif t.find("port") != -1:
        serPort = t[5:]
    elif t.find("connect") != -1:
        try:
            ser = Gcode.connection(serPort)
            sleep(0.2)
            config.func()
            for motor in range (0,4):
                b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, motor, 2047)
                b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
                byte = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                ser.write(byte)
                sleep(0.001)
        except: 
            ""
    elif t.find("disconnect") != -1:
        ser.close()
        ser = Exceptions()
    elif t.find("gcode") != -1:
        y = t[6:]
        gcoload(y)
    elif t.find("cut") != -1:
        if file != "":
            sendComm()
            print("Starting sender")
            sleep(1)
            openSender()
        else:
            print("no file for cutting selected")
    elif t.find("stop") != -1:
        STOP()
    elif t.find("exit") != -1:
        pid = os.getpid()
        subprocess.call("kill "+str(pid), shell = True)
    elif t.find("command") != -1:
        if len(t) > 8:
            x = t[8:]
            subprocess.call(x, shell = True)
        else:
            subprocess.call(input("command: "), shell = True)
    elif t.find("help") != -1:
        print(cli.__doc__)
    elif t == "":
        print("No command given\n")
    else:
        print("Unknown command: " + t)


print(cli.__doc__)
while True:
    x = input("CLI: ")
    cli(x)
