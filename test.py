import spidev
import time

spi_bus = spidev.SpiDev()
spi_bus.open(10,0)
spi_bus.max_speed_hz = 500000
spi_bus.mode = 0

def read_thermocouples():
    raw = spi_bus.readbytes(2)
    return raw

for i in range(10):
    tc1 = read_thermocouples()
    print(tc1)
    time.sleep(0.01)

spi_bus.close()