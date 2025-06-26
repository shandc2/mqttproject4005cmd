import time, random
import paho.mqtt.client as mqtt

# constants
temp_max = 40.0
temp_min = 10.0

client = mqtt.Client(client_id="tempsensor")
client.connect("localhost", 1883)

temp = round(random.uniform(temp_min, temp_max), 2)

while True:
    temp_change = random.uniform(-2.0, 2.0)
    temp = temp+temp_change
    temp = max(temp_min, min(temp_max, temp))
    temp = round(temp, 2)
    client.publish("home/temp", temp)
    print(f"[tempsensor] Sent: {temp}°C")
    time.sleep(5)
