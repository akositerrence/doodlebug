import RPi.GPIO as GPIO
import spidev
import thermocouple
import time

from pid import control

GPIO.setmode(GPIO.BOARD)    # Set GPIO mode to board

spi_a = spidev.SpiDev()       # Initialize SPI thermocouple a
spi_a.max_speed_hz = 500000   

spi_b = spidev.SpiDev()       # Initialize SPI thermocouple b
spi_b.max_speed_hz = 500000   

enter_cooling_valve = 16    # GPIO 23
exit_cooling_valve = 18     # GPIO 24
enter_gas_solenoid = 32     # GPIO 12
exit_gas_solenoid = 36      # GPIO 16

thermocouple_so_a = 21      # GPIO 9 ( SPI0 MISO )

thermocouple_cs_a = 24      # GPIO 8 ( SPI0 CE0 )
thermocouple_sck_a = 23     # GPIO 11 ( SPI0 SCLK )

thermocouple_so_b = 21      # GPIO 9 ( SPI0 MISO )
thermocouple_cs_b = 26      # GPIO 7 ( SPI0 CE1 )
thermocouple_sck_b = 23     # GPIO 11 ( SPI0 SCLK )

transducer = 0 # UNKNOWN
flow = 0 # UNKNOWN

GPIO.setup(enter_cooling_valve, GPIO.OUT)
GPIO.setup(exit_cooling_valve, GPIO.OUT)
GPIO.setup(enter_gas_solenoid, GPIO.OUT)
GPIO.setup(exit_gas_solenoid, GPIO.OUT)

GPIO.setup(thermocouple_so_a , GPIO.OUT)
GPIO.setup(thermocouple_cs_a, GPIO.OUT)
GPIO.setup(thermocouple_sck_a, GPIO.OUT)

def pause_resume():


def read_sensors():


def print_data():


def temperature_cycle(cycle_number):


if __name__ == "__main__":
    Kp = 1.0
    Ki = 1.0
    Kd = 1.0
    pid = control(Kp, Ki, Kd, setpoint = 100)
