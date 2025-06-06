import network
import socket
import time

# 1. Connect to Wi-Fi
ssid = 'hackhubafrica'         # 🔁 Change this
password = 'hackhubafrica' # 🔁 Change this

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(0.5)

print('Connected! Network config:', wlan.ifconfig())

ip = wlan.ifconfig()[0]  # Get ESP32 IP address
print("Access your ESP32 at: http://{}".format(ip))

# 2. Start Web Server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print("Listening on http://{}".format(ip))

while True:
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break

        response = """\
HTTP/1.1 200 OK

<html>
  <head><title>ESP32 Web Server</title></head>
  <body>
    <h1>Hello from ESP32!</h1>
    <p>IP Address: {}</p>
  </body>
</html>
""".format(ip)

        cl.send(response)
        cl.close()

    except Exception as e:
        print('Error:', e)
        cl.close()
