import RPi.GPIO as GPIO
import os
from time import sleep
import pickle
import CLI

f = open("comm.pickle", "rb")
pid = pickle.load(f)
print("EMERGENCY PID CALLBACK:  "+str(pid))
f.close()

self_pid = os.getpid()

f = open("emergency.pickle", "wb")
pickle.dump(self_pid, f)
f.close()

def EMERGENCY_STOP(x):
    os.system("rm comm.pickle")
    os.system("kill "+str(pid))
    GPIO.output(4, GPIO.LOW)
    CLI.RESET()
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
