#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 13:51:44 2018

@author: angoosh

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



#nacitani konfiguracnich promennych do globalnich promennych
mode = config.glob()[0]
travel = config.glob()[1]
negtravel = config.glob()[2]
serport = ""
    #promenne pro kontrolu, zda prislusna osa jede
x1 = 0
y1 = 0
z1 = 0
a1 = 0


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
            global x1
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 0, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if x1 == 0:
                x1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis X ascend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis X already moving\n"
        def Xd(instance):
            global x1
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 0, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if x1 == 0:
                x1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,1,140]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis X descend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis X already moving\n"
        def Ya(instance):
            global y1
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 1, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if y1 == 0:
                y1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis Y ascend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis Y already moving\n"
        def Yd(instance):
            global y1
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 1, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if y1 == 0:
                y1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,2,141]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis Y descend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis Y already moving\n"
        def Za(instance):
            global z1
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 2, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if z1 == 0:
                z1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis Z ascend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis Z already moving\n"
        def Zd(instance):
            global z1
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 2, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if z1 == 0:
                z1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,4,143]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis Z descend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis Z already moving\n"
        def Aa(instance):
            global a1
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 3, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if a1 == 0:
                a1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis A ascend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis A already moving"
        def Ad(instance):
            global a1
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 3, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            if a1 == 0:
                a1 = 1
                ser.write(bytearray([1,138,0,0,0,0,0,8,147]))
                ser.write(x)
                Thread(target = wait_until_reached).start()
                self.terminal.text += "axis A descend: " + str(travel) +"mm\n"
            else:
                self.terminal.text += "axis A already moving\n"
        
#funkce stop tlacitka    
        def STOP(instance):
            print("RESET!!")
            self.terminal.text += "Reset\n"
            
            for motor in range (0,4):
                b2,b3,b4,b5,b6,b7,b8 = i.MST(motor)
                b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
                x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                ser.write(x)
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
                b2,b3,b4,b5,b6,b7,b8 = i.SAP(4, 0, value)
                b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
                x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                ser.write(x)
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
                if len(serport) > 2:
                    pass
            except:
                self.terminal.text += "No connection to serial\n"
            try:
                os.system("python sender.py")
            except:
                self.terminal.text += "No sender program\n"
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
#funkce primeho uzivatelskeho vstupu
        def command(instance):
            i = self.command.text
            global mode
            if i.find("G0") != -1:
                print("G0")
                x = i.find("X")
                y = i.find("Y")
                z = i.find("Z")
                a = i.find("A")
                if (x == -1) or (y == -1) or (z == -1) or (a == -1):
                    self.terminal.text += "Command must be in form: G0 X Y Z A\n"
                    return
                try:
                    xx = int(i[x+1:y-1])
                    yy = int(i[y+1:z-1])
                    zz = int(i[z+1:a-1])
                    aa = int(i[a+1:])
                except:
                    self.terminal.text += "Command must be in form: G0 X Y Z A\n"
                    return
                x, y, z, a = Gcode.G0(xx, yy, zz, aa)
                ser.write(x)
                ser.write(y)
                ser.write(z)
                ser.write(a)
                self.terminal.text += i + "\n"
                self.command.text = ""
            elif i.find("G1") != -1:
                print("G1")
                x = i.find("X")
                y = i.find("Y")
                z = i.find("Z")
                a = i.find("A")
                if (x == -1) or (y == -1) or (z == -1) or (a == -1):
                    self.terminal.text += "Command must be in form: G1 X Y Z A\n"
                    return
                try:
                    xx = int(i[x+1:y-1])
                    yy = int(i[y+1:z-1])
                    zz = int(i[z+1:a-1])
                    aa = int(i[a+1:])
                except:
                    self.terminal.text += "Command must be in form: G1 X Y Z A\n"
                    return
                x, y, z, a = Gcode.G1(xx, yy, zz, aa)
                ser.write(x)
                ser.write(y)
                ser.write(z)
                ser.write(a)
                self.terminal.text += i + "\n"
                self.command.text = ""
            elif i.find("G28") != -1:
                print("G28")
                x, y, z, a = Gcode.G28()
                ser.write(x)
                ser.write(y)
                ser.write(z)
                ser.write(a)
                self.terminal.text += i + "\n"
                self.command.text = ""
            elif i.find("G90") != -1:
                global mode
                mode = Gcode.G90()
                print("G90")
                self.terminal.text += i + "\n"
                self.command.text = ""
            elif i.find("G91") != -1:
                
                mode = Gcode.G91()
                print("G91")
                self.terminal.text += i + "\n"
                self.command.text = ""
            elif i.find("M104") != -1:
                a = i.find("S")
                if a == -1:
                    self.terminal.text += "Command must be in form: M104 S\n"
                    return
                temp = int(i[a+1:])
                heat, send = Gcode.M104(temp)
                print(heat)
                ser.write(send)
                self.terminal.text += i + "\n"
                self.command.text = ""
            elif i.find("MST") != -1:
                for motor in range (0,4):
                    b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,3, 0, motor, 0, 0, 0, 0)
                    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
                    ser.write(x)
                print("MST")
                self.terminal.text += i + "\n"
                self.command.text = ""
            elif i == "":
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
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,0,0,0,0,0)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "Home X\n"
        def homeY(instance):
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,1,0,0,0,0)
            y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(y)
            self.terminal.text += "Home Y\n"
        def homeZ(instance):
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,2,0,0,0,0)
            z = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(z)
            self.terminal.text += "Home Z\n"
        def homeA(instance):
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,3,0,0,0,0)
            a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(a)
            self.terminal.text += "Home A\n"
        
