import serial
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import deque

# Establish serial connection with Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct serial port
ser.flushInput()

# Initialize empty lists to store data
timestamps = deque(maxlen=100)  # Store only the latest 100 timestamps
pressures = deque(maxlen=100)    # Store only the latest 100 pressures
peak_counts = []  # Store peak counts for each minute
stride_times = []  # Store stride times
peak_count_per_min = []  # Store peak count per minute for later analysis

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
    
    plt.tight_layout()

try:
    while True:
        # Read data from serial port
        line = ser.readline().decode().strip()

        # Extract pressure value from the line
        try:
            # Assuming the format of the data is (timestamp, pressure)
            data_parts = line.strip('()').split(',')
            timestamp = datetime.now()
            pressure = float(data_parts[1])
        except (ValueError, IndexError):
            print("Invalid data format:", line)
            continue

        # Append data to lists
        timestamps.append(timestamp)
        pressures.append(pressure)

        # Calculate stride time (time interval between readings)
        if len(timestamps) >= 2:
            stride_time = (timestamp - timestamps[-2]).total_seconds()
            stride_times.append(stride_time)

        # Calculate peak count
        peak_count = calculate_peak_count(pressures)

        # Check if a new minute has started
        if len(timestamps) >= 2 and timestamp.minute != timestamps[-2].minute:
            print("Minute:", timestamp.strftime('%Y-%m-%d %H:%M'), "Peak Count:", peak_count)
            peak_counts.append(peak_count)
            peak_count_per_min.append(peak_count)  # Store peak count per minute for later analysis

        update_plots()
        plt.pause(0.05)

# Ensure all arrays have the same length before creating DataFrame
        min_length = min(len(timestamps), len(pressures), len(peak_counts), len(stride_times))
        data = {
        'Timestamp': pd.Series([t.strftime('%Y-%m-%d %H:%M:%S') for t in list(timestamps)[-min_length:]]),
        'Pressure': list(pressures)[-min_length:],
        'Peak_Count': peak_counts[-min_length:],
        'Stride_Time': stride_times[-min_length:]
        }
        df = pd.DataFrame(data)
        df.to_excel('data.xlsx', index=False)


except KeyboardInterrupt:
    ser.close()
