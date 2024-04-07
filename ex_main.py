import serial
import pandas as pd
from datetime import datetime

# Establish serial connection with Arduino
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the correct serial port
ser.flushInput()

# Initialize empty list to store data
data = []

try:
    while True:
        # Read data from serial port
        line = ser.readline().decode().strip()

        # Extract timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Append data to list
        data.append([timestamp, line])

        # Print data to console
        print(timestamp, line)

        # Save data to Excel file
        df = pd.DataFrame(data, columns=['Timestamp', 'Value'])
        df.to_excel('arduino_data.xlsx', index=False)

except KeyboardInterrupt:
    # Close serial connection
    ser.close()
