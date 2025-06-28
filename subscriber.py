import paho.mqtt.client as mqtt
from datetime import datetime

def get_timestamp():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return timestamp

def on_connect(client, userdata, flags, rc):
    print("Connected at " + (get_timestamp()) + " with result code " + str(rc))
    client.subscribe("#")  # Subscribe to all topics

def on_message(client, userdata, msg):
    print(f"[{get_timestamp()}][{msg.topic}] {msg.payload.decode()}")

client = mqtt.Client(client_id="monitor")
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883)
client.loop_forever()
