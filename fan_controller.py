import paho.mqtt.client as mqtt

# constants
target_temp = 21

# variables
latest_temp = 0.0
motion_detected = False


def fan_control():
    if latest_temp > target_temp and motion_detected:
        print(f"[FAN] Temp: {latest_temp}°C, Motion: {motion_detected} — Fan ON")
    else:
        print(f"[FAN] Temp: {latest_temp}°C, Motion: {motion_detected} — Fan OFF")

def on_message(client, userdata, message):
    global latest_temp, motion_detected

    topic = message.topic
    payload = message.payload.decode()

    if topic == "home/temp":
        latest_temp = float(payload)
    elif topic == "home/motion":
        motion_detected = payload.strip().lower() == "true"

    fan_control()

client = mqtt.Client(client_id="fancontroller")
client.connect("localhost", 1883)
client.subscribe("home/temp")
client.subscribe("home/motion")
client.on_message = on_message

client.loop_forever()