#include <WiFi.h>

// Replace with your network credentials
const char* ssid = "hackhubafrica";
const char* password = "hackhubafrica";

const int ledPin = 2; // Built-in LED on many ESP32 boards
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);

  Serial.println("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available(); // listen for incoming clients
  if (client) {
    String req = client.readStringUntil('\r');
    client.flush();

    // Simple LED control via web
    if (req.indexOf("/ON") != -1) {
      digitalWrite(ledPin, HIGH);
    } else if (req.indexOf("/OFF") != -1) {
      digitalWrite(ledPin, LOW);
    }

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html\n");
    client.println("<!DOCTYPE html><html><body>");
    client.println("<h1>ESP32 Web Server</h1>");
    client.println("<p><a href=\"/ON\">Turn ON</a></p>");
    client.println("<p><a href=\"/OFF\">Turn OFF</a></p>");
    client.println("</body></html>");
    client.stop();
  }
}
