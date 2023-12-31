import cv2 
import matplotlib.pyplot as plt
from motor_controller import motor_controller
from qrcode_test import GetQRCode 
from pid_controller import pid_controller
from plots import Plot
from rotary_encoder_rpm import RotaryEncoder
import time
import csv

#Pin definitions
RPWM = 19;  # GPIO pin 19 to the RPWM on the BTS7960
LPWM = 13;  #GPIO pin 13 to the LPWM on the BTS7960
R_EN = 20;
L_EN = 21; # connect GPIO pin 21 to L_EN on the BTS7960

code = GetQRCode()
pid_controller = pid_controller()
control = motor_controller(RPWM, LPWM, L_EN, R_EN)
#time_last_QR = time.time()

ppr = 500   #rotary encoder ppr, specification of the motor

error = []          #array with all error values, empty initialization
motor_input= []     #array with all motor input values, empty initialization
direc = []           #array with all direction values, empty initialization

start = False 


#initialize variables for detection rate calculation
x_total = []
x_detection = []

timer_start_time = None

#prompt user input about test conditions
# qr_code_size = input("Enter QR Code Size: ") #small, medium, large
# n_codes = input("Enter number of QR codes:") #enter number 1-3
# code_location = input("Enter location of QR codes:")  #(shoulder, knee, hip, ankle, head)
# walking_speed = input("Enter speed:") #static, slow, fast
print("Press Enter to start or ESC to quit:")
try:
    while True: #infinite loop
        x = code.QRCodeDisplay() #offset in m
        #print('x offset', x)
        c = cv2.waitKey(10)  #wait for a duration of 10 ms 
        #lighting_condition = input("Enter Lighting Condition: ")
        

        
        if c == 13: #start if 'Enter is pressed'
            time_last_QR = time.time()                              #time initialization
            print('First QR:', time_last_QR)
            time_interval = 0.5                                     #interval on which QR code is not detected and motor should stop
            time_out_duration = 5 
            timer_start_time = time.time()
            #start = True

        if timer_start_time is not None:
            elapsed_time = time.time() - timer_start_time
            if elapsed_time > 5:  # Wait 5 seconds before starting the test, time to initialize to the right position
                print('start = True')
                start = True
                tracking_start_time = time.time()

        if start:
            x_total, x_detection, detection_rate = code.QR_detection_rate(x, x_total, x_detection)
            if x is not None:                   #if QR code is being detected
                time_last_QR = time.time()
                direction, control_output = pid_controller.get_rotation_speed(x)
                error.append(x) #create an array with all error values over time
                motor_input.append(control_output) #create array with all control outputs over time
                direc.append(direction)

                if direction ==1:
                    control.motor_run_left(control_output)
                    print('Offset=', x, ': Motor runs left, control output =', control_output, 'and direction =', direction)
                if direction == 0:
                    control.motor_run_right(control_output)
                    print('Offset=', x, ': Motor runs right, control output =', control_output, 'and direction =', direction)

            elif time.time()-time_last_QR > time_out_duration:
                print("Stopping execution: No QR code detected for a duration of:", time_out_duration, 'seconds')
                control_output = 0
                control.motorStop()
                break 
            
            elif x is None:
                print("QR code not detected")
                    
                if time.time()-time_last_QR > time_interval:
                        control_output = 0
                        control.motor_run_left(control_output)
                        print("Motor stop, control_ouput = ", control_output)
                        
            

        if c == 27:
            break
                                    
except KeyboardInterrupt:
    pass
       
finally: 
    control.motorStop()
    code.EndQRCode()
    
    # Open a file for appending the detection rate
    print("detection rate:", detection_rate)
    # csv_file_path = "detection_rates.csv"  
    # with open(csv_file_path, mode="a", newline="") as csv_file:
    #     csv_writer = csv.writer(csv_file)
        
    # # Write the header only if the file is empty (first time)
    #     if csv_file.tell() == 0:
    #         csv_writer.writerow(["Detection Rate", "Size", "# Codes", "Location", "S peed"])

    #     csv_writer.writerow([detection_rate, qr_code_size, n_codes, code_location, walking_speed]) #row for current execution

    
    #creating a plot to get insight in the PID control
    plt.figure(1)
    Plot.plot_motor_input(error, motor_input, direc)    #creating a plot
    plt.show()
    
