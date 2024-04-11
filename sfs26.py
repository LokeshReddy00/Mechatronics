import serial
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.signal import find_peaks
import time


ser = serial.Serial('COM3', 9600)  
ser.flushInput()

timestamps_fsr1 = []
pressures_fsr1 = []

timestamps_fsr2 = []
pressures_fsr2 = []

def update_plots():
    plt.clf()  
    
   
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
    plt.draw()

def count_peaks(pressures, timestamps):
    peaks, _ = find_peaks(pressures, prominence=0.1)  
    peak_timestamps = [timestamps[i] for i in peaks]
    return len(peaks), peak_timestamps

try:
   
    duration_minutes = int(input("Enter the duration of data collection (minutes): "))
    
    end_time = time.time() + duration_minutes * 60  # Calculate end time
    
    
    plt.ion()
    
    while time.time() < end_time:
       
        line = ser.readline().decode().strip()
        
       
        if line.startswith('FSR1'):
          
            data_str = line[len('FSR1 '):]  
            time_str, pressure_str = data_str.split(', ')
            timestamp = datetime.now()  
            pressure = float(pressure_str.rstrip(')'))  
            if pressure > 100:
                timestamps_fsr1.append(timestamp)
                pressures_fsr1.append(pressure)
            else:
               
                timestamps_fsr1.append(timestamp)
                pressures_fsr1.append(0)
           
            update_plots()

        elif line.startswith('FSR2'):
           
            data_str = line[len('FSR2 '):]  
            time_str, pressure_str = data_str.split(', ')
            timestamp = datetime.now()  
            pressure = float(pressure_str.rstrip(')'))  
            if pressure > 100:
                timestamps_fsr2.append(timestamp)
                pressures_fsr2.append(pressure)
            else:
               
                timestamps_fsr2.append(timestamp)
                pressures_fsr2.append(0)
          
            update_plots()

        plt.pause(0.05)  

except KeyboardInterrupt:
    print("Data collection interrupted by user.")

finally:
   
    ser.close()

   
    peaks_fsr1, peak_times_fsr1 = count_peaks(pressures_fsr1, timestamps_fsr1)
    peaks_fsr2, peak_times_fsr2 = count_peaks(pressures_fsr2, timestamps_fsr2)

    print(f"Number of peaks in FSR1: {peaks_fsr1}")
    print(f"Number of peaks in FSR2: {peaks_fsr2}")

   
    time_diffs_fsr1 = [(peak_times_fsr1[i + 1] - peak_times_fsr1[i]).total_seconds() for i in range(len(peak_times_fsr1) - 1)]
    print("Time differences between peaks for FSR1 (seconds):")
    print(time_diffs_fsr1)

   
    time_diffs_fsr2 = [(peak_times_fsr2[i + 1] - peak_times_fsr2[i]).total_seconds() for i in range(len(peak_times_fsr2) - 1)]
    print("Time differences between peaks for FSR2 (seconds):")
    print(time_diffs_fsr2)

   
    time_diffs_fsr1_fsr2 = []
    for i in range(min(len(peak_times_fsr1), len(peak_times_fsr2))):
        time_diff = (peak_times_fsr2[i] - peak_times_fsr1[i]).total_seconds()
        time_diffs_fsr1_fsr2.append(time_diff)
    print("Time differences between corresponding peaks of FSR1 and FSR2 (seconds):")
    print(time_diffs_fsr1_fsr2)

   
    if timestamps_fsr1 and pressures_fsr1:
        data_fsr1 = {'Timestamp_FSR1': timestamps_fsr1,
                     'Pressure_FSR1': pressures_fsr1}
        df_fsr1 = pd.DataFrame(data_fsr1)
        df_fsr1.to_excel('data_fsr1.xlsx', index=False)

  
    if timestamps_fsr2 and pressures_fsr2:
        data_fsr2 = {'Timestamp_FSR2': timestamps_fsr2,
                     'Pressure_FSR2': pressures_fsr2}
        df_fsr2 = pd.DataFrame(data_fsr2)
        df_fsr2.to_excel('data_fsr2.xlsx', index=False)

   
    update_plots()
    plt.ioff()
    plt.show()