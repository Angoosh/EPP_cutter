#!/usr/bin/env p#ython3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 13:51:44 2018

@author: angoosh
"""

from kivy.app import App
from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import Gcode
from Gcode import connection
import instructions as i
from byteparams import parameter as par
from time import sleep



def end():
    Gui().stop()


#ser = "/dev/ttyACM0"
  
class Exceptions:
    def write(self,byte):
        print("No Connection")
        
#Globalni promenne
ser = Exceptions()
travel = 10
negtravel = -10
mode = "ABS"

class Widgets(FloatLayout):
    def __init__(self, **kwargs):
        super(Widgets, self).__init__(**kwargs)
        
#funkce pro pohybova tlacitka
        def Xa(instance):
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 0, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            print(b1,b2,b3,b4,b5,b6,b7,b8,b9)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "axis X ascend: " + str(travel) +"mm\n"
        def Xd(instance):
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 0, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "axis X descend: " + str(travel) +"mm\n"
        def Ya(instance):
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 1, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "axis Y ascend: " + str(travel) +"mm\n"
        def Yd(instance):
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 1, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "axis Y descend: " + str(travel) +"mm\n"
        def Za(instance):
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 2, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "axis Z ascend: " + str(travel) +"mm\n"
        def Zd(instance):
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 2, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "axis Z descend: " + str(travel) +"mm\n"
        def Aa(instance):
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 3, travel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "axis A ascend: " + str(travel) +"mm\n"
        def Ad(instance):
            b2, b3, b4, b5, b6, b7, b8 = i.MVP("REL", 3, negtravel)
            b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,b2,b3,b4,b5,b6,b7,b8)
            x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(x)
            self.terminal.text += "axis A descend: " + str(travel) +"mm\n"
        
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
            if self.travel.text == "":
                travel = 0
            else:
                global travel
                travel = float(self.travel.text)
                global negtravel
                negtravel = travel * -1
            self.terminal.text += "Travel set to: " + str(travel) +"mm\n"
            print(travel)
            return travel
#funkce pro nacteni gcodu
        def gcoload(btn):
            try:
                with open(self.gco1.text) as f:
                    content1 = f.read()
                    self.terminal.text += "Gcode1 loaded\n"
                    print(content1)
            except:
                self.terminal.text += "Path: "+self.gco1.text+" does not exist\n"
#funkce tlacitka nahrati odporoveho dratu                
        def heating(instance):
            if self.heating.state == "down":
                print("heating")
            else:
                print("cooling")
#funkce primeho uzivatelskeho vstupu
        def command(instance):
            i = self.command.text
            if i.find("G0") != -1:
                print("G0")
                x = i.find("X")
                y = i.find("Y")
                z = i.find("Z")
                a = i.find("A")
                print(x, y, z, a)
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
                print(x, y, z, a)
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
                global mode
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
            else:
                self.terminal.text += "Unknown command: " + self.command.text + "\n"
                self.command.text = ""
            
#funkce nastaveni portu        
        def port(instance):
            if self.portButt.state == "down":
                self.portButt.text = "Disconnect"
                self.portButt.size_hint = (.1, .05)
                if self.port.text != "":
                    global ser
                    ser = connection(self.port.text)
                    if ser != "":
                        print(ser.name)
                        self.terminal.text += "Connected to: "+ser.name+"\n"
                        global ser
                        ser = ser
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
            print(x)
            self.terminal.text += "Home X\n"
        def homeY(instance):
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,1,0,0,0,0)
            y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(y)
            print(y)
            self.terminal.text += "Home Y\n"
        def homeZ(instance):
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,2,0,0,0,0)
            z = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(z)
            print(z)
            self.terminal.text += "Home Z\n"
        def homeA(instance):
            b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,3,0,0,0,0)
            a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
            ser.write(a)
            print(a)
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
        self.gco1 = TextInput(size_hint=(.2, .05), pos=(100, 480), font_size=12, multiline=False)
        self.add_widget(self.gco1)
        self.add_widget(
                Label(text = "Gcode", pos = (100, 510), size_hint=(.1, .05), color=(0,0,0,255)))
        self.add_widget(
                Button(text = "Load", on_press = gcoload, font_size = 25, size_hint=(.08, .05), pos = (370, 480)))
       
#tlacitko nahrati odporoveho dratu
        self.heating = ToggleButton(text = "Heating", on_press = heating, font_size = 25, size_hint=(.08, .05), pos = (500, 480), background_down = "./images/heatingPressed.png")
        self.add_widget(self.heating)
        
#ERROR terminal        
        self.terminal = TextInput(size_hint=(.3, .3), pos=(450, 70), font_size=12, readonly=True)
        self.add_widget(self.terminal)
        
#Command sender
        self.command = TextInput(size_hint=(.2, .05), pos=(450, 20), font_size=16, multiline=False)
        self.add_widget(self.command)
        self.add_widget(
                Button(text = "Send", on_press = command, font_size = 25, size_hint=(.08, .05), pos = (720, 20)))
        
#Home buttons
        self.add_widget(
                Button(text = "X", on_press = homeX, font_size = 30, size_hint=(.045, .08), pos = (850, 300), bold = True))
        self.add_widget(
                Button(text = "Y", on_press = homeY, font_size = 30, size_hint=(.045, .08), pos = (920, 300), bold = True))
        self.add_widget(
                Button(text = "Z", on_press = homeZ, font_size = 30, size_hint=(.045, .08), pos = (990, 300), bold = True))
        self.add_widget(
                Button(text = "A", on_press = homeA, font_size = 30, size_hint=(.045, .08), pos = (1060, 300), bold = True))
        self.add_widget(
                Label(text = "HOME axis", pos = (850, 360), size_hint=(.1, .05), color=(0,0,0,255)))
        
#Vyber portu
        self.port = TextInput(text = "/dev/ttyACM0", size_hint=(.1, .05), pos=(100, 560), font_size=12, multiline=False)
        self.add_widget(self.port)
        self.add_widget(
                Label(text = "Port", pos = (100, 590), size_hint=(.1, .05), color=(0,0,0,255)))
        self.portButt = ToggleButton(text = "Connect", on_press = port, font_size = 25, size_hint=(.08, .05), pos = (240, 560))
        self.add_widget(self.portButt)
        
    
class Gui(App):
     def build(self):
        self.root = root = Widgets()
        root.bind(size = self._update_rect, pos = self._update_rect)
        
        Window.size = (1280, 720)
        self.icon = "./images/appIcon1.png"
        self.title = "Control Panel"

        with root.canvas.before:
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root
        
     def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
if __name__ == "__main__":
    Gui().run()
    