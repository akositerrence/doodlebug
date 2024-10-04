class thermocouple:
    def __init__(self, serial_clock, chip_select, serial_data_out):
        global max6675
        self.CLK = serial_clock
        self.CS
        self.DO
        max6675 = MAX6675.MAX6675(CLK, CS, DO)

    def get_temp():
        return max6675.readTempC()
