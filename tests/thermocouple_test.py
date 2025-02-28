import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

spi_a = spidev.SpiDev()
spi_a.open(0,0)
spi_a.max_speed_hz = 500000

def read_test():
    raw = spi_a.xfer2([0x00, 0x00])
    value = (raw[0] << 8) | raw[1]

    if value & 0x4:
        return None
    
    return raw

i = 0
while i < 10:
    raw_data = read_test()
    if raw_data is not None:
        print(raw_data)
    else:
        print('not connected')
    time.sleep(0.1)
    i = i +1

spi_a.close()