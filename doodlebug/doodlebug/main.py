import tkinter as tk
import time
import embedded

import RPi.GPIO as GPIO
import spidev, time

spi = spidev.SpiDev()
spi.open(0, 1)                 
spi.mode = 0
spi.max_speed_hz = 5_000_000

GPIO.setmode(GPIO.BOARD)

class ControlPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Status")
        self.geometry("750x750")
        self.solenoid_states = [False, False, False, False]
        self.heater_state = False
        
        ### HEADER ###
        title = tk.Label(self, text="SOLENOIDS", font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        ### SOLENOIDS ###
        self.solenoid_labels = []
        for i in range(4):
            label = tk.Label(self, text = f"Solenoid {i+1}", width = 10, height = 2, bg = "red", fg = "white")
            label.grid(row = i+1, column = 0, padx = 5, pady = 2.5)
            self.solenoid_labels.append(label)

            btn = tk.Button(self, text = f"Toggle {i+1}", width = 10, height = 2, command = lambda i=i : self.toggle_solenoid(i))
            btn.grid(row = i+1, column = 1, padx = 10, pady = 2.5)
        
        ### HEATERS ###
        self.heater_label = tk.Label(self, text = "Heater", width = 10, height = 2, bg = "red", fg = "white")
        self.heater_label.grid(row = 5, column = 0, padx = 10, pady = 2.5)

        self.heater_btn = tk.Button(self, text = "Toggle Heater", width = 10, height = 2, command = self.toggle_heater)
        self.heater_btn.grid(row = 5, column = 1, padx = 10, pady = 2.5)
        
        ### SENSORS ###
        sensor_title = tk.Label(self, text="SENSORS", font=("Arial", 14, "bold"))
        sensor_title.grid(row=  7, column = 0, columnspan = 2, pady = 10)

        self.tc1_label = tk.Label(self, text="Thermocouple 1: -- °F", width=25, anchor="w")
        self.tc1_label.grid(row = 8 , column = 0 , columnspan = 2, sticky = "w", padx = 10)

        self.tc2_label = tk.Label(self, text="Thermocouple 2: -- °F", width=25, anchor="w")
        self.tc2_label.grid(row = 9, column = 0, columnspan = 2, sticky = "w", padx = 10)

        self.pressure_label = tk.Label(self, text="Pressure: -- PSI", width=25, anchor="w")
        self.pressure_label.grid(row = 10, column = 0, columnspan = 2, sticky = "w", padx = 10)

        self.flow_label = tk.Label(self, text="Flow: -- L/min", width=25, anchor="w")
        self.flow_label.grid(row= 11, column = 0, columnspan = 2, sticky = "w", padx = 10)
        
        ### SETTINGS ###
        limit_title = tk.Label(self, text="SETTINGS", font=("Arial", 14, "bold"))
        limit_title.grid(row=12, column=0, columnspan=2, pady=10)

        tk.Label(self, text="Min Temp (°F):").grid(row=13, column=0, sticky="e", padx=5)
        self.min_temp_entry = tk.Entry(self, width=10)
        self.min_temp_entry.grid(row=13, column=1, sticky="w", padx=5)

        tk.Label(self, text="Max Temp (°F):").grid(row=14, column=0, sticky="e", padx=5)
        self.max_temp_entry = tk.Entry(self, width=10)
        self.max_temp_entry.grid(row=14, column=1, sticky="w", padx=5)

        tk.Label(self, text="Min Pressure (kPa):").grid(row=15, column=0, sticky="e", padx=5)
        self.min_pressure_entry = tk.Entry(self, width=10)
        self.min_pressure_entry.grid(row=15, column=1, sticky="w", padx=5)

        tk.Label(self, text="Max Pressure (kPa):").grid(row=16, column=0, sticky="e", padx=5)
        self.max_pressure_entry = tk.Entry(self, width=10)
        self.max_pressure_entry.grid(row=16, column=1, sticky="w", padx=5)

        self.min_temp_entry.insert(0, "30")
        self.max_temp_entry.insert(0, "110")
        self.min_pressure_entry.insert(0, "14")
        self.max_pressure_entry.insert(0, "15")
        
        ### LOOP ###

    def toggle_solenoid(self, index):
        self.solenoid_states[index] = not self.solenoid_states[index]
        color = "green" if self.solenoid_states[index] else "red"
        self.solenoid_labels[index].config(bg=color)
        embedded.close_relay(index + 1)
        if self.solenoid_states[index]:
            embedded.close_relay(index + 1)
        else:
            embedded.open_relay(index + 1)
        
    def toggle_heater(self):
        self.heater_state = not self.heater_state
        color = "green" if self.heater_state else "red"
        self.heater_label.config(bg=color)
        if self.heater_state:
            embedded.close_relay(4)
        else:
            embedded.open_relay(4)
        
    def update_sensors(self):
        tc1 = self.read_thermocouples()
        # pressure = 
        # flow = 
        self.tc1_label.config(text=f"Thermocouple 1: {tc1} °C")
        # self.pressure_label.config(text=f"Pressure: {pressure} kPa")
        # self.flow_label.config(text=f"Flow: {flow} L/min")

        self.after(1000, self.update_sensors)
    
    def read_thermocouples():
        raw = spi.readbytes(4)
        val = (raw[0]<<24)|(raw[1]<<16)|(raw[2]<<8)|raw[3]

        if (val >> 16) & 1:
            oc  = bool((val >> 2) & 1)
            scg = bool((val >> 1) & 1)
            scv = bool(val & 1)
            raise RuntimeError(f"Fault: open={oc}, short_gnd={scg}, short_vcc={scv}")

        tc = (val >> 18) & 0x3FFF
        if tc & 0x2000: tc -= 0x4000
        tc_c = tc * 0.25

        # Internal (cold junction): bits 15..4, signed, 0.0625 °C/LSB
        # cj = (val >> 4) & 0x0FFF
        # if cj & 0x800: cj -= 0x1000
        # cj_c = cj * 0.0625

        return tc_c
    
def run():
    ### LOOP STARTUP ###
    embedded.relay_setup()
    embedded.startup()
    
    ### GUI STARTUP ###
    root = ControlPanel()
    root.title("Control Panel")
    root.mainloop()
     
if __name__ == "__main__":
    run()