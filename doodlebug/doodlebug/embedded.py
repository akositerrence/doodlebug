
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
# heating_pad = 0          # GPIO x

# flow_sensor = 0
# pressure_sensor = 0

# def read_flow():
#     GPIO.input(flow_sensor, GPIO.IN)
    
# def read_pressure():
#     GPIO.input(pressure_sensor, GPIO.IN)

def relay_setup():
    GPIO.setup(ent_cooling_valve, GPIO.OUT)
    GPIO.setup(ext_cooling_valve, GPIO.OUT)
    GPIO.setup(ent_gas_valve, GPIO.OUT)
    GPIO.setup(ext_gas_valve, GPIO.OUT)
    # GPIO.setup(heating_pad, GPIO.OUT)

def sensor_setup():
    GPIO.setup(sck, GPIO.OUT)
    GPIO.setup(cs, GPIO.OUT)
    GPIO.setup(so, GPIO.IN)

def startup():
    GPIO.output(ent_cooling_valve, 0)
    GPIO.output(ext_cooling_valve, 0)
    GPIO.output(ent_gas_valve, 0)
    GPIO.output(ext_gas_valve, 0)
    # GPIO.output(heating_pad, 0)
    
def read_thermocouples():
    GPIO.output(cs, 0)
    time.sleep(0.001)
    value = 0
    for i in range(16):
        GPIO.output(sck, 1)
        time.sleep(0.0001)
        value <<= 1
        if GPIO.input(so):
            value = (value << 1) + GPIO.input(so)
        GPIO.output(sck, 0)
        time.sleep(0.0001)

        GPIO.output(cs, 1)

        if value & 0x4:
            return None
        
        return (value >> 3) * 0.25
    
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
        # case 5:
            # GPIO.output(heating_pad, 0)
            
relay_setup()
sensor_setup()

time.sleep(3)
temp = read_thermocouples()
print(temp)

GPIO.cleanup()