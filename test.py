import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)

SO  = 21
SCK = 23
CS  = 29

GPIO.setup(SCK, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(CS, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(SO, GPIO.IN)

def read_max6675():
    GPIO.output(CS, GPIO.LOW)
    time.sleep(0.001)

    value = 0
    for i in range(16):
        GPIO.output(SCK, GPIO.HIGH)
        time.sleep(0.0001)
        value = (value << 1) + GPIO.input(SO)
        GPIO.output(SCK, GPIO.LOW)
        time.sleep(0.0001)

    GPIO.output(CS, GPIO.HIGH)
    return value

raw = read_max6675()
temp_c = (raw >> 3) * 0.25
print(f"Raw=0x{raw:04X}, Temp={temp_c:.2f} °C")

GPIO.cleanup()
