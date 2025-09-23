
import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

cs = 29     # GPIO 5
so = 21     # GPIO 9
sck = 23    # GPIO 11

ent_cooling_valve = 16      # GPIO 23
ext_cooling_valve = 18      # GPIO 24
ent_gas_valve = 32          # GPIO 12
ext_gas_valve = 36          # GPIO 16

def relay_setup():
    GPIO.setup(ent_cooling_valve, GPIO.OUT)
    GPIO.setup(ext_cooling_valve, GPIO.OUT)
    GPIO.setup(ent_gas_valve, GPIO.OUT)
    GPIO.setup(ext_gas_valve, GPIO.OUT)
    # GPIO.setup(heating_pad, GPIO.OUT)

def startup():
    GPIO.output(ent_cooling_valve, 0)
    GPIO.output(ext_cooling_valve, 0)
    GPIO.output(ent_gas_valve, 0)
    GPIO.output(ext_gas_valve, 0)
    # GPIO.output(heating_pad, 0)
    
def close_relay(solenoid_number: int):
    match solenoid_number: # DOUBLE CHECK
        case 1:
            GPIO.output(ent_cooling_valve, 1)
        case 2:
            GPIO.output(ext_cooling_valve, 1)
        case 3:
            GPIO.output(ent_gas_valve, 1)
        case 4:
            GPIO.output(ext_gas_valve, 1)
        # case 5:
            # GPIO.output(heating_pad, 1)

def open_relay(solenoid_number: int):
    match solenoid_number: # DOUBLE CHECK
        case 1:
            GPIO.output(ent_cooling_valve, 0)
        case 2:
            GPIO.output(ext_cooling_valve, 0)
        case 3:
            GPIO.output(ent_gas_valve, 0)
        case 4:
            GPIO.output(ext_gas_valve, 0)
            
relay_setup()
GPIO.cleanup()