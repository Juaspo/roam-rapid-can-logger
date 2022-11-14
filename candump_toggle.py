#!/usr/bin/env python3

__all__ = []
__version__ = "0.0.1"
__date__ = "2022-10-18"
__author__ = "Junior Asante"
__status__ = "development"


import os
import time
#import threading
import multiprocessing
import RPi.GPIO as GPIO
from threading import Thread

run_dump = False
led_pin = 35
btn_pin = 37

GPIO.setwarnings(False)  # Ignore warnings
GPIO.setmode(GPIO.BOARD)  # Use physical board layout
GPIO.setup(led_pin, GPIO.OUT)  # Set led pin to output
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin 35 to be input with pullup
#GPIO.output(led_pin, GPIO.LOW)
GPIO.add_event_detect(btn_pin, GPIO.RISING, callback=lambda x: button_callback(), bouncetime=300)

candumprun = None

def startup_sequence():
    for x in range(5):
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.2)

def button_callback():
    GPIO.remove_event_detect(btn_pin)
    print("Button pressed!")
    toggle_candump()
    GPIO.add_event_detect(btn_pin, GPIO.RISING, callback=lambda x: button_callback(), bouncetime=300)

def toggle_candump():
    '''
    Toggle mode function
    '''

    global run_dump
    if run_dump:
        stop_candump()
    else:
        start_candump()
    time.sleep(1)

def start_candump():
    '''
    Function to start a process which in turn runs candump
    '''

    global run_dump
    global candumprun
    run_dump = True
    candumprun = multiprocessing.Process(target=run_can_dump, args=())
    candumprun.start()

def stop_candump():
    '''
    Stop candump process
    '''

    global run_dump
    global candumprun
    run_dump = False
    candumprun.terminate()  # sends a SIGTERM
    print("candump terminated")
    GPIO.output(led_pin, GPIO.LOW)
    os.system('sudo ifconfig can0 down')
    print("can0 down")

def run_can_dump():
    '''
    candump function run
    '''
    global run_dump

    os.system('sudo /sbin/ip link set can0 up type can bitrate 250000')
    print("can0 set to 250kbit/s")
    print("running candump...")
    GPIO.output(led_pin, GPIO.HIGH)
    pth = os.path.expanduser('~/canlogs')
    os.makedirs(pth, exist_ok=True)
    os.system('stdbuf -i0 -o0 candump -T 2000 -ta can0 > ~/canlogs/can-$(date +"%Y%m%d_%H%M%S").txt')
    GPIO.output(led_pin, GPIO.LOW)
    run_dump = False

startup_sequence()

user_input = None
while user_input != "":
    user_input = input("Press enter to quit\n")  # Run until someone presses enter

if run_dump:
    stop_candump()

GPIO.cleanup()  # Clean up
