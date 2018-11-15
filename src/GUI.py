
"""
Must run on python 3 
"""

from threading import Thread
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import Gcode
import config
from Gcode import connection
import instructions as i
from byteparams import parameter as par
import os
import pickle
from time import sleep
import tkinter

#zjistovani rozliseni obrazovky
root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#vychozi promenne pro nastaveni velikosti fontu
fTiny = 12
fSmall = 16
fMed = 20
fBig = 25
fLarge = 30
fHuge = 40

#nastaveni velikosti fontu pro obrazovky mensi nez 1280x720
if height < 700:
    fTiny = 8
    fSmall = 8
    fMed = 10
    fBig = 12.5
    fLarge = 15
    fHuge = 20

#nacitani konfiguracnich promennych do globalnich promennych
mode = config.glob()[0]
travel = config.glob()[1]
negtravel = config.glob()[2]
#serport = ""
    #promenne pro kontrolu, zda prislusna osa jede
x1 = 0
y1 = 0
z1 = 0
a1 = 0
    #promenne pro zobrazeni nastavene hodnoty os
x2, y2, z2, a2 = 0, 0, 0, 0

#funkce cekani na dojeti motoru na pozici
def wait_until_reached():
    while True:
        global x1, y1, z1, a1
        r = ser.read(9)
        print(r)
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x01\x0e':
            print("travelled")
            x1 = y1 = z1 = a1 = 0
            break
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x02\x0f':
            x1 = y1 = z1 = a1 = 0
            break
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x04\x11':
            x1 = y1 = z1 = a1 = 0
            break
        if r == b'\x02\x01\x80\x8a\x00\x00\x00\x08\x15':
            x1 = y1 = z1 = a1 = 0
            break        

#funkce otevreni senderu jako novy thread
def openSender():
    os.system("python3 sender.py")

def sendComm():
    f = open("comm.pickle", "wb")
    pickle.dump(serport, f)
    pickle.dump(file, f)
    f.close()
#trida pro nahrazeni ser.write(), kdyz bude port nedostupny
class Exceptions:
    def write(self,byte):
        print("No Connection")
    def read(dd, aa):
        print("No connection")
ser = Exceptions()

#trida vsech objektu GUI
class Widgets(FloatLayout):
    def __init__(self, **kwargs):
        super(Widgets, self).__init__(**kwargs)
            
#funkce pro pohybova tlacitka
        def Xa(instance):
            global x1, x2
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 0, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            x2 = x2 + travel
            if (x1 == 0) and (x2 <= 900):
                x1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis X ascend: " + str(travel) +"mm\n"
                self.xTravel.text = str(x2)
            else:
                self.terminal.text += "axis X already moving or can't travel more\n"
        def Xd(instance):
            global x1, x2
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 0, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if (x1 == 0) and (x2 > 0):
                x1 = 1
                x2 = x2 - travel
                ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.xTravel.text = str(x2)
                self.terminal.text += "axis X descend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis X already moving or can't travel to negative\n"
        def Ya(instance):
            global y1, y2
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 1, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if (y1 == 0) and (y2 <= 420):
                y1 = 1
                y2 = y2 + travel
                ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.yTravel.text = str(y2)
                self.terminal.text += "axis Y ascend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis Y already moving\n"
        def Yd(instance):
            global y1, y2
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 1, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if (y1 == 0) and (y2 > 0):
                y1 = 1
                y2 = y2 - travel
                ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.yTravel.text = str(y2)
                self.terminal.text += "axis Y descend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis Y already moving or can't travel to negative\n"
        def Za(instance):
            global z1, z2
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 2, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if (z1 == 0) and (z2 <= 900):
                z1 = 1
                z2 = z2 + travel
                ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.zTravel.text = str(z2)
                self.terminal.text += "axis Z ascend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis Z already moving\n"
        def Zd(instance):
            global z1, z2
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 2, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if (z1 == 0) and (z2 > 0):
                z1 = 1
                z2 = z2 - travel
                ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.zTravel.text = str(z2)
                self.terminal.text += "axis Z descend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis Z already moving or can't travel to negative\n"
        def Aa(instance):
            global a1, a2
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 3, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if (a1 == 0) and (a2 <= 420):
                a1 = 1
                a2 = a2 + travel
                ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.aTravel.text = str(a2)
                self.terminal.text += "axis A ascend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis A already moving"
        def Ad(instance):
            global a1, a2
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 3, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if (a1 == 0) and (a2 > 0):
                a1 = 1
                a2 = a2 - travel
                ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.aTravel.text = str(a2)
                self.terminal.text += "axis A descend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis A already moving or can't travel to negative\n"
        
