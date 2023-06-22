import time
import rainbow
import machine
import neopixel
import secrets
from umqttsimple import MQTTClient


from machine import Pin
import time
import ubinascii
from umqttsimple import MQTTClient


## MQTT
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = secrets.mqtt.topic
mqtt_server = secrets.mqtt.host
mqtt_port = secrets.mqtt.port
mqtt_user = secrets.mqtt.user
mqtt_password = secrets.mqtt.password

# Determine SSID
import network
sta = network.WLAN(network.STA_IF)
ssid = sta.config('essid')

# Setup Neopixel
pixelCount = 60
np = neopixel.NeoPixel(machine.Pin(12), pixelCount)

keepalive = 65535

gauge = 0

def setGauge():
    global gauge, np, pixelCount
    gauge = gauge + 1
    for i in range(gauge %(pixelCount-1)):
        np[i] = rainbow.colors[i]
        np.write()
        time.sleep(0.01)


def sub_cb(topic, msg):
    print((topic, msg))
    setGauge()

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub, mqtt_port, mqtt_user, mqtt_password,sub_cb
  client = MQTTClient(client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password,keepalive=keepalive)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

try:
  print("connecting to MQTT")
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
    client.check_msg()
    time.sleep(10)

setGauge()
