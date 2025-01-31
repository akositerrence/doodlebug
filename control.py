import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

spi_a = spidev.SpiDev()

spi_a.max_speed_hz = 500000

thermocouple_so_a = 21      # GPIO 9 ( SPI0 MISO )
thermocouple_cs_a = 24      # GPIO 8 ( SPI0 CE0 )
thermocouple_sck_a = 23     # GPIO 11 ( SPI0 SCLK )