import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

spi_a = spidev.SpiDev()
spi_a.open(0,0)
spi_a.max_speed_hz = 500000

def read_test(): # account for loss of signal?
    raw = spi_a.xfer2([0x00, 0x00])
    value = (raw[0] << 8) | raw[1]
    temperature = (value >> 3) * 0.25
    return temperature

i = 0
while i < 100:
    temp = read_test()
    print(temp)
    time.sleep(0.5)
    i = i +1

spi_a.close()