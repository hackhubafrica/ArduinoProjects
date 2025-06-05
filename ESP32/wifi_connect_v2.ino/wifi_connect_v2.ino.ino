#include <WiFi.h>

const char* ssid = "hackhubafrica";
const char* password = "hackhubafrica";

// Start web server on port 80
WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();  // Start the server
}

void loop() {
  WiFiClient client = server.available();  // Accept new client (still works)

  if (client) {
    Serial.println("New Client Connected");
    String request = client.readStringUntil('\r');
    Serial.print("Request: ");
    Serial.println(request);
    client.flush();

    // Send response
    client.println("HTTP/1.1 200 OK");
    client.println("Content-type:text/html");
    client.println();
    client.println("<h1>Hello from ESP32!</h1>");
    client.println();

    delay(1);
    client.stop();
    Serial.println("Client disconnected");
  }
}
