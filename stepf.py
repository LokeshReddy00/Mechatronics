import serial
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import deque

# Establish serial connection with Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct serial port
ser.flushInput()

# Initialize empty lists to store data
timestamps = []
pressures = []
peak_counts = deque(maxlen=60)  # Store peak counts for last 60 seconds

def calculate_peak_count(data):
    peak_count = 0
    for i in range(1, len(data)-1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            peak_count += 1
    return peak_count

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

        # Calculate peak count
        peak_count = calculate_peak_count(pressures[-60:])  # Calculate peak count for last 60 seconds
        peak_counts.append(peak_count)

        # Print data to console
        print(timestamp, pressure, "Peak Count:", peak_count)

        # Plot live graph
        plt.clf()  # Clear previous plot
        plt.subplot(2, 1, 1)  # Pressure graph
        plt.plot(timestamps, pressures, 'b-')  # Plot timestamps on x-axis and pressures on y-axis
        plt.xlabel('Time')
        plt.ylabel('Pressure')
        plt.title('Live Pressure vs Time Graph')
        plt.grid(True)

        # Plot bar graph for peak counts
        plt.subplot(2, 1, 2)  # Peak count bar graph
        plt.bar(range(len(peak_counts)), peak_counts, color='g')
        plt.xlabel('Time (in seconds)')
        plt.ylabel('Peak Count')
        plt.title('Peak Count per Minute')
        plt.grid(True)

        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.pause(0.05)  # Pause for a short duration to update the plot

except KeyboardInterrupt:
    # Close serial connection
    ser.close()
