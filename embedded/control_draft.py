import RPi.GPIO as GPIO
import spidev
import embedded.thermocouple as thermocouple
import time

from simple_pid import PID

GPIO.setmode(GPIO.BOARD)   

spi_a = spidev.SpiDev()          
spi_b = spidev.SpiDev()   

spi_a.max_speed_hz = 500000    
spi_b.max_speed_hz = 500000     

enter_cooling_valve = 16        # GPIO 23
exit_cooling_valve = 18         # GPIO 24
enter_gas_solenoid = 32         # GPIO 12
exit_gas_solenoid = 36          # GPIO 16
thermocouple_so_a = 21          # GPIO 9 ( SPI0 MISO )
thermocouple_cs_a = 24          # GPIO 8 ( SPI0 CE0 )
thermocouple_sck_a = 23         # GPIO 11 ( SPI0 SCLK )
thermocouple_so_b = 21          # GPIO 9 ( SPI0 MISO )
thermocouple_cs_b = 26          # GPIO 7 ( SPI0 CE1 )
thermocouple_sck_b = 23         # GPIO 11 ( SPI0 SCLK )
heating_pad = 0                 # UNKNOWN
transducer = 0                  # UNKNOWN
flow = 0                        # UNKNOWN

def setup():
    GPIO.setup(enter_cooling_valve, GPIO.OUT)
    GPIO.setup(exit_cooling_valve, GPIO.OUT)
    GPIO.setup(enter_gas_solenoid, GPIO.OUT)
    GPIO.setup(exit_gas_solenoid, GPIO.OUT)

    GPIO.setup(thermocouple_so_a , GPIO.OUT)
    GPIO.setup(thermocouple_cs_a, GPIO.OUT)
    GPIO.setup(thermocouple_sck_a, GPIO.OUT)

    GPIO.setup(thermocouple_so_b , GPIO.OUT)
    GPIO.setup(thermocouple_cs_b, GPIO.OUT)
    GPIO.setup(thermocouple_sck_b, GPIO.OUT)

def read_sensors():
    temp_a = GPIO.input(thermocouple_so_a)
    temp_b = GPIO.input(thermocouple_so_b)
    pressure = GPIO.input(transducer)
    flow_rate = GPIO.input(flow)
    valve_a = GPIO.input(enter_cooling_valve)
    valve_b = GPIO.input(exit_cooling_valve)
    valve_c = GPIO.input(enter_gas_solenoid)
    valve_d = GPIO.input(exit_gas_solenoid)

    sensor_data = [temp_a, temp_b, pressure, flow_rate, valve_a, valve_b, valve_c, valve_d]
    return(sensor_data)

def startup():
    GPIO.output(enter_cooling_valve, GPIO.LOW)  # CLOSE COOLING VALVES
    GPIO.output(exit_cooling_valve, GPIO.LOW)   
    GPIO.output(enter_gas_solenoid, GPIO.LOW)   # CLOSE PRESSURE VALVES
    GPIO.output(exit_gas_solenoid, GPIO.LOW)

def heat(target_temp, cycle_time):
    pid = PID(1, 1, 1, setpoint = target_temp)
    pid.output_limits = (0,100)
    while True:
        current_temp = read_sensors()[1]        # TIME PROPORTIONAL CONTROL
        duty_cycle = pid(current_temp)
        on_time = (duty_cycle / 100) * cycle_time
        off_time = cycle_time - on_time

        if on_time > 0:
            GPIO.output(heating_pad, GPIO.HIGH)
            time.sleep(on_time)

        if off_time > 0:
            GPIO.output(heating_pad, GPIO.LOW)
            time.sleep(off_time)

        if off_time == cycle_time:
            break

def pressure(target_pres):
    while True:
        current_pres = read_sensors()[3]
        if current_pres > target_pres:
            GPIO.output(enter_gas_solenoid, GPIO.LOW)
            GPIO.output(exit_gas_solenoid, GPIO.HIGH)
        elif current_pres < target_pres:
            GPIO.output(enter_gas_solenoid, GPIO.HIGH)
            GPIO.output(exit_gas_solenoid, GPIO.LOW)
        else:
            GPIO.output(enter_gas_solenoid, GPIO.LOW)
            GPIO.output(exit_gas_solenoid, GPIO.LOW)
            break

def cool(target_temp, cycle_time):
    while True:
        current_temp = read_sensors()[1]        
        if current_temp > target_temp:
            GPIO.output(enter_cooling_valve, GPIO.HIGH)
            GPIO.output(exit_cooling_valve, GPIO.HIGH)
            time.sleep(cycle_time)
        else:
            GPIO.output(enter_cooling_valve, GPIO.LOW)
            GPIO.output(exit_cooling_valve, GPIO.LOW)
            break

def high_pressure_cycle(cycle_count):
    for i in range(cycle_count):
        heat(target_temp)
        cool(target_temp)

def low_pressure_cycle(cycle_count):
    for i in range(cycle_count):
        heat(target_temp)
        cool(target_temp)

def main_cycle():
    while paused == False:
        pressure(target_pres)                    
        heat(target_temp)                          
        high_pressure_cycle(cycle_count)

        pressure(target_pres)                     
        heat(target_temp)           
        low_pressure_cycle(cycle_count)