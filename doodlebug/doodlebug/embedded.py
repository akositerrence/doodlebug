import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

spi_bus = spidev.SpiDev()
spi_bus.open(0,0)
spi_bus.max_speed_hz = 500000

ent_cooling_valve = 16      # GPIO 23
ext_cooling_valve = 18      # GPIO 24
ent_gas_valve = 32          # GPIO 12
ext_gas_valve = 36          # GPIO 16

flow_sensor = 0
pressure_sensor = 0

def read_flow():
    GPIO.input(flow_sensor, GPIO.IN)
    
def read_pressure():
    GPIO.input(pressure_sensor, GPIO.IN)

def relay_setup():
    GPIO.setup(ent_cooling_valve, GPIO.OUT)
    GPIO.setup(ext_cooling_valve, GPIO.OUT)
    GPIO.setup(ent_gas_valve, GPIO.OUT)
    GPIO.setup(ext_gas_valve, GPIO.OUT)

def read_thermocouples():
    raw = spi_bus.xfer2([0x00, 0x00])
    value = (raw[0] << 8 | raw[1])
    temperature = (value >> 3) * 0.25
    return temperature

def startup():
    GPIO.output(ent_cooling_valve, 0)
    GPIO.output(ext_cooling_valve, 0)
    GPIO.output(ent_gas_valve, 0)
    GPIO.output(ext_gas_valve, 0)

GPIO.cleanup()
spi_bus.close()