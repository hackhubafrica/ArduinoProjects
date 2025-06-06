import network
import socket
import time
import dht
from machine import Pin, PWM

# === Wi-Fi Settings ===
ssid = 'YourSSID'
password = 'YourPassword'

# === Setup Pins ===
led = PWM(Pin(2), freq=1000)  # LED or relay
sensor = dht.DHT22(Pin(4))    # DHT22 sensor

# === Connect to Wi-Fi ===
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(0.5)

ip = wlan.ifconfig()[0]
print('Connected on:', ip)

# === HTML Web Page Template ===
def webpage(temp="--", hum="--", brightness=512):
    return """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 IoT Dashboard</title>
</head>
<body>
    <h2>ESP32 IoT Control</h2>
    <p>Temperature: {} °C</p>
    <p>Humidity: {} %</p>
    <form action="/led" method="get">
        <button name="state" value="on">LED ON</button>
        <button name="state" value="off">LED OFF</button>
    </form>
    <form action="/slider" method="get">
        <input type="range" name="val" min="0" max="1023" value="{}">
        <input type="submit" value="Set Brightness">
    </form>
</body>
</html>""".format(temp, hum, brightness)

# === Web Server ===
s = socket.socket()
s.bind(('0.0.0.0', 80))
s.listen(1)
print("Web server running at http://{}".format(ip))

brightness = 512  # Default PWM value
led.duty(brightness)

while True:
    cl, addr = s.accept()
    print("Client from", addr)
    request = cl.recv(1024).decode()

    # === Sensor Reading ===
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
    except:
        temp = hum = "--"

    # === Handle LED Button ===
    if "/led?state=on" in request:
        led.duty(1023)
    elif "/led?state=off" in request:
        led.duty(0)

    # === Handle Slider ===
    if "/slider?val=" in request:
        try:
            val_str = request.split("val=")[1].split(" ")[0]
            brightness = int(val_str)
            led.duty(brightness)
        except:
            pass

    response = webpage(temp, hum, brightness)
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
