import cv2 
import matplotlib.pyplot as plt
from motor_controller import motor_controller
from qrcode import GetQRCode 
from pid_controller import pid_controller
from plots import Plot
from rotary_encoder_rpm import RotaryEncoder
import time


     #Pin definitions
RPWM = 19;  # GPIO pin 18 to the RPWM on the BTS7960
LPWM = 13;  #GPIO pin 18 to the RPWM on the BTS7960
R_EN = 20;
L_EN = 21; # connect GPIO pin 21 to L_EN on the BTS7960

code = GetQRCode()
pid_controller = pid_controller()
control = motor_controller(RPWM, LPWM, L_EN, R_EN)

ppr = 500   #rotary encoder ppr, specification of the motor

error = []          #array with all error values, empty initialization
motor_input= []     #array with all motor input values, empty initialization
direc = []           #array with all direction values, empty initialization

start = False 
print("Press Enter to start or ESC to quit:")

try:
    while True: #infinite loop
        x = code.QRCodeDisplay() # in m
        print('x offset', x)
        direction, control_output = pid_controller.get_rotation_speed(x)
        c = cv2.waitKey(10)
        error.append(x) #create an array with all error values over time
        motor_input.append(control_output) #create array with all control outputs over time
        direc.append(direction)
        
        # #include encoder data
        # PIN_A, PIN_B = RotaryEncoder.setup_GPIO()
        

        # time_values, counter_values, direction_values, rpm_values, last_time_values = RotaryEncoder.run_encoder(ppr, PIN_A, PIN_B)
        
        if c == 13:
            time_last_QR = time.time()                              #time initialization
            print('First QR:', time_last_QR)
            time_interval = 0.5                                     #interval on which QR code is not detected and motor should stop
            time_out_duration = 10  
            
            start = True

        if start:

            # if time.time()-time_last_QR > time_out_duration: #stop if QR code isn't detected for a while
            #     print("Stopping execution: No QR code detected for a duration of:", time_out_duration)
            #     break 

            # if time.time()-time_last_QR > time_interval: #stop motor if QR code isn't detected for a while
            #     print("Motor stop")
            #     control.motorStop()

            # # else:
            # if direction ==1:
            #     control.motor_run_left(control_output)
            #     print('motor runs left with speed control output', control_output, ' and direction', direction)
            # if direction == 0:
            #     control.motor_run_right(control_output)
            #     print('motor runs right with speed control output', control_output, ' and direction', direction)

                
            print('motor runs left with speed control output', control_output, ' and direction', direction)    

        if c == 27:
            break
                                    
except KeyboardInterrupt:
    pass
       
finally: 
    control.motorStop()
    code.EndQRCode()

    #creating a plot to get insight in the PID control
    plt.figure(1)
    Plot.plot_motor_input(error, motor_input, direc)    #creating a plot
    plt.show()
    
  
    #creating the encoder data
    
    