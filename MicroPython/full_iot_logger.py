import network, socket, time, os
import machine
import dht
import ujson as json
from machine import Pin, ADC, I2C
from bmp280 import BMP280

# === Sensor Setup ===
dht_sensor = dht.DHT22(Pin(4))
acs712 = ADC(Pin(36))
mq135 = ADC(Pin(39))
acs712.atten(ADC.ATTN_11DB)
mq135.atten(ADC.ATTN_11DB)

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bmp = BMP280(i2c)

# === Wi-Fi Connect ===
ssid = 'YourSSID'
password = 'YourPassword'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(0.5)

ip = wlan.ifconfig()[0]
print('Connected. Visit: http://{}'.format(ip))

# === CSV Log File ===
logfile = "log.csv"
if logfile not in os.listdir():
    with open(logfile, "w") as f:
        f.write("timestamp,temp_dht,hum_dht,voltage_acs,pressure_bmp,air_mq\n")

# === HTML Page ===
def webpage(data):
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
<p><a href="/log.csv">📥 Download CSV Log</a></p>
</body></html>
""".format(*data)

# === Read All Sensors ===
def read_all():
    try:
        dht_sensor.measure()
        t = dht_sensor.temperature()
        h = dht_sensor.humidity()
    except:
        t, h = "--", "--"
    v = acs712.read() * 3.3 / 4095
    p = bmp.pressure
    q = mq135.read()
    return (t, h, v, p, q)

# === Log to CSV ===
def log_data(data):
    ts = time.localtime()
    timestamp = "{:02}:{:02}:{:02}".format(ts[3], ts[4], ts[5])
    with open(logfile, "a") as f:
        f.write("{},{},{},{},{},{}\n".format(timestamp, *data))

# === Web Server ===
s = socket.socket()
s.bind(('0.0.0.0', 80))
s.listen(1)

print("Serving on http://{}".format(ip))

while True:
    cl, addr = s.accept()
    request = cl.recv(1024).decode()
    if "GET /log.csv" in request:
        with open(logfile, "r") as f:
            csv_data = f.read()
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/csv\r\n\r\n")
        cl.send(csv_data)
    else:
        data = read_all()
        log_data(data)
        page = webpage(data)
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(page)
    cl.close()
