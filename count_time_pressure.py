import serial
import matplotlib.pyplot as plt
from datetime import datetime

# Establish serial connection with Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct serial port
ser.flushInput()

# Initialize empty lists to store data
timestamps = []
pressures = []
pressure_count = []  # Store pressure count per minute
start_time = datetime.now()

# Initialize variables for counting pressure per minute
pressure_per_min = 0
prev_minute = start_time.minute

try:
    while True:
        # Read data from serial port
        line = ser.readline().decode().strip()

        # Extract data from the line
        try:
            time_str, count_str, pressure_str = line.strip('()').split(', ')
            time = int(time_str)
            count = int(count_str)
            pressure = int(pressure_str)
        except ValueError:
            print("Invalid data format:", line)
            continue

        # Append data to lists
        timestamps.append(datetime.fromtimestamp(time))
        pressures.append(pressure)
        pressure_count.append(count)

        # Count pressure per minute
        current_time = datetime.now()
        if current_time.minute != prev_minute:
            pressure_per_min = count
            prev_minute = current_time.minute
            print("Pressure count per minute:", pressure_per_min)

        # Print data to console
        print("Time:", time, "Pressure count:", count, "Pressure:", pressure)

        # Plot live graph
        plt.figure(1)
        plt.subplot(3, 1, 1)
        plt.plot(timestamps, pressures, 'b-')
        plt.xlabel('Time')
        plt.ylabel('Pressure')
        plt.title('Pressure vs Time')

        # Plot pressure count vs time
        plt.subplot(3, 1, 2)
        plt.plot(timestamps, pressure_count, 'r-')
        plt.xlabel('Time')
        plt.ylabel('Pressure Count')
        plt.title('Pressure Count vs Time')

        # Plot pressure count per minute
        plt.subplot(3, 1, 3)
        plt.bar(range(len(pressure_count)), pressure_count, color='g')
        plt.xlabel('Time (minutes)')
        plt.ylabel('Pressure Count')
        plt.title('Pressure Count per Minute')

        plt.tight_layout()
        plt.pause(0.05)  # Pause for a short duration to update the plot

except KeyboardInterrupt:
    # Close serial connection
    ser.close()
