import RPi.GPIO as GPIO
import time
from time import sleep


class RotaryEncoder:
    def setup_GPIO(PIN_A, PIN_B):
        #set GPIO pins to input with pull down resistor 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(PIN_B, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)

    def read_encoder(PIN_A, PIN_B, pinA_laststate, counter, time_zero):
        pinA_state = GPIO.input(PIN_A)      #current state of pin A
        pinB_state = GPIO.input(PIN_B)      #current state of pin B

        if pinA_state != pinA_laststate:    #check if rotator has been rotated 
            if pinB_state != pinA_state:    #if pinA unequal to pinB state -> rotating in clockwise direction
                counter += 1
                direction = 1               #clockwise rotation

            else:                           #else, rotating in ccw direction
                counter -= 1 
                direction = 0              #ccw direction

            current_time = time.time()
            elapsed_time = current_time - time_zero  #elapsed time since start

            return counter, direction, pinA_state, elapsed_time
        else:
            current_time = time.time()
            elapsed_time = current_time - time_zero  #elapsed time since start
            return counter, 0, pinA_laststate, elapsed_time
        
    def calculate_rpm(ppr, counter, elapsed_time):
        if elapsed_time > 0:
            rpm = (counter / ppr) / elapsed_time * 60
            return rpm
        else:
            return 0
    

    # def calculate_speed(PIN_A, PIN_B, time_zero):
    #     current_time = time.time()
    # #     dt = current_time - start_time           #elapsed time since last iteration
    #     elapsed_time = current_time - time_zero  #elapsed time since start
    # #     diff_counter = counter - start_counter


    # #     speed = abs(diff_counter/dt)
    # #     #update start values for next iteration
    # #     start_time = current_time
    # #     start_counter = counter

    # #     #update start values for next iteration
    # #     start_time = current_time
    # #     start_counter = counter
                

    #     return elapsed_time
    
    def cleanup_gpio():
        GPIO.cleanup()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from rotary_encoder_rpm import RotaryEncoder
    import RPi.GPIO as GPIO
    PIN_A = 23
    PIN_B = 24
    
    RotaryEncoder.setup_GPIO(PIN_A, PIN_B)
    
    counter = 0 #start counting at 0
    start_counter = 0
    pinA_laststate = GPIO.input(PIN_A) #set initial state of pin A
    ppr = 500  # Resolution: Pulses Per Revolution of the encoder, specification of the encoder 

    #create lists to store data for plotting later
    time_values = [] 
    counter_values = []
    direction_values = []
    rpm_values = []

    last_time = time.time() #start time iteration
    time_zero = time.time()  #starting time

    try: 
        while True:
            counter, direction, pinA_laststate, elapsed_time = RotaryEncoder.read_encoder(PIN_A, PIN_B, pinA_laststate, counter, time_zero)
            rpm =  RotaryEncoder.calculate_rpm(ppr, counter, elapsed_time)
            rpm = abs(rpm) #take speed as absolute value
            print('Counter:', counter, 'direction:', direction, 'RPM:', rpm)
            time_values.append(elapsed_time)
            counter_values.append(counter)
            direction_values.append(direction)
            rpm_values.append(rpm)
            sleep_time = 0.1 #check if this influences the counter
            sleep(sleep_time)                         #pause script

    except KeyboardInterrupt:
        pass

    finally:            
        RotaryEncoder.cleanup_gpio()                   #clean GPIO pins

    #plot the data
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex =True, figsize=(10,8))

    ax1.plot(time_values, counter_values, label = 'Counter')
    ax1.set_ylabel('Counter')
    ax2.plot(time_values, direction_values, label = 'Direction')
    ax2.set_ylabel('Direction')
    ax3.plot(time_values, rpm_values, label = 'RPM')
    ax3.set_ylabel('RPM')
    plt.xlabel('Time')
    plt.show()