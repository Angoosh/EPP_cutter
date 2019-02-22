import RPi.GPIO as GPIO
import os
from time import sleep
import pickle
import serial
import Gcode

f = open("comm.pickle", "rb")
pid = pickle.load(f)
serPort = pickle.load(f)
print("EMERGENCY PID CALLBACK:  "+str(pid))
f.close()

self_pid = os.getpid()
print("EM: Got PID")

f = open("emergency.pickle", "wb")
pickle.dump(self_pid, f)
f.close()
print("EM: Dumped PID")

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
        GPIO.cleanup()
        sleep(0.2)
