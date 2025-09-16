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
    GPIO.setup(thermocouple_cs_a, GPIO.OUT)
    GPIO.setup(thermocouple_sck_a, GPIO.OUT)

    GPIO.setup(ent_cooling_valve, GPIO.OUT)
    GPIO.setup(ext_cooling_valve, GPIO.OUT)
    GPIO.setup(ent_gas_valve, GPIO.OUT)
    GPIO.setup(ext_gas_valve, GPIO.OUT)

def test_relay():
    while True:
        print('off')
        GPIO.output(ent_cooling_valve, 0)  
        GPIO.output(ext_cooling_valve, 0) 
        GPIO.output(ent_gas_valve, 0)   
        GPIO.output(ext_gas_valve, 0)
        time.sleep(2)
        print('on')
        GPIO.output(ent_cooling_valve, 1)  
        GPIO.output(ext_cooling_valve, 1) 
        GPIO.output(ent_gas_valve, 1)   
        GPIO.output(ext_gas_valve, 1)
        time.sleep(2)

setup()
test_relay()

GPIO.cleanup()