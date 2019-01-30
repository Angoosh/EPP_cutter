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
                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(5, GPIO.IN)
                GPIO.add_event_detect(5, GPIO.BOTH, callback=edge_detected, bouncetime=10)
                t = threading.Timer(3.0, shutdown)
                sleep(0.2)
                while True:
                        sleep(0.2)
                        pass
        finally:
                GPIO.cleanup()
                sleep(0.2)
