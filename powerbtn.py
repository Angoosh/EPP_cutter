import threading, subprocess
import RPi.GPIO as GPIO
from time import sleep

def shutdown():
        subprocess.call("sudo shutdown now", shell=True)

def edge_detected(pin):
        if GPIO.input(pin):
                t.cancel()
                subprocess.call("sudo reboot", shell=True)
        else:
                t.start()

if __name__ == "__main__":
        try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(3, GPIO.IN)
                GPIO.setup(4, GPIO.OUT)
                GPIO.output(4, GPIO.HIGH)
                GPIO.setup(15, GPIO.OUT)
                GPIO.output(15, GPIO.HIGH)
                GPIO.add_event_detect(5, GPIO.BOTH, callback=edge_detected, bouncetime=10)
                t = threading.Timer(3.0, shutdown)
                sleep(0.2)
                while True:
                        sleep(0.2)
                        pass
        finally:
                GPIO.cleanup()
                sleep(0.2)
