from simple_pid import PID
from qrcode import GetQRCode
import numpy as np
import cv2

Kp = 10; #proportional gain
Ki = 2; #integral gain
Kd = 0; #derivative gain

control_limit = 35; 

class pid_controller():
    def __init__(self):
        self.pid = PID(Kp, Ki, Kd, setpoint=0) #PID controller initialization
        self.pid.output_limits = (0, control_limit) #limit the input that is given to the motor to 0 - 10% duty cycle

    def get_rotation_speed(self, input_x):
        x = -np.abs(input_x) #give the x always a negative sign

        #Prevent too high values for integral gain when error is low
        # Condition for disabling integral term
        small_error_threshold = 0.01; 
        if abs(input_x) < small_error_threshold:
            control_output = 0 
        else:
            control_output = self.pid(x)

        control_output = max(0, min(control_limit, control_output)) #maybe a bit double with setting output limits?
        rotation_direction = 0 if input_x > 0 else 1 #define the rotation direction based on the sign of offset x 

        return rotation_direction, control_output

if __name__ == '__main__':
    code = GetQRCode()
    pid_controller = pid_controller()

    while True:
        x = code.QRCodeDisplay()
        print('x offset', x)
        direction, control_output = pid_controller.get_rotation_speed(x)
        print('direction', direction)
        print('control_output', control_output)

        c = cv2.waitKey(10)

        if c == 27:
            code.EndQRCode()