#tlacitka pohybu
        self.add_widget(
                Label(text = "XY", color=(0,0,0,255), pos = (240, 150), size_hint = (.07, .07), font_size = 40, bold = True))
        self.add_widget(
                Label(text = "ZA", color=(0,0,0,255), pos = (950, 150), size_hint = (.07, .07), font_size = 40, bold = True))        
        self.add_widget(
                Button(background_normal = "./images/upArrow.png", background_down = "./images/upArrowPressed.png", on_press = Ya, font_size = 40, size_hint=(.09, .16), pos = (120, 120))) #x=115.2px
        self.add_widget(
                Button(background_normal = "./images/dwnArrow.png", background_down = "./images/dwnArrowPressed.png", on_press = Yd, font_size = 40, size_hint=(.09, .16), pos = (120, 5)))
        self.add_widget(
                Button(background_normal = "./images/rightArrow.png", background_down = "./images/rightArrowPressed.png", on_press = Xa, font_size = 40, size_hint=(.09, .16), pos = (235, 5)))
        self.add_widget(
                Button(background_normal = "./images/leftArrow.png", background_down = "./images/leftArrowPressed.png", on_press = Xd, font_size = 40, size_hint=(.09, .16), pos = (5, 5)))
        self.add_widget(
                Button(background_normal = "./images/upArrow.png", background_down = "./images/upArrowPressed.png", on_press = Aa, font_size = 40, size_hint=(.09, .16), pos = (1045, 120)))
        self.add_widget(
                Button(background_normal = "./images/dwnArrow.png", background_down = "./images/dwnArrowPressed.png", on_press = Ad, font_size = 40, size_hint=(.09, .16), pos = (1045, 5)))
        self.add_widget(
                Button(background_normal = "./images/rightArrow.png", background_down = "./images/rightArrowPressed.png", on_press = Za, font_size = 40, size_hint=(.09, .16), pos = (1160, 5)))
        self.add_widget(
                Button(background_normal = "./images/leftArrow.png", background_down = "./images/leftArrowPressed.png", on_press = Zd, font_size = 40, size_hint=(.09, .16), pos = (930, 5)))
        
