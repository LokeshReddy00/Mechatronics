import serial
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.signal import find_peaks
import time

# Establish serial connection with Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct serial port
ser.flushInput()

# Initialize empty lists to store data for FSR1 and FSR2
timestamps1 = []
pressures1 = []

timestamps2 = []
pressures2 = []

# Lists to store peak timestamps and times between peaks
peak_times_fsr1 = []
peak_times_fsr2 = []

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

def count_peaks(pressures, timestamps, peak_times_list):
    peaks, _ = find_peaks(pressures, prominence=0.1)  # Adjust prominence threshold as needed
    peak_timestamps = [timestamps[i] for i in peaks]
    peak_times_list.extend(peak_timestamps)
    return len(peaks)

try:
    # Ask user for duration of data collection in minutes
    duration_minutes = int(input("Enter the duration of data collection (minutes): "))
    
    end_time = time.time() + duration_minutes * 60  # Calculate end time
    
    while time.time() < end_time:
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
    pass
finally:
    ser.close()

# After data collection duration, count peaks and print results
peaks_fsr1 = count_peaks(pressures1, timestamps1, peak_times_fsr1)
peaks_fsr2 = count_peaks(pressures2, timestamps2, peak_times_fsr2)

print(f"Number of peaks in FSR1: {peaks_fsr1}")
print(f"Number of peaks in FSR2: {peaks_fsr2}")

# Calculate time differences between peaks
def calculate_peak_time_diffs(peak_times_list):
    time_diffs = []
    for i in range(len(peak_times_list) - 1):
        time_diff = peak_times_list[i + 1] - peak_times_list[i]
        time_diffs.append(time_diff)
    return time_diffs

# Print time differences between peaks for FSR1
time_diffs_fsr1 = calculate_peak_time_diffs(peak_times_fsr1)
print("Time differences between peaks for FSR1 (seconds):")
print(time_diffs_fsr1)

# Print time differences between peaks for FSR2
time_diffs_fsr2 = calculate_peak_time_diffs(peak_times_fsr2)
print("Time differences between peaks for FSR2 (seconds):")
print(time_diffs_fsr2)

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
