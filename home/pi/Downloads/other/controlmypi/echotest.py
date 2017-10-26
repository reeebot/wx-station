import getpass
import logging
from controlmypi import ControlMyPi

def on_registered(conn):
    print "Registered with controlmypi.com!"
    
def on_control_message(conn, key, value):
    if key == 'echobox':
        print 'Received entry: %s' % value
        conn.update_status({'echo':'Pi echoes back: '+value})
    else:
        print key, value

def main_loop():
    # Block here. When you exit this function the connection to controlmypi.com will be closed
    raw_input("Press Enter to finish\n")

# Setup logging - change the log level here to debug faults
logging.basicConfig(level=logging.ERROR, format='%(levelname)-8s %(message)s')

jid = raw_input("Jabber ID: ")
password = getpass.getpass("Jabber password: ")
id = raw_input("Control panel ID: ")
name = raw_input("Control panel name: ")

panel_form = [
             [ ['L','Echo box:'] ],
             [ ['E','echobox','send'],['S','echo','-'] ]
             ]

conn = ControlMyPi(jid, password, id, name, panel_form, on_control_message, 'hid', on_registered)
print "Connecting to ControlMyPi..."
if conn.start_control():
    try:
        main_loop()
    finally:
        conn.stop_control()
else:
    print("FAILED TO CONNECT")
