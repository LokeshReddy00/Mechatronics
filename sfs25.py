import serial
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.signal import find_peaks
import time

# Establish serial connection with Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct serial port
ser.flushInput()

# Initialize lists to store data for FSR1 and FSR2
timestamps_fsr1 = []
pressures_fsr1 = []

timestamps_fsr2 = []
pressures_fsr2 = []

def update_plots():
    plt.clf()  # Clear previous plot
    
    # Pressure vs. time graph for FSR1
    if timestamps_fsr1 and pressures_fsr1:
        plt.subplot(2, 1, 1)
        plt.plot(timestamps_fsr1, pressures_fsr1, 'b-')
        plt.xlabel('Time')
        plt.ylabel('Pressure FSR1')
        plt.title('FSR1 Live Pressure vs Time Graph')
        plt.grid(True)

    # Pressure vs. time graph for FSR2
    if timestamps_fsr2 and pressures_fsr2:
        plt.subplot(2, 1, 2)
        plt.plot(timestamps_fsr2, pressures_fsr2, 'r-')
        plt.xlabel('Time')
        plt.ylabel('Pressure FSR2')
        plt.title('FSR2 Live Pressure vs Time Graph')
        plt.grid(True)
    
    plt.tight_layout()

def count_peaks(pressures, timestamps):
    peaks, _ = find_peaks(pressures, prominence=0.1)  # Adjust prominence threshold as needed
    peak_timestamps = [timestamps[i] for i in peaks]
    return len(peaks), peak_timestamps

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
            data_str = line[len('FSR1 '):]  # Remove 'FSR1 ' at the beginning
            time_str, pressure_str = data_str.split(', ')
            timestamp = datetime.now()  # Use current time
            pressure = float(pressure_str.rstrip(')'))  # Convert to float, removing ')' if present
            if pressure > 100:
                timestamps_fsr1.append(timestamp)
                pressures_fsr1.append(pressure)
            else:
                # Treat pressures below 100 as 0
                timestamps_fsr1.append(timestamp)
                pressures_fsr1.append(0)
            # Update FSR1 plot
            update_plots()

        elif line.startswith('FSR2'):
            # Extract timestamp and pressure values from FSR2 line
            data_str = line[len('FSR2 '):]  # Remove 'FSR2 ' at the beginning
            time_str, pressure_str = data_str.split(', ')
            timestamp = datetime.now()  # Use current time
            pressure = float(pressure_str.rstrip(')'))  # Convert to float, removing ')' if present
            if pressure > 100:
                timestamps_fsr2.append(timestamp)
                pressures_fsr2.append(pressure)
            else:
                # Treat pressures below 100 as 0
                timestamps_fsr2.append(timestamp)
                pressures_fsr2.append(0)
            # Update FSR2 plot
            update_plots()

        plt.pause(0.05)  

except KeyboardInterrupt:
    print("Data collection interrupted by user.")

finally:
    # Close serial connection
    ser.close()

    # Count peaks for FSR1 and FSR2
    peaks_fsr1, peak_times_fsr1 = count_peaks(pressures_fsr1, timestamps_fsr1)
    peaks_fsr2, peak_times_fsr2 = count_peaks(pressures_fsr2, timestamps_fsr2)

    print(f"Number of peaks in FSR1: {peaks_fsr1}")
    print(f"Number of peaks in FSR2: {peaks_fsr2}")

    # Calculate time differences between peaks for FSR1
    time_diffs_fsr1 = [(peak_times_fsr1[i + 1] - peak_times_fsr1[i]).total_seconds() for i in range(len(peak_times_fsr1) - 1)]
    print("Time differences between peaks for FSR1 (seconds):")
    print(time_diffs_fsr1)

    # Calculate time differences between peaks for FSR2
    time_diffs_fsr2 = [(peak_times_fsr2[i + 1] - peak_times_fsr2[i]).total_seconds() for i in range(len(peak_times_fsr2) - 1)]
    print("Time differences between peaks for FSR2 (seconds):")
    print(time_diffs_fsr2)

    # Store data in an Excel sheet for FSR1
    if timestamps_fsr1 and pressures_fsr1:
        data_fsr1 = {'Timestamp_FSR1': timestamps_fsr1,
                     'Pressure_FSR1': pressures_fsr1}
        df_fsr1 = pd.DataFrame(data_fsr1)
        df_fsr1.to_excel('data_fsr1.xlsx', index=False)

    # Store data in an Excel sheet for FSR2
    if timestamps_fsr2 and pressures_fsr2:
        data_fsr2 = {'Timestamp_FSR2': timestamps_fsr2,
                     'Pressure_FSR2': pressures_fsr2}
        df_fsr2 = pd.DataFrame(data_fsr2)
        df_fsr2.to_excel('data_fsr2.xlsx', index=False)

    # Display the plots one last time
    update_plots()
    plt.show()
