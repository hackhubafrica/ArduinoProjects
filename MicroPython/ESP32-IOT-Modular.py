# === sensor.py ===
import dht
from machine import Pin, ADC, I2C
from bmp280 import BMP280

# Sensor Pins
dht_sensor = dht.DHT22(Pin(4))
acs712 = ADC(Pin(36))
mq135 = ADC(Pin(39))
acs712.atten(ADC.ATTN_11DB)
mq135.atten(ADC.ATTN_11DB)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bmp = BMP280(i2c)

def read_sensors():
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
    except:
        temp, hum = "--", "--"

    voltage = acs712.read() * 3.3 / 4095
    pressure = bmp.pressure
    air_quality = mq135.read()
    return (temp, hum, voltage, pressure, air_quality)


# === logger.py ===
import time
import os

LOG_FILE = "log.csv"

def init_log():
    if LOG_FILE not in os.listdir():
        with open(LOG_FILE, "w") as f:
            f.write("timestamp,temp,humidity,voltage,pressure,air_quality\n")

def log(data):
    ts = time.localtime()
    timestamp = "{:02}:{:02}:{:02}".format(ts[3], ts[4], ts[5])
    with open(LOG_FILE, "a") as f:
        f.write("{},{},{},{},{},{}\n".format(timestamp, *data))

def read_log():
    with open(LOG_FILE, "r") as f:
        return f.read()


# === web.py ===
def generate_html(data):
    return """<!DOCTYPE html>
<html><head><title>ESP32 Sensor Dashboard</title></head>
<body>
<h2>Sensor Readings</h2>
<ul>
<li>Temperature (DHT22): {} °C</li>
<li>Humidity (DHT22): {} %</li>
<li>Current (ACS712): {:.2f} V</li>
<li>Pressure (BMP280): {} hPa</li>
<li>Air Quality (MQ135): {:.2f}</li>
</ul>
<p><a href=\"/log.csv\">📥 Download CSV Log</a></p>
</body></html>
""".format(*data)


# === main.py ===
import network, socket
from sensor import read_sensors
from logger import init_log, log, read_log
from web import generate_html

# Connect Wi-Fi
ssid = "YourSSID"
password = "YourPassword"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass

ip = wlan.ifconfig()[0]
print("ESP32 online at http://{}".format(ip))

init_log()

# Start web server
s = socket.socket()
s.bind(('0.0.0.0', 80))
s.listen(1)

while True:
    cl, addr = s.accept()
    request = cl.recv(1024).decode()

    if "GET /log.csv" in request:
        csv = read_log()
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/csv\r\n\r\n")
        cl.send(csv)
    else:
        data = read_sensors()
        log(data)
        page = generate_html(data)
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(page)
    cl.close()
