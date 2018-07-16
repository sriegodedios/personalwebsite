from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
#from django.setup import DJANGO_SETTINGS_MODULE
#from smbus2 import SMBus
import threading
import RPi.GPIO as GPIO
import smbus

slaveAddress = 0x12
numberInterruptPIN = 19
messageInterruptPIN = 12




def djangoserver():
    application = get_wsgi_application()
    call_command('runserver','10.0.0.225:8000')

webserver = threading.Thread(target=djangoserver)
print("Server has been turned on!")


webserver.start()

def readMessageFromArduino():
    global smsMessage
    data_received_from_Arduino = i2c.read_i2c_block_data(slaveAddress, 0,15)
    for i in range(len(data_received_from_Arduino)):
        smsMessage += chr(data_received_from_Arduino[i])

    print(smsMessage.encode('utf-8'))
    data_received_from_Arduino =""
    smsMessage = ""

def readNumberFromArduino():
    global smsNumber
    data_received_from_Arduino = i2c.read_i2c_block_data(slaveAddress, 0,15)
    for i in range(len(data_received_from_Arduino)):
        smsNumber += chr(data_received_from_Arduino[i])

    print(smsNumber.encode('utf-8'))
    data_received_from_Arduino = ""
    smsNumber = ""

smsMessage = ""
smsNumber = ""

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(numberInterruptPIN, GPIO.IN)
    GPIO.setup(messageInterruptPIN, GPIO.IN)

    i2c = smbus.SMBus(1)

    GPIO.add_event_detect(numberInterruptPIN, GPIO.RISING)
    GPIO.add_event_detect(messageInterruptPIN, GPIO.RISING)
    print("Listening for communication to arduino!!")
    while 1:

        try:
            if GPIO.event_detected(numberInterruptPIN):
                try:
                    readMessageFromArduino()
                except IOError:
                    pass
            if GPIO.event_detected(messageInterruptPIN):
                try:
                    readNumberFromArduino()
                except IOError:
                    pass

        except KeyboardInterrupt:
               GPIO.cleanup()
