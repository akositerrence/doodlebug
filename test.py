import RPi.GPIO as GPIO
import spidev
import thermocouple
import time

from pid import control

GPIO.setmode(GPIO.BOARD)

target_temp = 110
target_pressure = 50

heating_pad = 22
enter_cooling_valve = 24
exit_cooling_valve = 26
enter_gas_solenoid = 28
exit_gas_solenoid = 30

GPIO.setup(heating_pad, GPIO.OUT)
GPIO.setup(enter_cooling_valve, GPIO.OUT)
GPIO.setup(exit_cooling_valve, GPIO.OUT)
GPIO.setup(enter_gas_solenoid, GPIO.OUT)
GPIO.setup(exit_gas_solenoid, GPIO.OUT)

def pause_resume():


def read_sensors():


def print_data():


def temperature_cycle(cycle_number):
    read_sensors()
    time.sleep(0.5)

    GPIO.output(enter_cooling_valve, False)
    time.sleep(0.5)

    GPIO.output(exit_cooling_valve, False)
    time.sleep(0.5)

    if pid.output > 0 and current_temp < ( target_temp-1 ):
        GPIO.output(heating_pad, True)
    elif pid.output < 0 and current_temp > ( target_temp+1 ):


    while thermocouple1 <= target_temp:
        GPIO.output(heating_pad, True)
        time.sleep(0.5) #PID stuff
    GPIO.output(heating_pad, False)
    
    while pressure < target_pressure:
        GPIO.output(enter_gas_solenoid, True)
        time.sleep(0.5) #PID stuff
    GPIO.output(enter_gas_solenoid, False)


if __name__ == "__main__":
    Kp = 1.0
    Ki = 1.0
    Kd = 1.0
    pid = control(Kp, Ki, Kd, setpoint = 100)
