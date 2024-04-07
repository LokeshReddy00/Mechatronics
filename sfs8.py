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
peak_counts = []
minutes = []

def calculate_peak_count(data):
    peak_count = 0
    for i in range(1, len(data) - 1):
        if data[i] > data[i - 1] and data[i] > data[i + 1]:
            peak_count += 1
    return peak_count

def update_plots():
    plt.clf()  # Clear previous plot
    
    # Pressure vs. time graph
    plt.subplot(2, 1, 1)
    plt.plot(timestamps, pressures, 'b-')
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Live Pressure vs Time Graph')
    plt.grid(True)
    
    # Peak count per minute bar graph
    plt.subplot(2, 1, 2)
    plt.bar(minutes, peak_counts, color='g')
    plt.xlabel('Time (in minutes)')
    plt.ylabel('Peak Count')
    plt.title('Peak Count per Minute')
    plt.grid(True)
    plt.tight_layout()

try:
    minute_start_time = datetime.now()
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

        # Check if a new minute has started
        if (timestamp - minute_start_time).seconds >= 60:
            minute_start_time = timestamp
            minutes.append(len(peak_counts) + 1)
            peak_count = calculate_peak_count(pressures[-60:])  # Calculate peak count for the last minute
            peak_counts.append(peak_count)
            print("Minute:", len(peak_counts), "Peak Count:", peak_count)

        # Update plots
        update_plots()
        plt.pause(0.05)  # Pause for a short duration to update the plot

except KeyboardInterrupt:
    # Close serial connection
    ser.close()
