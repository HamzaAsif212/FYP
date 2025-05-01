import serial
import csv
import time

# Configure the serial connection (update 'COM8' to match your Arduino's port)
SERIAL_PORT = 'COM8'  # Replace with your Arduino's serial port (e.g., '/dev/ttyUSB0' on Linux/Mac)
BAUD_RATE = 9600

# Open the serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

# Create or open the CSV file
CSV_FILE = 'mean_moisture_data.csv'
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Mean_Moisture_Percent'])

    print("Reading data from Arduino for 10 seconds and computing the mean...")
    try:
        while True:
            # Collect data for 10 seconds
            start_time = time.time()  # Record the start time
            moisture_values = []  # List to store moisture percentage values

            while time.time() - start_time < 10:  # Run for 10 seconds
                # Read a line from the serial monitor
                line = ser.readline().decode('utf-8').strip()

                # Check if the line contains valid numeric data
                if line.isdigit():  # Ensure the data is numeric
                    moisture_percent = int(line)  # Convert to integer
                    moisture_values.append(moisture_percent)  # Add to the list
                    print(f"Received Moisture Percentage: {moisture_percent}%")

                time.sleep(0.1)  # Small delay to avoid overloading the CPU

            # Compute the mean of the collected values
            if moisture_values:
                mean_moisture = sum(moisture_values) / len(moisture_values)
                print(f"Mean Moisture Percentage over 10 seconds: {mean_moisture:.2f}%")

                # Write the mean value to the CSV file
                writer.writerow([mean_moisture])
                file.flush()  # Ensure data is written immediately
            else:
                print("No valid data received in the last 10 seconds.")

    except KeyboardInterrupt:
        print("\nExiting program. CSV file saved.")
    finally:
        ser.close()  # Close the serial connection