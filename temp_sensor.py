import time, random
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="tempsensor")
client.connect("localhost", 1883)

temp = round(random.uniform(10.0, 40.0), 2)

while True:
    temp_change = random.uniform(-2.0, 2.0)
    temp = temp+temp_change
    temp = max(10.0, min(40.0, temp))
    temp = round(temp, 2)
    client.publish("home/temp", temp)
    print(f"[tempsensor] Sent: {temp}°C")
    time.sleep(5)
