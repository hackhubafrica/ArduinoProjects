// Define LED pin (on most Arduino Uno boards, it's digital pin 13)
const int ledPin = 2;

void setup() {
  pinMode(ledPin, OUTPUT);       // Set the LED pin as output
  Serial.begin(9600);            // Start serial communication at 9600 baud rate
  Serial.println("Hello, World!"); // Print a welcome message
}

void loop() {
  digitalWrite(ledPin, HIGH);    // Turn the LED on
  Serial.println("LED is ON");   // Print status
  delay(3000);                   // Wait for 3 seconds

  digitalWrite(ledPin, LOW);     // Turn the LED off
  Serial.println("LED is OFF");  // Print status
  delay(3000);                   // Wait for 3 seconds
}
