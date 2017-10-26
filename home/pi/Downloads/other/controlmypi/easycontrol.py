from controlmypi import ControlMyPi
import json
import RPi.GPIO as GPIO
import time

JABBER_ID = 'me@my.jabber.domain'
JABBER_PASSWORD = 'password'
SHORT_ID = 'easy1'
FRIENDLY_NAME = 'Control my red and yellow LEDs'
PANEL_FORM = [
             [ ['L','Remote control Raspberry Pi LEDs - status pushed back to this page!'] ],
             [ ['O'] ],
             [ ['L','Yellow'],['B','18 on','on'],['B','18 off','off'],['S','GPIO18','-'] ],
             [ ['L','Red'],['B','23 on','on'],['B','23 off','off'],['S','GPIO23','-'] ],
             [ ['C'] ],
             ]

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)

status = {18:False, 23:False}

def switch_led(n, state):
    if status[n] != state:
        GPIO.output(n, not state) #Low to glow!
        conn.update_status({'GPIO'+str(n): 'on' if state else 'off'})    
        status[n] = state

def on_control_message(conn, key, value):
    tokens = key.split(' ')
    number = int(tokens[0])
    state = tokens[1]
    if number in [18,23] and state in ['on','off']:
        switch_led(number, state == 'on')

def main_loop():
    switch_led(18,True)
    switch_led(23,True)
    debounced_one = True
    debounced_two = True
    while True:
        state_one = GPIO.input(24)
        state_two = GPIO.input(25)
        if state_one and debounced_one:
            switch_led(18, not status[18])
            debounced_one = False
        elif not state_one:
            debounced_one = True
            
        if state_two and debounced_two:
            switch_led(23, not status[23])
            debounced_two = False
        elif not state_two:
            debounced_two = True

        time.sleep(0.1)    


conn = ControlMyPi(JABBER_ID, JABBER_PASSWORD, SHORT_ID, FRIENDLY_NAME, PANEL_FORM, on_control_message)
if conn.start_control():
    try:
        main_loop()
    finally:
        conn.stop_control()
else:
    print("FAILED TO CONNECT")
