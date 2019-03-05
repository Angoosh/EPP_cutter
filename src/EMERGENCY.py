import RPi.GPIO as GPIO
import os
from time import sleep
import pickle
import serial
import Gcode

#otevreni souboru s informaci o portu a pid senderu
f = open("comm.pickle", "rb")
pid = pickle.load(f)
serPort = pickle.load(f)
print("EMERGENCY PID CALLBACK:  "+str(pid))
f.close()

#ziskani pid vlastniho procesu
self_pid = os.getpid()
print("EM: Got PID")

#ulozeni pid vlastniho procesu do souboru
f = open("emergency.pickle", "wb")
pickle.dump(self_pid, f)
f.close()
print("EM: Dumped PID")

#funkce nouzoveho tlacitka
def EMERGENCY_STOP(x):
    print("EM: Stopping sender")
    os.system("rm comm.pickle")
    os.system("kill "+str(pid))
    ser = Gcode.connection(serPort)
    heat, send = Gcode.M104(0)
    ser.write(send)
    sleep(0.001)
    ser.close()
    GPIO.output(4, GPIO.LOW)
    exit()

if __name__ == "__main__":
    try:
        #nastaveni cteni tlacitka a zapnuti indikace
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(4, GPIO.OUT)
        GPIO.output(4, GPIO.HIGH)
        GPIO.add_event_detect(14, GPIO.BOTH, callback=EMERGENCY_STOP, bouncetime=10)
        sleep(0.2)
        while True:
            sleep(0.2)
            pass
    finally:
        GPIO.cleanup() #vypnuti vsech GPIO a jejich vymazani z pouzivanych pinu
        sleep(0.2)
