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
CSV_FILE = 'mean_npk_data.csv'
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Mean_Nitrogen_N_mg/kg', 'Mean_Phosphorus_P_mg/kg', 'Mean_Potassium_K_mg/kg'])

    print("Reading data from Arduino for 10 seconds and computing the mean...")
    try:
        while True:
            # Collect data for 10 seconds
            start_time = time.time()  # Record the start time
            nitrogen_values = []  # List to store nitrogen values
            phosphorus_values = []  # List to store phosphorus values
            potassium_values = []  # List to store potassium values

            while time.time() - start_time < 10:  # Run for 10 seconds
                # Read a line from the serial monitor
                line = ser.readline().decode('utf-8').strip()

                # Split the CSV-like data into nitrogen, phosphorus, and potassium values
                if ',' in line:
                    try:
                        n, p, k = line.split(',')  # Split by comma
                        nitrogen = int(n)         # Convert nitrogen to integer
                        phosphorus = int(p)       # Convert phosphorus to integer
                        potassium = int(k)        # Convert potassium to integer
                        nitrogen_values.append(nitrogen)
                        phosphorus_values.append(phosphorus)
                        potassium_values.append(potassium)
                        print(f"Received: Nitrogen={nitrogen} mg/kg, Phosphorus={phosphorus} mg/kg, Potassium={potassium} mg/kg")
                    except ValueError:
                        print("Invalid data format received. Skipping...")

                time.sleep(0.1)  # Small delay to avoid overloading the CPU

            # Compute the mean of the collected values
            if nitrogen_values and phosphorus_values and potassium_values:
                mean_nitrogen = sum(nitrogen_values) / len(nitrogen_values)
                mean_phosphorus = sum(phosphorus_values) / len(phosphorus_values)
                mean_potassium = sum(potassium_values) / len(potassium_values)
                print(f"Mean Nitrogen over 10 seconds: {mean_nitrogen:.2f} mg/kg")
                print(f"Mean Phosphorus over 10 seconds: {mean_phosphorus:.2f} mg/kg")
                print(f"Mean Potassium over 10 seconds: {mean_potassium:.2f} mg/kg")

                # Write the mean values to the CSV file
                writer.writerow([mean_nitrogen, mean_phosphorus, mean_potassium])
                file.flush()  # Ensure data is written immediately
            else:
                print("No valid data received in the last 10 seconds.")

    except KeyboardInterrupt:
        print("\nExiting program. CSV file saved.")
    finally:
        ser.close()  # Close the serial connection