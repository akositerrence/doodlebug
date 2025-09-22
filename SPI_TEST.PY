import spidev, time

spi = spidev.SpiDev()
spi.open(10, 0)             # Pi 5 default SPI controller is bus 10
spi.max_speed_hz = 500000
spi.mode = 0b00             # SPI Mode 0

while True:
    raw = spi.readbytes(2)
    value = (raw[0] << 8 | raw[1]) >> 3
    if value & 0x1000:
        print("Thermocouple not connected")
    else:
        print(f"Temp: {value * 0.25:.2f} °C")
    time.sleep(1)
