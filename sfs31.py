import serial
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.signal import find_peaks
import time

def find_peak_cycles(pressures, timestamps):
    peaks, _ = find_peaks(pressures, prominence=50)
    peak_timestamps = [timestamps[i] for i in peaks]
    peak_durations = []
    peak_to_peak_intervals = []

    if len(peaks) > 0:
        for i in range(len(peaks) - 1):
            start_index = peaks[i]
            end_index = peaks[i + 1]

            # Find the rising edge (start) and falling edge (end) of the peak
            peak_start = start_index
            while peak_start > 0 and pressures[peak_start] > pressures[peak_start - 1]:
                peak_start -= 1

            peak_end = end_index
            while peak_end < len(pressures) - 1 and pressures[peak_end] > pressures[peak_end + 1]:
                peak_end += 1

            peak_start_time = timestamps[peak_start]
            peak_end_time = timestamps[peak_end]

            duration_seconds = (peak_end_time - peak_start_time).total_seconds()
            peak_durations.append(duration_seconds)

            # Calculate the peak-to-peak interval (time between end of one peak and start of next peak)
            peak_to_peak_interval_seconds = (timestamps[end_index] - timestamps[start_index]).total_seconds()
            peak_to_peak_intervals.append(peak_to_peak_interval_seconds)

    return peaks, peak_timestamps, peak_durations, peak_to_peak_intervals

try:
    ser = serial.Serial('COM3', 9600)
    ser.flushInput()

    timestamps_fsr1 = []
    pressures_fsr1 = []

    timestamps_fsr2 = []
    pressures_fsr2 = []

    duration_minutes = int(input("Enter the duration of data collection (minutes): "))
    end_time = time.time() + duration_minutes * 60

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

    ser.close()

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

    # Calculate peak cycles and durations for FSR1
    peaks_fsr1, peak_times_fsr1, peak_durations_fsr1, peak_to_peak_intervals_fsr1 = find_peak_cycles(pressures_fsr1, timestamps_fsr1)
    print(f"Number of peaks in FSR1: {len(peaks_fsr1)}")
    print("Peak durations for FSR1 (seconds):")
    print(peak_durations_fsr1)
    print("Peak-to-peak intervals for FSR1 (seconds):")
    print(peak_to_peak_intervals_fsr1)

    # Calculate peak cycles and durations for FSR2
    peaks_fsr2, peak_times_fsr2, peak_durations_fsr2, peak_to_peak_intervals_fsr2 = find_peak_cycles(pressures_fsr2, timestamps_fsr2)
    print(f"Number of peaks in FSR2: {len(peaks_fsr2)}")
    print("Peak durations for FSR2 (seconds):")
    print(peak_durations_fsr2)
    print("Peak-to-peak intervals for FSR2 (seconds):")
    print(peak_to_peak_intervals_fsr2)

    # Calculate time differences between corresponding peaks of FSR1 and FSR2
    time_diffs_fsr1_fsr2 = []
    for peak_time_fsr1 in peak_times_fsr1:
        closest_peak_time_fsr2 = min(peak_times_fsr2, key=lambda x: abs((x - peak_time_fsr1).total_seconds()))
        time_diff = (closest_peak_time_fsr2 - peak_time_fsr1).total_seconds()
        time_diffs_fsr1_fsr2.append(time_diff)

    print("Time differences between corresponding peaks of FSR1 and FSR2 (seconds):")
    print(time_diffs_fsr1_fsr2)

except KeyboardInterrupt:
    print("Data collection interrupted by user.")
finally:
    ser.close()
