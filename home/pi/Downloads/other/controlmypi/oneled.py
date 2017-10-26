from controlmypi import ControlMyPi
import json
import RPi.GPIO as GPIO
import time

JABBER_ID = 'me@my.jabber.domain'
JABBER_PASSWORD = 'password'
SHORT_ID = 'oneled'
FRIENDLY_NAME = 'One LED'
PANEL_FORM = [
             [ ['O'] ],
             [ ['L','LED'],['B','on_button','On'],['B','off_button','Off'],['S','state','-'] ],
             [ ['C'] ],
             ]

GPIO_NUM = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_NUM, GPIO.OUT)

led_state = {GPIO_NUM:False}

def switch_led(state):
    if led_state[GPIO_NUM] != state:
        GPIO.output(GPIO_NUM, not state) #Low to glow!
        conn.update_status({'state': 'on' if state else 'off'})    
        led_state[GPIO_NUM] = state

def on_control_message(conn, key, value):
    if key == 'on_button':    
        switch_led(True)
    elif key == 'off_button':
        switch_led(False)


def main_loop():
    switch_led(True)
    while True:
        time.sleep(3) #Yield for a while but keep main thread running    


conn = ControlMyPi(JABBER_ID, JABBER_PASSWORD, SHORT_ID, FRIENDLY_NAME, PANEL_FORM, on_control_message)
if conn.start_control():
    try:
        main_loop()
    finally:
        conn.stop_control()
else:
    print("FAILED TO CONNECT")
