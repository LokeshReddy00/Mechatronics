import serial

try:
    # Configure the serial port
    ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the port your Arduino is connected to

    while True:
        # Read a line from the serial port
        data = ser.readline().decode().strip()
        print(data)  # Print the data to the terminal

except serial.SerialException as e:
    print("Serial port error:", e)

except KeyboardInterrupt:
    # Close the serial connection when Ctrl+C is pressed
    ser.close()
