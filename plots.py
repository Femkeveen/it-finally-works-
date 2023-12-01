#creating the plots 

#creating a plot to get insight in the PID control
#plot relation between error and control output
class Plot():
    def plot_motor_input(error, motor_input, direc):
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(3,1)

        #plot error over time
        axes[0].plot(error)
        axes[0].set_xlabel('Time [ms]' )
        axes[0].set_ylabel('Error')

        axes[1].plot(motor_input)
        axes[1].set_xlabel('Time [ms]' )
        axes[1].set_ylabel('Control output')

        axes[2].plot(direc)
        axes[2].set_xlabel('Time [ms]' )
        axes[2].set_ylabel('Direction')
     
    def plot_encoder(time_values, counter_values, direction_values, rpm_values):
        import matplotlib.pyplot as plt
        fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex =True, figsize=(10,8))

        ax1.plot(time_values, counter_values, label = 'Counter')
        ax1.set_ylabel('Counter')
        ax2.plot(time_values, direction_values, label = 'Direction')
        ax2.set_ylabel('Direction')
        ax3.plot(time_values, rpm_values, label = 'RPM')
        ax3.set_ylabel('RPM')
        plt.xlabel('Time')
    