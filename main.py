import cv2 
import matplotlib.pyplot as plt
from motor_controller import motor_controller
from qrcode import GetQRCode 
from pid_controller import pid_controller
from plots import Plot


     #Pin definitions
RPWM = 19;  # GPIO pin 18 to the RPWM on the BTS7960
LPWM = 13;  #GPIO pin 18 to the RPWM on the BTS7960
R_EN = 20;
L_EN = 21; # connect GPIO pin 21 to L_EN on the BTS7960

code = GetQRCode()
pid_controller = pid_controller()
control = motor_controller(RPWM, LPWM, L_EN, R_EN)

error = []          #array with all error values, empty initialization
motor_input= []     #array with all motor input values, empty initialization
direc = []           #array with all direction values, empty initialization

try:
    while True: #infinite loop
        x = code.QRCodeDisplay()
        print('x offset', x)
        direction, control_output = pid_controller.get_rotation_speed(x)
        print('direction', direction, 'control_output', control_output)
        c = cv2.waitKey(10)
        error.append(x) #create an array with all error values over time
        motor_input.append(control_output) #create array with all control outputs over time
        direc.append(direction)

        if direction ==1:
            control.motor_run_left(control_output)
            print('motor runs left with speed control output', control_output)
        if direction == 0:
            control.motor_run_right(control_output)
            print('motor runs right with speed control output', control_output)
                                
except KeyboardInterrupt:
    pass
       
finally: 
    control.motorStop()
    code.EndQRCode()

    #creating a plot to get insight in the PID control
    Plot.plot_motor_input(error, motor_input, direc)    #creating a plot