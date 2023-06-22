from machine import Pin
import time
import ubinascii
from umqttsimple import MQTTClient
import machine
import secrets
import dht

## MQTT
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = secrets.mqtt.topic
topic_pub = secrets.mqtt.topic
mqtt_server = secrets.mqtt.host
mqtt_port = secrets.mqtt.port
mqtt_user = secrets.mqtt.user
mqtt_password = secrets.mqtt.password

# DHT
d = dht.DHT11(machine.Pin(2))
d.measure()

# Determine SSID
import network
sta = network.WLAN(network.STA_IF)
ip = sta.ifconfig()[0]
ssid = sta.config('essid')

# Determine Time
year,month,day,hour,minute,x, x,x = time.localtime()
startup = f"{day}.{month}.{year} {hour}:{minute}"
startTime = time.time()

# Setup MQTT
client = MQTTClient(client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_password,keepalive=60)
client.set_last_will(topic_pub, f'{{ "status":"offline"}} ', retain=False, qos=0)
client.connect()

def sendMessage(topic_pub, msg, qos=1):
    global client
    client.publish(topic_pub, msg, qos=1)

def callback(p):
    global d
    temp = d.temperature()
    humidity = d.humidity()
    if p.value() == 0:
        t = str(time.time() - startTime)
        sendMessage(topic_pub, f'{{ "status":"tick", "time": "{t}", "temp": "{temp}", "humidity": "{humidity}" }} ')
        print(f"tick {t}")

# Setup magnetic callback
magnet_pin = 4
p = Pin(magnet_pin, Pin.IN, Pin.PULL_UP)
p.irq(trigger=Pin.IRQ_FALLING, handler=callback)

sendMessage(topic_pub, f'{{ "status":"hello", "ssid": "{ssid}", "ip": "{ip}", "time": "{startup}" }} ')

while True:
    time.sleep(40)
    d.measure()
    client.ping()

