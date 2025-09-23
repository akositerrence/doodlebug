import os, time
import spidev

def decode_max31855(raw):
    val = (raw[0]<<24) | (raw[1]<<16) | (raw[2]<<8) | raw[3]

    fault_summary = {}
    fault_flag = (val >> 16) & 0x1  # D16
    scv = val & 0x1                 # D0 short to VCC
    scg = (val >> 1) & 0x1          # D1 short to GND
    oc  = (val >> 2) & 0x1          # D2 open circuit

    if fault_flag:
        fault_summary["fault_flag"] = True
        if oc:  fault_summary["open_circuit"] = True
        if scg: fault_summary["short_to_gnd"] = True
        if scv: fault_summary["short_to_vcc"] = True
    else:
        fault_summary["fault_flag"] = False

    # Thermocouple temperature (bits 31..18), signed, 0.25°C/LSB
    tc = (val >> 18) & 0x3FFF
    if tc & 0x2000:  # sign
        tc -= 0x4000
    tc_c = tc * 0.25

    # Internal temperature (bits 15..4), signed, 0.0625°C/LSB
    cj = (val >> 4) & 0x0FFF
    if cj & 0x800:
        cj -= 0x1000
    cj_c = cj * 0.0625

    return val, tc_c, cj_c, fault_summary

def try_combo(bus, dev, mode, speed):
    spi = spidev.SpiDev()
    spi.open(bus, dev)
    spi.mode = mode
    spi.max_speed_hz = speed
    spi.lsbfirst = False

    # Read twice back-to-back (second read often more “settled”)
    raw1 = spi.readbytes(4)
    time.sleep(0.01)
    raw2 = spi.readbytes(4)
    spi.close()
    return raw1, raw2

def main():
    candidates = []
    if os.path.exists("/dev/spidev0.0"):
        candidates.append((0,0))
    if os.path.exists("/dev/spidev0.1"):
        candidates.append((0,1))

    if not candidates:
        print("ERROR: No SPI devices present. Enable SPI and reboot.")
        print("  sudo raspi-config  → Interface Options → SPI → Enable")
        return

    print("Trying combos (bus,dev,mode,speedHz)…")
    any_good = False
    for (bus,dev) in candidates:
        for mode in (0,1):
            for speed in (1_000_000, 5_000_000):
                try:
                    r1, r2 = try_combo(bus, dev, mode, speed)
                    v1, tc1, cj1, f1 = decode_max31855(r1)
                    v2, tc2, cj2, f2 = decode_max31855(r2)
                    print(f"\n(bus={bus}, dev={dev}, mode={mode}, speed={speed})")
                    print(f"  raw1={r1}  val=0x{v1:08X}")
                    print(f"    tc={tc1:.2f} °C  cj={cj1:.2f} °C  faults={f1}")
                    print(f"  raw2={r2}  val=0x{v2:08X}")
                    print(f"    tc={tc2:.2f} °C  cj={cj2:.2f} °C  faults={f2}")

                    # Heuristics: internal (CJ) should be ~ 10..45°C at room
                    if (not f2.get("fault_flag")) and (10 <= cj2 <= 45):
                        any_good = True
                except Exception as e:
                    print(f"(bus={bus}, dev={dev}, mode={mode}, speed={speed}) -> ERROR: {e}")

    if not any_good:
        print("\nNo combo produced a sane internal (CJ) temperature.")
        print("→ If raw is [0,0,0,0] or val=0x00000000: SO is stuck low or wired to MOSI.")
        print("→ If val=0xFFFFFFFF: floating line/no device (SO pulled high).")
        print("→ If faults show open_circuit/shorts: check thermocouple & polarity.")
        print("→ Double-check SO→GPIO9(MISO, pin 21), CS→GPIO8(CE0, pin 24), SCK→GPIO11(pin 23).")

if __name__ == "__main__":
    main()
