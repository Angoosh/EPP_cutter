import serial
from byteparams import parameter as par
from time import sleep

def glob():
    mode = "ABS"            #default mode for positioning 
    travel = 10.0           #default mode for travel in mm
    negtravel = -10.0       #default mode for negative travel in mm
    sender = "sender-log.py"    #sender program to use (sender.py or sender-log.py)
    motorsteps = 200        #steps per rotation of used motor
    microstepping = 128     #supplied microstepping - 1-256
    screwpitch = 4          #screw pitch in mm
    logtime = 7             #days after log files will be removed
    logpath = "logs/"       #path to log files
    
    return mode, travel, negtravel, motorsteps, microstepping, screwpitch, sender, logtime, logpath

#nastaveni microsteppingu, je potreba odkomentovat func() aby bylo mozne aplikovat zmeny
def func():
    ser = serial.Serial("/dev/ttyACM0")
    microstepping = glob()[4]
    if microstepping == 256:
        steps = 8
    elif microstepping == 128:
        steps = 7
    elif microstepping == 64:
        steps = 6
    elif microstepping == 32:
        steps = 5
    elif microstepping == 16:
        steps = 4
    elif microstepping == 8:
        steps = 3
    elif microstepping == 4:
        steps = 2
    elif microstepping == 2:
        steps = 1
    else:
        steps = 0
    for motor in range (0,4):
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,5,140,motor,0,0,0,steps)
        x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(x)
        sleep(0.001)
        b1,b2,b3,b4,b5,b6,b7,b8,b9 = par(1,7,140,motor,0,0,0,0)
        x = bytearray([b1,b2,b3,b4,b5,b6,b7,b8,b9])
        ser.write(x)
        sleep(0.001)
    ser.close()
#func()
