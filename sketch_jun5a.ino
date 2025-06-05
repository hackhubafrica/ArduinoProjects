// Define LED pin (on most ESP32 boards, it's GPIO 2)
const int ledPin = 2;

void setup() {
  pinMode(ledPin, OUTPUT);      // Set the LED pin as output
  Serial.begin(115200);         // Start serial communication at 115200 baud rate
  Serial.println("Hello, World!"); // Print message to Serial Monitor
}

void loop() {
  digitalWrite(ledPin, HIGH);   // Turn the LED on
  Serial.println("LED is ON"); // Print status to Serial Monitor
  delay(3000);                  // Wait for 3 seconds

  digitalWrite(ledPin, LOW);    // Turn the LED off
  Serial.println("LED is OFF"); // Print status to Serial Monitor
  delay(3000);                  // Wait for 3 seconds
}