#Stop tacitko
        self.add_widget(
                Button(text = "STOP", on_press = STOP, font_size = 40, size_hint=(.16, .16), pos = (1060, 600), background_color = (255, 0, 0, 255)))
        
#nastaveni feedrate
        self.feed = TextInput(size_hint=(.1, .05), pos=(500, 340), input_filter="int", font_size=20, multiline=False)
        self.add_widget(self.feed)
        self.add_widget(
                Button(text = "set", on_press = sett, font_size = 25, size_hint=(.05, .05), pos = (650, 340)))
        self.add_widget(
                Label(text = "Feedrate", pos = (500, 370), size_hint=(.1, .05), color=(0,0,0,255)))
        
#nastaveni travel os
        self.travel = TextInput(text = "10", size_hint=(.1, .05), pos=(500, 400), input_filter="float", font_size=20, multiline=False)
        self.add_widget(self.travel)
        self.add_widget(
                Label(text = "Travel", pos = (500, 430), size_hint=(.1, .05), color=(0,0,0,255)))
        self.add_widget(
                Button(text = "set", on_press = trav, font_size = 25, size_hint=(.05, .05), pos = (650, 400)))
       
#file chooser
        self.gco = TextInput(size_hint=(.2, .05), pos=(100, 480), font_size=12, multiline=False)
        self.add_widget(self.gco)
        self.add_widget(
                Label(text = "Gcode", pos = (100, 510), size_hint=(.1, .05), color=(0,0,0,255)))
        self.add_widget(
                Button(text = "Load", on_press = gcoload, font_size = 25, size_hint=(.08, .05), pos = (370, 480)))
       
#tlacitko zacnuti vyrezavani
        self.add_widget(
                Button(text = "Cut", on_press = cut, font_size = 25, size_hint=(.05, .05), pos = (100, 400)))
        
#tlacitko nahrati odporoveho dratu
        self.heating = ToggleButton(text = "Heating", on_press = heating, font_size = 25, size_hint=(.08, .05), pos = (500, 480), background_down = "./images/heatingPressed.png")
        self.add_widget(self.heating)
        
#ERROR terminal        
        self.terminal = TextInput(size_hint=(.3, .3), pos=(450, 70), font_size=12, readonly=True)
        self.add_widget(self.terminal)
        self.add_widget(
                Button(text = "Clear", on_press = clr, font_size = 25, size_hint=(.06, .05), pos = (835, 250)))
        
#Command sender
        self.command = TextInput(size_hint=(.2, .05), pos=(450, 20), font_size=16, multiline=False)
        self.add_widget(self.command)
        self.add_widget(
                Button(text = "Send", on_press = command, font_size = 25, size_hint=(.08, .05), pos = (720, 20)))
        
#Home buttons
        self.add_widget(
                Button(text = "X", on_press = homeX, font_size = 30, size_hint=(.045, .08), pos = (850, 350), bold = True))
        self.add_widget(
                Button(text = "Y", on_press = homeY, font_size = 30, size_hint=(.045, .08), pos = (920, 350), bold = True))
        self.add_widget(
                Button(text = "Z", on_press = homeZ, font_size = 30, size_hint=(.045, .08), pos = (990, 350), bold = True))
        self.add_widget(
                Button(text = "A", on_press = homeA, font_size = 30, size_hint=(.045, .08), pos = (1060, 350), bold = True))
        self.add_widget(
                Label(text = "HOME axis", pos = (850, 410), size_hint=(.1, .05), color=(0,0,0,255)))
        
#Vyber portu
        self.port = TextInput(text = "/dev/ttyACM0", size_hint=(.1, .05), pos=(100, 560), font_size=12, multiline=False)
        self.add_widget(self.port)
        self.add_widget(
                Label(text = "Port", pos = (100, 590), size_hint=(.1, .05), color=(0,0,0,255)))
        self.portButt = ToggleButton(text = "Connect", on_press = port, font_size = 25, size_hint=(.08, .05), pos = (240, 560))
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
    