import time
import random
import paho.mqtt.client as mqtt

# Constants
temp_max = 40.0
temp_min = 10.0

client = mqtt.Client(client_id="tempsensor")
client.connect("localhost", 1883)

# Start with a random temperature in range
temp = round(random.uniform(temp_min, temp_max), 2)

while True:
    # Generate a small temperature change
    temp_change = random.uniform(-2.0, 2.0)
    temp += temp_change

    # Bounce logic
    if temp < temp_min:
        excess = temp_min - temp
        temp = temp_min + excess  # bounce back upward
    elif temp > temp_max:
        excess = temp - temp_max
        temp = temp_max - excess  # bounce back downward

    # Round and send
    temp = round(temp, 2)
    client.publish("home/temp", temp)
    print(f"[tempsensor] Sent: {temp}°C")
    time.sleep(5)
