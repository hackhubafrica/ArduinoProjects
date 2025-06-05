#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <BluetoothSerial.h>

BluetoothSerial SerialBT; // Classic Bluetooth

const char* ssid = "ESP32-NET";
const char* password = "12345678";

WebServer server(80);

String btMessages = "";

void handleRoot() {
  String page = "<!DOCTYPE html><html><head><meta charset='utf-8'>";
  page += "<title>ESP32 Wi-Fi + Bluetooth</title></head><body>";
  page += "<h2>🌐 Wi-Fi Dashboard</h2>";
  page += "<p><strong>Last Bluetooth Message:</strong><br>" + btMessages + "</p>";
  page += "<p>Send something from your Windows Bluetooth Terminal and see it here!</p>";
  page += "</body></html>";
  server.send(200, "text/html", page);
}

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32-BT"); // Visible Bluetooth name
  Serial.println("Bluetooth device started. Pair it from Windows!");

  WiFi.softAP(ssid, password);
  server.on("/", handleRoot);
  server.begin();
  Serial.println("Wi-Fi Access Point started. Connect to ESP32-NET and visit 192.168.4.1");
}

void loop() {
  server.handleClient();

  if (SerialBT.available()) {
    String incoming = SerialBT.readStringUntil('\n');
    btMessages = incoming;
    Serial.println("BT Received: " + incoming);
    SerialBT.println("Echo: " + incoming); // Optional echo
  }
}