#funkce stop tlacitka    
        def STOP(instance):
            print("RESET!!")
            self.terminal.text += "Reset\n"
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
            

#fukce pro nastaveni feedrate pro vsechny osy        
        def sett(btn):
            if self.feed.text == "":
                print("error")
                self.terminal.text += "FeedrateError\n"
            else:
                value = int(self.feed.text)
                print(self.feed.text)
                for motor in range (0,4):
                    b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, motor, value)
                    b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
                    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                    ser.write(x)
                    sleep(0.001)
                self.terminal.text += "Feedrate set to: " + self.feed.text + "\n"
#funkce pro travel os
        def trav(btn):
            global travel
            if self.travel.text == "":
                travel = 0
            else:
                
                travel = float(self.travel.text)
                global negtravel
                negtravel = travel * -1
            self.terminal.text += "Travel set to: " + str(travel) +"mm\n"
            print(travel)
            return travel
#funkce pro nacteni gcodu
        def gcoload(btn):
            global file
            s = self.gco.text
            try:
                if (".g" in s) or (".gco" in s) or (".gcode" in s):
                    with open(s) as f:
                        file = self.gco.text
                        content = f.read()
                        self.terminal.text += "Gcode loaded\n"
                        print(content)
                else:
                    self.terminal.text += "Not a gcode\n"
            except:
                self.terminal.text += "Path: "+self.gco.text+" does not exist\n"
                
#funkce spusteni senderu
        def cut(instance):
            try:
                if len(file) > 2:
                    pass
            except:
                self.terminal.text += "No file loaded\n"
            try:
                if len(serport) >= 4:
                    pass
            except:
                self.terminal.text += "No connection to serial\n"
            try:
                sendComm()
                self.terminal.text += "Starting sender\n"
                sleep(1)
                self.terminal.text += "Passing instruction to sender\n"
                self.xTravel.text = "0"
                self.yTravel.text = "0"
                self.zTravel.text = "0"
                self.aTravel.text = "0"
                try:
                    self.terminal.text += "Cutting started\n"
                    Thread(target = openSender).start()
                except:
                    self.terminal.text += "No sender program\n"
            except:
                self.terminal.text += "Cutting not possible\n"

#funkce vycisteni terminalu                
        def clr(instance):
            self.terminal.text = ""
#funkce tlacitka nahrati odporoveho dratu                
        def heating(instance):
            if self.heating.state == "down":
                send = Gcode.M104(1)[1]
                ser.write(send)
                self.terminal.text += "Heating\n"
            else:
                send = Gcode.M104(0)[1]
                ser.write(send)
                self.terminal.text += "cooling\n"
#funkce fullscreen tlacitka
        def fullscreen(instance):
            if self.fullscreen.state == "down":
                Window.fullscreen = True
            else:
                Window.fullscreen = False
#funkce primeho uzivatelskeho vstupu
        def command(instance):
            t = self.command.text
            global mode
            if t.find("G0") != -1:
                print("G0")
                x = t.find("X")
                y = t.find("Y")
                z = t.find("Z")
                a = t.find("A")
                if (x == -1) or (y == -1) or (z == -1) or (a == -1):
                    self.terminal.text += "Command must be in form: G0 X Y Z A\n"
                    return
                try:
                    xx = int(t[x+1:y-1])
                    yy = int(t[y+1:z-1])
                    zz = int(t[z+1:a-1])
                    aa = int(t[a+1:])
                except:
                    self.terminal.text += "Command must be in form: G0 X Y Z A\n"
                    return
                x, y, z, a = Gcode.G0(xx, yy, zz, aa)
                ser.write(x)
                sleep(0.001)
                ser.write(y)
                sleep(0.001)
                ser.write(z)
                sleep(0.001)
                ser.write(a)
                self.terminal.text += t + "\n"
                self.command.text = ""
            elif t.find("G1") != -1:
                print("G1")
                x = t.find("X")
                y = t.find("Y")
                z = t.find("Z")
                a = t.find("A")
                if (x == -1) or (y == -1) or (z == -1) or (a == -1):
                    self.terminal.text += "Command must be in form: G1 X Y Z A\n"
                    return
                try:
                    xx = int(t[x+1:y-1])
                    yy = int(t[y+1:z-1])
                    zz = int(t[z+1:a-1])
                    aa = int(t[a+1:])
                except:
                    self.terminal.text += "Command must be in form: G1 X Y Z A\n"
                    return
                x, y, z, a = Gcode.G1(xx, yy, zz, aa)
                ser.write(x)
                sleep(0.001)
                ser.write(y)
                sleep(0.001)
                ser.write(z)
                sleep(0.001)
                ser.write(a)
                self.terminal.text += t + "\n"
                self.command.text = ""
            elif t.find("G28") != -1:
                print("G28")
                x, y, z, a = Gcode.G28()
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
                ser.write(x)
                sleep(0.001)
                ser.write(y)
                sleep(0.001)
                ser.write(z)
                sleep(0.001)
                ser.write(a)
                self.terminal.text += t + "\n"
                self.command.text = ""
                self.xTravel.text = "0"
                self.yTravel.text = "0"
                self.zTravel.text = "0"
                self.aTravel.text = "0"
            elif t.find("G90") != -1:
                global mode
                mode = Gcode.G90()
                print("G90")
                self.terminal.text += t + "\n"
                self.command.text = ""
            elif t.find("G91") != -1:
                
                mode = Gcode.G91()
                print("G91")
                self.terminal.text += t + "\n"
                self.command.text = ""
            elif t.find("M104") != -1:
                a = t.find("S")
                if a == -1:
                    self.terminal.text += "Command must be in form: M104 S\n"
                    return
                temp = int(t[a+1:])
                heat, send = Gcode.M104(temp)
                print(heat)
                ser.write(send)
                self.terminal.text += t + "\n"
                self.command.text = ""
            elif t.find("MST") != -1:
                for motor in range (0,4):
                    b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,3, 0, motor, 0, 0, 0, 0)
                    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                    ser.write(x)
                print("MST")
                self.terminal.text += t + "\n"
                self.command.text = ""
            elif t == "":
                self.terminal.text += "No command specified\n"
                
            else:
                self.terminal.text += "Unknown command: " + self.command.text + "\n"
                self.command.text = ""
