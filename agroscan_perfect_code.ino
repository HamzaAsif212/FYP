#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ESP32Servo.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

// Define pins and sensor types
#define DHTPIN 13         // Pin connected to the DHT22 data pin
#define DHTTYPE DHT22     // DHT22 sensor type
DHT dht(DHTPIN, DHTTYPE);

const int soilMoisturePin = 4;  // Soil moisture sensor pin
const int AirValue = 3790;      // Calibration value for dry soil
const int WaterValue = 1691;    // Calibration value for wet soil

const int raindropPin = 15;     // Raindrop sensor pin
Servo myServo;                  // Servo object
int servoPin = 18;              // Servo connected to PWM-capable GPIO pin

// OLED display setup
#define i2c_Address 0x3c        // I2C address for OLED
#define SCREEN_WIDTH 128        // OLED display width, in pixels
#define SCREEN_HEIGHT 64        // OLED display height, in pixels
#define OLED_RESET -1           // OLED reset pin (-1 if not used)

Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(9600);               // Start serial communication
  
  dht.begin();                      // Initialize DHT22 sensor
  myServo.attach(servoPin);         // Attach the servo to the pin
  
  delay(250);                       // Wait for the OLED to power up
  display.begin(i2c_Address, true); // Initialize OLED display with I2C address
  display.display();
  delay(1000);                      // Display Adafruit splash screen for 1 second

  display.clearDisplay();           // Clear the buffer to start fresh
}

void loop() {
  // Read soil moisture sensor
  int soilMoistureValue = analogRead(soilMoisturePin);
  int soilMoisturePercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);

  // Read raindrop sensor
  int raindropValue = analogRead(raindropPin);
  String rainStatus;

  if (raindropValue < 4095) {
    myServo.write(180);             // Move servo to 180 degrees
    rainStatus = "Raining";
  } else {
    myServo.write(0);               // Move servo to 0 degrees
    rainStatus = "No Rain";
  }

  // Read temperature and humidity from DHT22
  float temperature = dht.readTemperature();  // Temperature in Celsius
  float humidity = dht.readHumidity();        // Humidity in percentage

  // Check if the readings are valid
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Print all sensor values to the serial monitor
  Serial.print("Soil Moisture: ");
  Serial.print(soilMoisturePercent);
  Serial.println(" %");

  Serial.print("Rain Status: ");
  Serial.println(rainStatus);

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C\tHumidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  // Update OLED display with all sensor values
  display.clearDisplay();           // Clear the previous display
  display.setTextSize(1);           // Set text size for readability
  display.setTextColor(SH110X_WHITE); // Set text color

  display.setCursor(0, 0);          // Set cursor position (x, y)
  display.println("Soil Moisture: " + String(soilMoisturePercent) + "%");
  display.println("Rain Status: " + rainStatus);
  display.println("Temperature: " + String(temperature) + " C");
  display.println("Humidity: " + String(humidity) + " %");

  display.display();                // Show the updated content on the OLED

  delay(2000);                      // Delay for 2 seconds before the next reading
}
