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

        # Print data to console
        print(timestamp, pressure)

        # Plot live graph
        plt.plot(timestamps, pressures, 'b-')  # Plot timestamps on x-axis and pressures on y-axis
        plt.xlabel('Time')
        plt.ylabel('Pressure')
        plt.title('Live Pressure vs Time Graph')
        plt.grid(True)
        plt.pause(0.05)  # Pause for a short duration to update the plot

except KeyboardInterrupt:
    # Close serial connection
    ser.close()
