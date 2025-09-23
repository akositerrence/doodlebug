import spidev
import time

class MAX31855:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)      # bus=0, device=0 → CE0
        self.spi.max_speed_hz = 5000000 # 5 MHz (max for MAX31855)
        self.spi.mode = 0b00

    def read(self):
        # Read 32 bits (4 bytes)
        raw = self.spi.readbytes(4)
        value = raw[0] << 24 | raw[1] << 16 | raw[2] << 8 | raw[3]

        # Check fault bit (D16)
        if value & 0x7:
            if value & 0x01:
                raise RuntimeError("Thermocouple not connected")
            elif value & 0x02:
                raise RuntimeError("Short to ground")
            elif value & 0x04:
                raise RuntimeError("Short to VCC")

        # Extract thermocouple temperature (bits 31–18)
        temp_tc = (value >> 18) & 0x3FFF
        if temp_tc & 0x2000:  # sign bit
            temp_tc -= 0x4000
        temp_tc *= 0.25  # each bit = 0.25 °C

        # Extract internal (cold junction) temperature (bits 15–4)
        temp_int = (value >> 4) & 0xFFF
        if temp_int & 0x800:
            temp_int -= 0x1000
        temp_int *= 0.0625

        return temp_tc, temp_int

    def close(self):
        self.spi.close()


if __name__ == "__main__":
    sensor = MAX31855(bus=0, device=0)
    try:
        while True:
            tc, cj = sensor.read()
            print(f"Thermocouple: {tc:.2f} °C | Internal: {cj:.2f} °C")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        sensor.close()
