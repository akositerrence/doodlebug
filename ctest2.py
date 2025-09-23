# file: mx55_manual_cs_diag.py
import time
import spidev
import RPi.GPIO as GPIO

# ---- Edit these if your wiring differs ----
BOARD_CS   = 29   # your current CS on BOARD 29 (GPIO5)
# SCK must be on SPI0 SCLK (BOARD 23 / GPIO11)
# SO must be on SPI0 MISO (BOARD 21 / GPIO9)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BOARD_CS, GPIO.OUT, initial=GPIO.HIGH)

spi = spidev.SpiDev()
spi.open(0, 0)           # SPI0; device index is irrelevant since we disable HW CS
spi.mode = 0
spi.max_speed_hz = 5_000_000
spi.no_cs = True         # <<< IMPORTANT: we'll drive CS ourselves

def read_once():
    # assert CS low, read 4 bytes, deassert CS
    GPIO.output(BOARD_CS, GPIO.LOW)
    raw = spi.readbytes(4)
    GPIO.output(BOARD_CS, GPIO.HIGH)

    val = (raw[0]<<24) | (raw[1]<<16) | (raw[2]<<8) | raw[3]

    fault_flag = (val >> 16) & 1
    oc  = (val >> 2) & 1
    scg = (val >> 1) & 1
    scv = val & 1

    tc = (val >> 18) & 0x3FFF
    if tc & 0x2000: tc -= 0x4000
    tc_c = tc * 0.25

    cj = (val >> 4) & 0x0FFF
    if cj & 0x800: cj -= 0x1000
    cj_c = cj * 0.0625

    return raw, val, tc_c, cj_c, fault_flag, oc, scg, scv

try:
    for _ in range(5):
        raw, val, tc, cj, ff, oc, scg, scv = read_once()
        print(f"raw={raw}  val=0x{val:08X}  TC={tc:.2f} °C  CJ={cj:.2f} °C  "
              f"fault_flag={ff} oc={bool(oc)} scg={bool(scg)} scv={bool(scv)}")
        time.sleep(0.25)
finally:
    spi.close()
    GPIO.cleanup()
