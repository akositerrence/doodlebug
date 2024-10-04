class control:
    def __init__(self, P, I, D, S, T, t):
        global delta, time
        self.setpoint = S
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.thermocouple = T
        time = t

        self.measurement = self.thermocouple.get_temp()
        delta = self.setpoint - self.measurement

    def output(self):
        global prev_delta, prev_time
        self.proportional = self.Kp * delta
        self.integral = self.Ki * delta * (time - prev_time)
        self.derivative = self.Kd * ((delta - prev_delta)/(time - prev_time))

        output = self.proportional + self.integral + self.derivative
        prev_delta = delta
        prev_time = time

        return output