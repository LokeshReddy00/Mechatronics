import serial
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.signal import find_peaks
import time

# Open the serial port
ser = serial.Serial('COM3', 9600)
ser.flushInput()

timestamps_fsr1 = []
pressures_fsr1 = []

timestamps_fsr2 = []
pressures_fsr2 = []

peak_durations_fsr1 = []  # Array to store peak durations for FSR1
peak_differences_fsr1 = []  # Array to store peak time differences for FSR1

peak_durations_fsr2 = []  # Array to store peak durations for FSR2
peak_differences_fsr2 = []  # Array to store peak time differences for FSR2

try:
    # User input for duration of data collection
    duration_minutes = int(input("Enter the duration of data collection (minutes): "))
    
    # Calculate end time for data collection
    end_time = time.time() + duration_minutes * 60
    
    # Data collection loop
    while time.time() < end_time:
        line = ser.readline().decode().strip()
        
        if line.startswith('FSR1'):
            data_str = line[len('FSR1 '):]
            time_str, pressure_str = data_str.split(', ')
            timestamp = datetime.now()
            pressure = float(pressure_str.rstrip(')'))
            timestamps_fsr1.append(timestamp)
            pressures_fsr1.append(pressure)
        
        elif line.startswith('FSR2'):
            data_str = line[len('FSR2 '):]
            time_str, pressure_str = data_str.split(', ')
            timestamp = datetime.now()
            pressure = float(pressure_str.rstrip(')'))
            timestamps_fsr2.append(timestamp)
            pressures_fsr2.append(pressure)
    
    # Close the serial port
    ser.close()
    
    # Plotting after data collection
    plt.figure(figsize=(12, 8))
    
    if timestamps_fsr1 and pressures_fsr1:
        plt.subplot(2, 1, 1)
        plt.plot(timestamps_fsr1, pressures_fsr1, 'b-')
        plt.xlabel('Time')
        plt.ylabel('Pressure FSR1')
        plt.title('FSR1 Live Pressure vs Time Graph')
        plt.grid(True)
    
    if timestamps_fsr2 and pressures_fsr2:
        plt.subplot(2, 1, 2)
        plt.plot(timestamps_fsr2, pressures_fsr2, 'r-')
        plt.xlabel('Time')
        plt.ylabel('Pressure FSR2')
        plt.title('FSR2 Live Pressure vs Time Graph')
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()

    def count_peaks(pressures, timestamps):
        peaks, _ = find_peaks(pressures, prominence=50)  
        peak_start_times = []
        peak_end_times = []
        peak_durations = []
        peak_time_differences = []

        for i in range(len(peaks)):
            if i < len(peaks) - 1:
                start_index = peaks[i]
                end_index = peaks[i + 1]
            else:
                start_index = peaks[i]
                end_index = len(pressures) - 1
            
            peak_start_time = timestamps[start_index]
            peak_end_time = timestamps[end_index]
            peak_duration = (peak_end_time - peak_start_time).total_seconds()
            peak_time_difference = (peak_end_time - peak_start_time).total_seconds()
            
            peak_start_times.append(peak_start_time)
            peak_end_times.append(peak_end_time)
            peak_durations.append(peak_duration)
            peak_time_differences.append(peak_time_difference)
        
        return len(peaks), peak_start_times, peak_end_times, peak_durations, peak_time_differences
    
    # Calculate peaks, peak start times, peak end times, peak durations, and peak time differences for FSR1
    peaks_fsr1, peak_start_times_fsr1, peak_end_times_fsr1, peak_durations_fsr1, peak_differences_fsr1 = count_peaks(pressures_fsr1, timestamps_fsr1)
    
    # Calculate peaks, peak start times, peak end times, peak durations, and peak time differences for FSR2
    peaks_fsr2, peak_start_times_fsr2, peak_end_times_fsr2, peak_durations_fsr2, peak_differences_fsr2 = count_peaks(pressures_fsr2, timestamps_fsr2)

    print(f"Number of peaks in FSR1: {peaks_fsr1}")
    print(f"Number of peaks in FSR2: {peaks_fsr2}")

    print("Peak start times for FSR1:")
    print(peak_start_times_fsr1)
    print("Peak end times for FSR1:")
    print(peak_end_times_fsr1)
    print("Peak durations for FSR1 (seconds):")
    print(peak_durations_fsr1)
    print("Peak time differences for FSR1 (seconds):")
    print(peak_differences_fsr1)

    print("Peak start times for FSR2:")
    print(peak_start_times_fsr2)
    print("Peak end times for FSR2:")
    print(peak_end_times_fsr2)
    print("Peak durations for FSR2 (seconds):")
    print(peak_durations_fsr2)
    print("Peak time differences for FSR2 (seconds):")
    print(peak_differences_fsr2)

    # Save data to Excel if data exists
    if timestamps_fsr1 and pressures_fsr1:
        data_fsr1 = {'Timestamp_FSR1': timestamps_fsr1,
                     'Pressure_FSR1': pressures_fsr1,
                     'Peak_Start_Times_FSR1': peak_start_times_fsr1,
                     'Peak_End_Times_FSR1': peak_end_times_fsr1,
                     'Peak_Durations_FSR1': peak_durations_fsr1,
                     'Peak_Time_Differences_FSR1': peak_differences_fsr1}
        df_fsr1 = pd.DataFrame(data_fsr1)
        df_fsr1.to_excel('data_fsr1.xlsx', index=False)

    if timestamps_fsr2 and pressures_fsr2:
        data_fsr2 = {'Timestamp_FSR2': timestamps_fsr2,
                     'Pressure_FSR2': pressures_fsr2,
                     'Peak_Start_Times_FSR2': peak_start_times_fsr2,
                     'Peak_End_Times_FSR2': peak_end_times_fsr2,
                     'Peak_Durations_FSR2': peak_durations_fsr2,
                     'Peak_Time_Differences_FSR2': peak_differences_fsr2}
        df_fsr2 = pd.DataFrame(data_fsr2)
        df_fsr2.to_excel('data_fsr2.xlsx', index=False)

except KeyboardInterrupt:
    print("Data collection interrupted by user.")
finally:
    # Close the serial port in case of any error
    ser.close()
