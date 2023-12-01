import RPi.GPIO as GPIO

class motor_controller():
    def __init__(self, RPWM, LPWM, L_EN, R_EN):
        GPIO.setmode(GPIO.BCM)                              #set mode to BCM
        GPIO.setwarnings(False)
        self.rpwm = RPWM
        self.lpwm = LPWM
        self.l_en = L_EN
        self.r_en = R_EN

        #initialize the pins to low
        GPIO.setup(self.rpwm, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.lpwm, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.l_en, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.r_en, GPIO.OUT, initial=GPIO.LOW)

        self.rpwm_setup = GPIO.PWM(self.rpwm, 1500)         #set PWM frequency
        self.lpwm_setup = GPIO.PWM(self.lpwm, 1500)         #set PWM frequency
        self.lpwm_setup.start(0)                            #initialize dutycycle to 0
        self.rpwm_setup.start(0)                            #initialize dutycycle to 0
        GPIO.output(self.l_en, True)                        #enable L_EN
        GPIO.output(self.r_en, True)                        #enable R_EN

        self.current_direction = None                       #initialize current rotation direction to 0

    def motor_run_right(self, control_output):
        if self.current_direction != 0:                     #check if you are currently running in the direction '0 (right)' 
            self.lpwm_setup.start(0)                        #initialize dutycycle to 0
            self.rpwm_setup.start(0)
            self.lpwm_setup.ChangeDutyCycle(control_output) #change duty cycle (0-100%)
        else: 
            self.lpwm_setup.ChangeDutyCycle(control_output) #change duty cycle (0-100%)
        

    def motor_run_left(self, control_output):
       
        if self.current_direction != 1:                     #check if you are currently running in the direction '1 (lef)' 
            self.lpwm_setup.start(0)                        #initialize dutycycle to 0
            self.rpwm_setup.start(0)
            self.rpwm_setup.ChangeDutyCycle(control_output) #change duty cycle (0-100%)
        else: 
            self.rpwm_setup.ChangeDutyCycle(control_output) #change duty cycle (0-100%)

    def motorStop(self): 
        GPIO.cleanup()                                      #release pins


if __name__ == '__main__':
    from motor_controller import motor_controller
    import time
    from time import sleep
    import matplotlib.pyplot as plt
    from rotary_encoder_rpm import RotaryEncoder
    from plots import Plot


        #Pin definitions
    RPWM = 19;  # GPIO pin 18 to the RPWM on the BTS7960
    LPWM = 13;  #GPIO pin 18 to the RPWM on the BTS7960
    R_EN = 20;
    L_EN = 21; # connect GPIO pin 21 to L_EN on the BTS7960

    control = motor_controller(RPWM, LPWM, L_EN, R_EN)
    control.motor_run_left(0.5)
    time.sleep(0.5)
    # control.motor_run_left(0.005)
    # time.sleep(2)
    # control.motor_run_left(60)
    # time.sleep(1)
    control.motorStop()

    
    # PIN_A, PIN_B = RotaryEncoder.setup_GPIO()
    # ppr = 500  # Resolution: Pulses Per Revolution of the encoder, specification of the encoder 

    # time_values, counter_values, direction_values, rpm_values, last_time_values = RotaryEncoder.run_encoder(ppr, PIN_A, PIN_B)
    # data = list(zip(time_values, counter_values, direction_values, rpm_values, last_time_values))
    # RotaryEncoder.save_to_csv("encoder_data.csv", data)

    # Plot.plot_encoder(time_values, counter_values, direction_values, rpm_values)
    # plt.show()