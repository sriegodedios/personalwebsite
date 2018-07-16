from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
#from django.setup import DJANGO_SETTINGS_MODULE
from smbus2 import SMBus
import threading
import RPi.GPIO as GPIO
import smbus

slaveAddress = 0x12
numberInterruptPIN = 19
messageInterruptPIN = 12




def djangoserver():
    application = get_wsgi_application()
    call_command('runserver')

webserver = threading.Thread(target=djangoserver)
print("Server has been turned on!")


webserver.start()
