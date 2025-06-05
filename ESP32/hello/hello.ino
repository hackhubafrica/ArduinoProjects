#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  delay(2000); // Wait a bit for Serial Monitor to open
}

void loop() {
  Serial.println("Hello from ESP32!");
  delay(1000);
}
