import serial
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Establish serial connection with Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct serial port
ser.flushInput()

# Initialize empty lists to store data for FSR1 and FSR2
timestamps1 = []
pressures1 = []

timestamps2 = []
pressures2 = []

def update_plots():
    plt.clf()  # Clear previous plot

    # Pressure vs. time graph for FSR1
    plt.subplot(2, 1, 1)
    plt.plot(timestamps1, pressures1, 'b-')
    plt.xlabel('Time')
    plt.ylabel('Pressure FSR1')
    plt.title('FSR1 Live Pressure vs Time Graph')
    plt.grid(True)

    # Pressure vs. time graph for FSR2
    plt.subplot(2, 1, 2)
    plt.plot(timestamps2, pressures2, 'r-')
    plt.xlabel('Time')
    plt.ylabel('Pressure FSR2')
    plt.title('FSR2 Live Pressure vs Time Graph')
    plt.grid(True)
    
    plt.tight_layout()

try:
    while True:
        # Read data from serial port
        line = ser.readline().decode().strip()

        # Check if the line starts with 'FSR1' or 'FSR2'
        if line.startswith('FSR1'):
            # Extract timestamp and pressure values from FSR1 line
            data_str = line[len('FSR1 '):-1]  # Remove 'FSR1 ' at the beginning and ')' at the end
            time_str, pressure_str = data_str.split(', ')
            timestamp = datetime.now()  # Use current time
            pressure = float(pressure_str)
            timestamps1.append(timestamp)
            pressures1.append(pressure)

        elif line.startswith('FSR2'):
            # Extract timestamp and pressure values from FSR2 line
            data_str = line[len('FSR2 '):-1]  # Remove 'FSR2 ' at the beginning and ')' at the end
            time_str, pressure_str = data_str.split(', ')
            timestamp = datetime.now()  # Use current time
            pressure = float(pressure_str)
            timestamps2.append(timestamp)
            pressures2.append(pressure)

        # Update the plots
        update_plots()
        plt.pause(0.05)  

except KeyboardInterrupt:
    ser.close()

# Store data in an Excel sheet for FSR1
data1 = {'Timestamp_FSR1': [t.strftime('%Y-%m-%d %H:%M:%S') for t in timestamps1],
         'Pressure_FSR1': pressures1}
df1 = pd.DataFrame(data1)
df1.to_excel('data_fsr1.xlsx', index=False)

# Store data in an Excel sheet for FSR2
data2 = {'Timestamp_FSR2': [t.strftime('%Y-%m-%d %H:%M:%S') for t in timestamps2],
         'Pressure_FSR2': pressures2}
df2 = pd.DataFrame(data2)
df2.to_excel('data_fsr2.xlsx', index=False)
