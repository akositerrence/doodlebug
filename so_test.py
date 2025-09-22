import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
SO = 21
GPIO.setup(SO, GPIO.IN)

for i in range(20):
    print(GPIO.input(SO))
    time.sleep(0.5)

GPIO.cleanup()
