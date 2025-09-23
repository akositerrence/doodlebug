from max31855 import MAX31855, MAX31855Error

cs_pin=26
clock_pin=23
data_pin=22
unit="f"
thermocouple1=MAX31855(cs_pin, clock_pin, data_pin)
print(thermocouple1.get())
thermocouple1.cleanup()