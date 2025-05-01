import csv
import time
import serial
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
CSV_FILE = 'mean_weather_data23.csv'
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Mean_Humidity_%', 'Mean_Temperature_C'])

    print("Reading data from Arduino for 10 seconds and computing the mean...")
    try:
        while True:
            # Collect data for 10 seconds
            start_time = time.time()  # Record the start time
            humidities = []  # List to store humidity values
            temperatures = []  # List to store temperature values

            while time.time() - start_time < 10:  # Run for 10 seconds
                # Read a line from the serial monitor
                line = ser.readline().decode('utf-8').strip()

                # Split the CSV-like data into humidity and temperature
                if ',' in line:
                    try:
                        h, t = line.split(',')  # Split by comma
                        humidity = float(h)    # Convert humidity to float
                        temperature = float(t)  # Convert temperature to float
                        humidities.append(humidity)
                        temperatures.append(temperature)
                        print(f"Received: Humidity={humidity}%, Temperature={temperature}°C")
                    except ValueError:
                        print("Invalid data format received. Skipping...")

                time.sleep(0.1)  # Small delay to avoid overloading the CPU

            # Compute the mean of the collected values
            if humidities and temperatures:
                mean_humidity = sum(humidities) / len(humidities)
                mean_temperature = sum(temperatures) / len(temperatures)
                print(f"Mean Humidity over 10 seconds: {mean_humidity:.2f}%")
                print(f"Mean Temperature over 10 seconds: {mean_temperature:.2f}°C")

                # Write the mean values to the CSV file
                writer.writerow([mean_humidity, mean_temperature])
                file.flush()  # Ensure data is written immediately
            else:
                print("No valid data received in the last 10 seconds.")

    except KeyboardInterrupt:
        print("\nExiting program. CSV file saved.")
    finally:
        ser.close()  # Close the serial connection