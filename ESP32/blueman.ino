#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT_Device"); // You’ll see this name when scanning
  Serial.println("Bluetooth started! Pair your device.");
}

void loop() {
  if (SerialBT.available()) {
    char incoming = SerialBT.read();
    Serial.write(incoming); // echo to USB serial
  }

  if (Serial.available()) {
    char outgoing = Serial.read();
    SerialBT.write(outgoing); // send to Bluetooth client
  }
}
