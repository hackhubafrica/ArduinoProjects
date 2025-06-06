import esp
import os
import gc
import network

x = [
esp.flash_size(),
os.uname(),
gc.mem_free()]
print(x)

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('hackhubafrica', 'hackhubafrica')

while not sta.isconnected():
    pass

print("Connected, IP:", sta.ifconfig()[0])