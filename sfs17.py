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
peak_counts = []  # Store peak counts for each minute
stride_times = deque(maxlen=100)  # Store stride times

def calculate_peak_count(data):
    peak_count = 0
    for i in range(1, len(data)-1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            peak_count += 1
    return peak_count

def update_plots():
    plt.clf()  # Clear previous plot

    # Pressure vs. time graph
    plt.subplot(3, 1, 1)
    plt.plot(timestamps, pressures, 'b-')
    plt.xlabel('Time')
    plt.ylabel('Pressure')
    plt.title('Live Pressure vs Time Graph')
    plt.grid(True)

    # Peak count per minute bar graph
    plt.subplot(3, 1, 2)
    plt.bar(range(len(peak_counts)), peak_counts, color='g')
    plt.xlabel('Minute')
    plt.ylabel('Peak Count')
    plt.title('Peak Count per Minute')
    plt.grid(True)

    # Stride time graph
    plt.subplot(3, 1, 3)
    plt.plot(stride_times, 'r-')
    plt.xlabel('Reading')
    plt.ylabel('Stride Time (s)')
    plt.title('Stride Time')
    plt.grid(True)

    # Calculate time interval between peaks
    if len(peak_counts) >= 2:
        peak_interval = (timestamps[-1] - timestamps[-2]).total_seconds()
        print("Time Interval Between Peaks:", peak_interval)
    
    plt.tight_layout()

try:
    minute_start_time = datetime.now()
    current_minute = minute_start_time.minute
    prev_timestamp = minute_start_time  # Previous timestamp
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

        # Calculate stride time (time interval between readings)
        stride_time = (timestamp - prev_timestamp).total_seconds()
        stride_times.append(stride_time)
        prev_timestamp = timestamp

        # Calculate peak count
        peak_count = calculate_peak_count(pressures)

        # Check if a new minute has started
        if timestamp.minute != current_minute:
            current_minute = timestamp.minute
            print("Minute:", timestamp.strftime('%Y-%m-%d %H:%M'), "Peak Count:", peak_count)
            peak_counts.append(peak_count)
            # Clear data for the new minute
            timestamps = []
            pressures = []

       
        update_plots()
        plt.pause(0.05)  

except KeyboardInterrupt:
    ser.close()
