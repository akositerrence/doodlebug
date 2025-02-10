import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

spi_a = spidev.SpiDev()
thermocouple_so_a = 21      # GPIO 9 ( SPI0 MISO )
thermocouple_cs_a = 24      # GPIO 8 ( SPI0 CE0 )
thermocouple_sck_a = 23     # GPIO 11 ( SPI0 SCLK )

ent_cooling_valve = 16      # GPIO 23
ext_cooling_valve = 18      # GPIO 24
ent_gas_valve = 32          # GPIO 12
ext_gas_valve = 36          # GPIO 16

def setup():
    GPIO.setup(thermocouple_so_a, GPIO.OUT)
    GPIO.setup(thermocouple_cs_a, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(thermocouple_sck_a, GPIO.OUT, initial = GPIO.LOW)

def test_thermocouple():
    GPIO.output(thermocouple_cs_a, GPIO.LOW)
    GPIO.output(thermocouple_sck_a, GPIO.HIGH)
    test = GPIO.input(thermocouple_so_a)
    GPIO.output(thermocouple_sck_a, GPIO.LOW)

    return test

setup()
print(test_thermocouple()) 