#funkce nastaveni portu        
        def port(instance):
            global ser
            global serport
            if self.portButt.state == "down":
                self.portButt.text = "Disconnect"
                self.portButt.size_hint = (.1, .05)
                if self.port.text != "":
                    global ser
                    ser = connection(self.port.text)
                    if ser != "":
                        print(ser.name)
                        self.terminal.text += "Connected to: "+ser.name+"\n"
                        #global ser
                        ser = ser
                        serport = self.port.text
                        return ser
                        #ser = connection(self.port.text)
                    else:
                        ser = Exceptions()
                        self.terminal.text += "Unable to open selected port\n"
                        self.portButt.state = "normal"
                        self.portButt.text = "Connect"
                        self.portButt.size_hint = (.08, .05)
                else:
                    self.terminal.text += "Enter port!\n"
            else:
                ser.close()
                ser = Exceptions()
                self.portButt.text = "Connect"
                self.portButt.size_hint = (.08, .05)
                self.terminal.text += "Disconnected\n"

#funkce pro home tlacitka
        def homeX(instance):
            
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(193,0,1)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(194,0,2000)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            s = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(s)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,0,0,0,0,0)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "Home X\n"
            self.xTravel.text = "0"
        def homeY(instance):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(193,1,1)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(194,1,2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            s = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(s)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,1,0,0,0,0)
            y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(y)
            self.terminal.text += "Home Y\n"
            self.yTravel.text = "0"
        def homeZ(instance):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(193,2,1)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(194,2,2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            s = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(s)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,2,0,0,0,0)
            z = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(z)
            self.terminal.text += "Home Z\n"
            self.zTravel.text = "0"
        def homeA(instance):
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(193,3,1)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            b2,b3,b4,b5,b6,b7,b8 = i.SAP(194,3,2047)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
            s = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(s)
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,3,0,0,0,0)
            a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(a)
            self.terminal.text += "Home A\n"
            self.aTravel.text = "0"
        
