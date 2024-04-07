import serial
import pandas as pd
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

        # Extract pressure value from the line
        try:
            _, pressure_str = line.strip('()').split(', ')
            pressure = float(pressure_str)
        except ValueError:
            print("Invalid data format:", line)
            continue

        # Extract timestamp
        timestamp = datetime.now()

        # Append data to lists
        timestamps.append(timestamp)
        pressures.append(pressure)

        # Count pressure per minute
        if timestamp.minute != prev_minute:
            pressure_count.append(pressure_per_min)
            pressure_per_min = 0
            prev_minute = timestamp.minute
            print("Count per minute:", pressure_per_min)  # Print count per minute

        pressure_per_min += 1

        # Print data to console
        print(timestamp, pressure)

        # Plot live graph
        plt.subplot(2, 1, 1)
        plt.plot(timestamps, pressures, 'b-')  # Plot timestamps on x-axis and pressures on y-axis
        plt.xlabel('Time')
        plt.ylabel('Pressure')
        plt.title('Live Pressure vs Time Graph')
        plt.grid(True)

        # Plot pressure count per minute as a bar graph
        plt.subplot(2, 1, 2)
        plt.bar(range(len(pressure_count)), pressure_count, color='r')
        plt.xlabel('Time (minutes)')
        plt.ylabel('Pressure Count')
        plt.title('Pressure Count per Minute')

        # Add count labels on top of each bar
        for i, count in enumerate(pressure_count):
            plt.text(i, count + 0.1, str(count), ha='center', va='bottom')

        plt.grid(True)

        plt.tight_layout()
        plt.pause(0.05)  # Pause for a short duration to update the plot

except KeyboardInterrupt:
    # Close serial connection
    ser.close()
