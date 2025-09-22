import time
from gpiozero import DigitalOutputDevice, DigitalInputDevice

class MAX6675:
    """
    MAX6675 thermocouple-to-digital converter, using bit-banged SPI via GPIO Zero.
    """

    def __init__(self, clk: int, cs: int, do: int):
        """
        clk : BCM pin for SCLK
        cs  : BCM pin for CS (chip select, active-low)
        do  : BCM pin for SO (serial data out from MAX6675)
        """
        # SPI clock line (output, idle LOW)
        self.clk = DigitalOutputDevice(clk, active_high=True, initial_value=False)
        # Chip-select line (output, active-low). Keep it HIGH (inactive) when idle.
        self.cs = DigitalOutputDevice(cs, active_high=False, initial_value=True)
        # Data-out line (input from MAX6675)
        self.do = DigitalInputDevice(do, pull_up=False)

        # Half clock delay (sec) — datasheet says 100 ns, but Python needs longer
        self._half_clock_delay = 0.00001

    def read_temp_c(self) -> float:
        """
        Perform one 16-bit read from MAX6675 and return temperature in °C.
        Raises RuntimeError if thermocouple not connected.
        """
        self.cs.on()   # drive CS LOW (because active_high=False)
        time.sleep(self._half_clock_delay)

        raw = 0
        for _ in range(16):
            self.clk.on()
            time.sleep(self._half_clock_delay)

            raw <<= 1
            if self.do.value:
                raw |= 0x1

            self.clk.off()
            time.sleep(self._half_clock_delay)

        self.cs.off()   # drive CS HIGH (inactive)

        # Bit D2 = 1 means thermocouple not connected
        if raw & 0x4:
            raise RuntimeError("MAX6675: thermocouple not connected or fault")

        # Bits 14..3 contain temperature in quarter-degrees C
        temp_c = ((raw >> 3) & 0x0FFF) * 0.25
        return temp_c