#tlacitka pohybu
        self.add_widget(
                Label(text = "XY", color=(0,0,0,255), pos_hint = {"x":.1875, "y":.208333333}, size_hint = (.07, .07), font_size = fHuge, bold = True))
        self.add_widget(
                Label(text = "ZA", color=(0,0,0,255), pos_hint = {"x":.7421875, "y":.208333333}, size_hint = (.07, .07), font_size = fHuge, bold = True))        
        self.add_widget(
                Button(background_normal = "./images/upArrow.png", background_down = "./images/upArrowPressed.png", on_press = Yd, font_size = fHuge, size_hint=(.09, .16), pos_hint = {"x":120/1280, "y":120/720}))
        self.add_widget(
                Button(background_normal = "./images/dwnArrow.png", background_down = "./images/dwnArrowPressed.png", on_press = Ya, font_size = fHuge, size_hint=(.09, .16), pos_hint = {"x":120/1280, "y":5/720}))
        self.add_widget(
                Button(background_normal = "./images/rightArrow.png", background_down = "./images/rightArrowPressed.png", on_press = Xa, font_size = fHuge, size_hint=(.09, .16), pos_hint = {"x":235/1280, "y":5/720}))
        self.add_widget(
                Button(background_normal = "./images/leftArrow.png", background_down = "./images/leftArrowPressed.png", on_press = Xd, font_size = fHuge, size_hint=(.09, .16), pos_hint = {"x":5/1280, "y":5/720}))
        self.add_widget(
                Button(background_normal = "./images/upArrow.png", background_down = "./images/upArrowPressed.png", on_press = Ad, font_size = fHuge, size_hint=(.09, .16), pos_hint = {"x":1045/1280, "y":120/720}))
        self.add_widget(
                Button(background_normal = "./images/dwnArrow.png", background_down = "./images/dwnArrowPressed.png", on_press = Aa, font_size = fHuge, size_hint=(.09, .16), pos_hint = {"x":1045/1280, "y":5/720}))
        self.add_widget(
                Button(background_normal = "./images/rightArrow.png", background_down = "./images/rightArrowPressed.png", on_press = Za, font_size = fHuge, size_hint=(.09, .16), pos_hint = {"x":1160/1280, "y":5/720}))
        self.add_widget(
                Button(background_normal = "./images/leftArrow.png", background_down = "./images/leftArrowPressed.png", on_press = Zd, font_size = fHuge, size_hint=(.09, .16), pos_hint = {"x":930/1280, "y":5/720}))

#indikatory pozic
        self.xTravel = TextInput(text = "0", size_hint=(.06, .05), pos_hint = {"x":550/1280, "y":600/720}, font_size=fMed, readonly=True)
        self.add_widget(self.xTravel)
        self.yTravel = TextInput(text = "0", size_hint=(.06, .05), pos_hint = {"x":640/1280, "y":600/720}, font_size=fMed, readonly=True)
        self.add_widget(self.yTravel)
        self.zTravel = TextInput(text = "0", size_hint=(.06, .05), pos_hint = {"x":730/1280, "y":600/720}, font_size=fMed, readonly=True)
        self.add_widget(self.zTravel)
        self.aTravel = TextInput(text = "0", size_hint=(.06, .05), pos_hint = {"x":820/1280, "y":600/720}, font_size=fMed, readonly=True)
        self.add_widget(self.aTravel)
        self.add_widget(
                Label(text = "Set axis positions", color=(0,0,0,255), pos_hint = {"x":670/1280, "y":660/720}, size_hint = (.07, .07), font_size = fMed, bold = True))
        self.add_widget(
                Label(text = "X", color=(0,0,0,255), pos_hint = {"x":550/1280, "y":630/720}, size_hint = (.06, .07), font_size = fMed, bold = True))
        self.add_widget(
                Label(text = "Y", color=(0,0,0,255), pos_hint = {"x":640/1280, "y":630/720}, size_hint = (.06, .07), font_size = fMed, bold = True))
        self.add_widget(
                Label(text = "Z", color=(0,0,0,255), pos_hint = {"x":730/1280, "y":630/720}, size_hint = (.06, .07), font_size = fMed, bold = True))
        self.add_widget(
                Label(text = "A", color=(0,0,0,255), pos_hint = {"x":820/1280, "y":630/720}, size_hint = (.06, .07), font_size = fMed, bold = True))
        
#Stop tacitko
        self.add_widget(
                Button(text = "STOP", on_press = STOP, font_size = fHuge, size_hint=(.16, .16), pos_hint = {"x":1060/1280, "y":600/720}, background_color = (255, 0, 0, 255)))
        
#nastaveni feedrate
        self.feed = TextInput(size_hint=(.1, .05), pos_hint = {"x":500/1280, "y":340/720}, input_filter="int", font_size=fMed, multiline=False)
        self.add_widget(self.feed)
        self.add_widget(
                Button(text = "set", on_press = sett, font_size = fBig, size_hint=(.05, .05), pos_hint = {"x":650/1280, "y":340/720}))
        self.add_widget(
                Label(text = "Feedrate",font_size = fMed, pos_hint = {"x":500/1280, "y":370/720}, size_hint=(.1, .05), color=(0,0,0,255)))
        
