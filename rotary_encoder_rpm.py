import RPi.GPIO as GPIO
import time
from time import sleep


class RotaryEncoder:
    def setup_GPIO():
        PIN_A = 23
        PIN_B = 24
        #set GPIO pins to input with pull down resistor 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(PIN_B, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)

        return PIN_A, PIN_B

    def read_encoder(PIN_A, PIN_B, pinA_laststate, counter, time_zero, direction, last_time):
        pinA_state = GPIO.input(PIN_A)      #current state of pin A
        pinB_state = GPIO.input(PIN_B)      #current state of pin B
        current_time = time.time()
        elapsed_time = current_time - time_zero  #elapsed time since start
        last_time = current_time - last_time


        if pinA_state != pinA_laststate:    #check if rotator has been rotated 
            if pinB_state != pinA_state:    #if pinA unequal to pinB state -> rotating in clockwise direction
                counter += 1
                direction = 1               #clockwise rotation

            else:                           #else, rotating in ccw direction
                counter -= 1 
                direction = 0              #ccw direction

            # current_time = time.time()
            # elapsed_time = current_time - time_zero  #elapsed time since start
            # last_time = current_time - last_time

            return counter, direction, pinA_state, elapsed_time, last_time
        else:
            return counter, direction, pinA_laststate, elapsed_time, last_time
        
    def calculate_rpm(ppr, counter, last_time):
            dt = last_time
            rpm = (counter / ppr) / dt * 60
            return rpm
       
    
    def run_encoder(ppr, PIN_A, PIN_B):
        import RPi.GPIO as GPIO
        counter = 0 #start counting at 0
        direction = 0
        start_counter = 0
        pinA_laststate = GPIO.input(PIN_A) #set initial state of pin A

        #create lists to store data for plotting later
        time_values = [] 
        counter_values = []
        direction_values = []
        rpm_values = []
        last_time_values = []

        last_time = time.time() #start time iteration
        time_zero = time.time()  #starting time


        try: 
            while True:
                counter, direction, pinA_laststate, elapsed_time, last_time = RotaryEncoder.read_encoder(PIN_A, PIN_B, pinA_laststate, counter, time_zero, direction, last_time)
                rpm =  RotaryEncoder.calculate_rpm(ppr, counter, last_time)
                rpm = abs(rpm) #take speed as absolute value
                print('Counter:', counter, 'direction:', direction, 'RPM:', rpm)
                time_values.append(elapsed_time)
                counter_values.append(counter)
                direction_values.append(direction)
                last_time_values.append(last_time)
                rpm_values.append(rpm)
                sleep_time = 0.01 #check if this influences the counter
                sleep(sleep_time)                         #pause script

        except KeyboardInterrupt:
            pass

        finally:            
            RotaryEncoder.cleanup_gpio()                   #clean GPIO pins

        return time_values, counter_values, direction_values, rpm_values, last_time_values 
    
    def save_to_csv(filename, data):
        import csv
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time' , 'Counter' , 'Direction' , 'RPM', 'dt'])
            writer.writerows(data)
    
    def cleanup_gpio():
        GPIO.cleanup()



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from rotary_encoder_rpm import RotaryEncoder
    from plots import Plot
    
    PIN_A, PIN_B = RotaryEncoder.setup_GPIO()
    ppr = 500  # Resolution: Pulses Per Revolution of the encoder, specification of the encoder 

    time_values, counter_values, direction_values, rpm_values, last_time_values = RotaryEncoder.run_encoder(ppr, PIN_A, PIN_B)
    data = list(zip(time_values, counter_values, direction_values, rpm_values, last_time_values))
    RotaryEncoder.save_to_csv("encoder_data.csv", data)

    Plot.plot_encoder(time_values, counter_values, direction_values, rpm_values)
  