import paho.mqtt.client as mqtt

# constants
target_temp = 21

# variables
latest_temp = 0.0
motion_detected = False
fan_state = "OFF"

def fan_control(client1):
    if latest_temp > target_temp and motion_detected:
        fan_state = "ON"

        print(f"[FAN] Temp: {latest_temp}°C, Motion: {motion_detected} — Fan ON")
    else:
        fan_state = "OFF"
        print(f"[FAN] Temp: {latest_temp}°C, Motion: {motion_detected} — Fan OFF")
    client1.publish("home/fan", fan_state)

def on_message(client, userdata, message):
    global latest_temp, motion_detected

    topic = message.topic
    payload = message.payload.decode()

    if topic == "home/temp":
        latest_temp = float(payload)
    elif topic == "home/motion":
        motion_detected = payload.strip().lower() == "true"

    fan_control(client)

client = mqtt.Client(client_id="fancontroller")
client.connect("localhost", 1883)
client.subscribe("home/temp")
client.subscribe("home/motion")
client.on_message = on_message

client.loop_forever()