import tkinter as tk
import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BOARD)

spi_bus = spidev.SpiDev()
spi_bus.open(0,0)
spi_bus.max_speed_hz = 500000

ent_cooling_valve = 16      # GPIO 23
ext_cooling_valve = 18      # GPIO 24
ent_gas_valve = 32          # GPIO 12
ext_gas_valve = 36          # GPIO 16

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

    def toggle_solenoid(self, index):
        self.solenoid_states[index] = not self.solenoid_states[index]
        color = "green" if self.solenoid_states[index] else "red"
        self.solenoid_labels[index].config(bg=color)

    def toggle_heater(self):
        self.heater_state = not self.heater_state
        color = "green" if self.heater_state else "red"
        self.heater_label.config(bg=color)
        
    def update_sensors(self):

        tc1 = self.read_thermocouples()
        # pressure = 
        # flow = 

        self.tc1_label.config(text=f"Thermocouple 1: {tc1} °C")
        # self.pressure_label.config(text=f"Pressure: {pressure} kPa")
        # self.flow_label.config(text=f"Flow: {flow} L/min")

        self.after(1000, self.update_sensors)
    
    def read_thermocouples():
        raw = spi_bus.xfer2([0x00, 0x00])
        value = (raw[0] << 8 | raw[1])
        temperature = (value >> 3) * 0.25
        return temperature
    
    def relay_setup():
        GPIO.setup(ent_cooling_valve, GPIO.OUT)
        GPIO.setup(ext_cooling_valve, GPIO.OUT)
        GPIO.setup(ent_gas_valve, GPIO.OUT)
        GPIO.setup(ext_gas_valve, GPIO.OUT)

    def startup():
        GPIO.output(ent_cooling_valve, 0)
        GPIO.output(ext_cooling_valve, 0)
        GPIO.output(ent_gas_valve, 0)
        GPIO.output(ext_gas_valve, 0)
    
def run():
    root = ControlPanel()
    root.title("Control Panel")
    root.mainloop()
     
if __name__ == "__main__":
    run()