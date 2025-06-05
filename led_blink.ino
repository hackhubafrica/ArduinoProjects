// Define LED pin (on most ESP32 boards, it's GPIO 2)
const int ledPin = 2;

void setup() {
  pinMode(ledPin, OUTPUT); // Set the LED pin as output
}

void loop() {
  digitalWrite(ledPin, HIGH);  // Turn the LED on
  delay(3000);                 // Wait for 3 seconds
  digitalWrite(ledPin, LOW);   // Turn the LED off
  delay(3000);                 // Wait for 3 seconds
}
