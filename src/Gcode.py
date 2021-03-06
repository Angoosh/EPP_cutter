import instructions as i
from byteparams import parameter as par
import config
import serial
from time import sleep

#funkce pripojeni k portu
def connection(port):
    try:
        ser = serial.Serial(port)
        print("Connected")
        return ser
    except:
        print(port + " does not exist")
        ser = ""
        return ser
    


mode = config.glob()[0]

# funkce gcodu G0
def G0(X, Y, A, B):
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,0,X)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,1,Y)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,2,A)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,3,B)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    b = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    return(x, y, a, b)
    
# funkce gcodu G1
def G1(X, Y, A, B):
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,0,X)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,1,Y)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,2,A)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b2,b3,b4,b5,b6,b7,b8 = i.MVP(mode,3,B)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    b = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    return(x, y, a, b)

# funkce gcodu G28
def G28():
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,0,0,0,0,0)
    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,1,0,0,0,0)
    y = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,2,0,0,0,0)
    a = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,13,0,3,0,0,0,0)
    b = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    return(x, y, a, b)

# funkce gcodu G90
def G90():
    global mode
    mode = "ABS"
    return(mode)

# funkce gcodu G91
def G91():
    global mode
    mode = "REL"
    return(mode)

# funkce mcodu M104
def M104(temp):
    if temp != 0:
        s = True
    else:
        s = False
    b2,b3,b4,b5,b6,b7,b8 = i.SIO(3, s)
    b1,b2,b3,b4,b5,b6,b7,b8,b9=par(1,b2,b3,b4,b5,b6,b7,b8)
    x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
    return(temp, x)

# funkce mcodu M600
def M600(t):
    sleep(t)