#nastaveni travel os
        self.travel = TextInput(text = "10", size_hint=(.1, .05), pos_hint = {"x":500/1280, "y":400/720}, input_filter="float", font_size=fMed, multiline=False)
        self.add_widget(self.travel)
        self.add_widget(
                Label(text = "Travel",font_size = fMed, pos_hint = {"x":500/1280, "y":430/720}, size_hint=(.1, .05), color=(0,0,0,255)))
        self.add_widget(
                Button(text = "set", on_press = trav, font_size = fBig, size_hint=(.05, .05), pos_hint = {"x":650/1280, "y":400/720}))
       
#file chooser
        self.gco = TextInput(size_hint=(.2, .05), pos_hint = {"x":100/1280, "y":480/720}, font_size=fTiny, multiline=False)
        self.add_widget(self.gco)
        self.add_widget(
                Label(text = "Gcode",font_size = fMed, pos_hint = {"x":100/1280, "y":510/720}, size_hint=(.1, .05), color=(0,0,0,255)))
        self.add_widget(
                Button(text = "Load", on_press = gcoload, font_size = fBig, size_hint=(.08, .05), pos_hint = {"x":370/1280, "y":480/720}))
       
#tlacitko zacnuti vyrezavani
        self.add_widget(
                Button(text = "Cut", on_press = cut, font_size = fBig, size_hint=(.05, .05), pos_hint = {"x":100/1280, "y":400/720}))
        
#tlacitko nahrati odporoveho dratu
        self.heating = ToggleButton(text = "Heating", on_press = heating, font_size = fBig, size_hint=(.08, .05), pos_hint = {"x":500/1280, "y":480/720}, background_down = "./images/heatingPressed.png")
        self.add_widget(self.heating)
        
#fullscreen tlacitko
        self.fullscreen = ToggleButton(text = "Fullscr", on_press = fullscreen, font_size = fBig, size_hint=(.08, .05), pos_hint = {"x":5/1280, "y":680/720})
        self.add_widget(self.fullscreen)
        
#ERROR terminal        
        self.terminal = TextInput(size_hint=(.3, .3), pos_hint = {"x":450/1280, "y":70/720}, font_size=fTiny, readonly=True)
        self.add_widget(self.terminal)
        self.add_widget(
                Button(text = "Clear", on_press = clr, font_size = fBig, size_hint=(.06, .05), pos_hint = {"x":835/1280, "y":250/720}))
        
#Command sender
        self.command = TextInput(size_hint=(.2, .05), pos_hint = {"x":450/1280, "y":20/720}, font_size=fSmall, multiline=False)
        self.add_widget(self.command)
        self.add_widget(
                Button(text = "Send", on_press = command, font_size = fBig, size_hint=(.08, .05), pos_hint = {"x":720/1280, "y":20/720}))
        
#Home buttons
        self.add_widget(
                Button(text = "X", on_press = homeX, font_size = fLarge, size_hint=(.045, .08), pos_hint = {"x":850/1280, "y":350/720}, bold = True))
        self.add_widget(
                Button(text = "Y", on_press = homeY, font_size = fLarge, size_hint=(.045, .08), pos_hint = {"x":920/1280, "y":350/720}, bold = True))
        self.add_widget(
                Button(text = "Z", on_press = homeZ, font_size = fLarge, size_hint=(.045, .08), pos_hint = {"x":990/1280, "y":350/720}, bold = True))
        self.add_widget(
                Button(text = "A", on_press = homeA, font_size = fLarge, size_hint=(.045, .08), pos_hint = {"x":1060/1280, "y":350/720}, bold = True))
        self.add_widget(
                Label(text = "HOME axis",font_size = fMed, pos_hint = {"x":850/1280, "y":410/720}, size_hint=(.1, .05), color=(0,0,0,255)))
        
#Vyber portu
        self.port = TextInput(text = "/dev/ttyACM0", size_hint=(.1, .05), pos_hint = {"x":100/1280, "y":560/720}, font_size=fTiny, multiline=False)
        self.add_widget(self.port)
        self.add_widget(
                Label(text = "Port",font_size = fMed, pos_hint = {"x":100/1280, "y":590/720}, size_hint=(.1, .05), color=(0,0,0,255)))
        self.portButt = ToggleButton(text = "Connect", on_press = port, font_size = fBig, size_hint=(.08, .05), pos_hint = {"x":240/1280, "y":560/720})
        self.add_widget(self.portButt)
        
#trida samotne aplikace   
class Gui(App):
     def build(self):
        self.root = root = Widgets()
        root.bind(size = self._update_rect, pos = self._update_rect)
        
        Window.size = (1280, 720)
        self.icon = "./images/appIcon1.png"
        self.title = "Control Panel"
        self.window_icon = "./images/appIcon1.png"

        with root.canvas.before:
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root
        
     def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

#spusteni aplikace        
if __name__ == "__main__":
    Gui().run()  