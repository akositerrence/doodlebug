import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

spi_a = spidev.SpiDev()
thermocouple_so_a = 21      # GPIO 9 ( SPI0 MISO )
thermocouple_cs_a = 24      # GPIO 8 ( SPI0 CE0 )
thermocouple_sck_a = 23     # GPIO 11 ( SPI0 SCLK )

ent_cooling_valve = 1       # GPIO 1
ext_cooling_valve = 1       # GPIO 1
ent_gas_valve = 1           # GPIO 1
ext_gas_valve = 1           # GPIO 1

def setup():
    GPIO.setup(thermocouple_so_a, GPIO.OUT)
    GPIO.setup(thermocouple_cs_a, GPIO.OUT)
    GPIO.setup(thermocouple_sck_a, GPIO.OUT)
    GPIO.setup(ent_cooling_valve, GPIO.OUT)
    GPIO.setup(ext_cooling_valve, GPIO.OUT)
    GPIO.setup(ent_gas_valve, GPIO.OUT)
    GPIO.setup(ext_gas_valve, GPIO.OUT)

def test_relay():
    while True:
        GPIO.output(ent_cooling_valve, GPIO.LOW)  
        GPIO.output(ext_cooling_valve, GPIO.LOW)   
        GPIO.output(ent_gas_valve, GPIO.LOW)   
        GPIO.output(ext_gas_valve, GPIO.LOW)
        time.sleep(2)
        GPIO.output(ent_cooling_valve, GPIO.HIGH)  
        GPIO.output(ext_cooling_valve, GPIO.HIGH)   
        GPIO.output(ent_gas_valve, GPIO.HIGH)   
        GPIO.output(ext_gas_valve, GPIO.HIGH)

test_relay()