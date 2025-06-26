import paho.mqtt.client as mqtt

# constants
target_temp = 18

# variables
latest_temp = 0.0
motion_detected = False
heater_state = "OFF"

def heater_control(client1):
    if latest_temp < target_temp and motion_detected:
        heater_state = "ON"
        print(f"[HEATER] Temp: {latest_temp}°C, Motion: {motion_detected} — HEATER ON")
    else:
        heater_state = "OFF"
        print(f"[HEATER] Temp: {latest_temp}°C, Motion: {motion_detected} — HEATER OFF")
    client1.publish("home/heater", heater_state)

def on_message(client, userdata, message):
    global latest_temp, motion_detected

    topic = message.topic
    payload = message.payload.decode()

    if topic == "home/temp":
        latest_temp = float(payload)
    elif topic == "home/motion":
        motion_detected = payload.strip().lower() == "true"

    heater_control(client)

client = mqtt.Client(client_id="heatercontroller")
client.connect("localhost", 1883)
client.subscribe("home/temp")
client.subscribe("home/motion")
client.on_message = on_message

client.loop_forever()