import random
import time
import paho.mqtt.client as mqtt

# Parameters for 'momentum based probability with decay'
# This is just to make the motion detection feel slightly more realistic
decay_rate = 0.05       # how quickly momentum fades per step
min_bias = 0.4          # minimum bias (equal chance)
initial_bias = 0.9      # bias after a value is picked
sleep_time = 5          # delay between picks

client = mqtt.Client(client_id="motionsensor")

client.connect("localhost", 1883)

# Starting state
# True = Motion Detected, False = No motion detected
current_value = random.choice([False, True])
bias = initial_bias
step = 0

client.publish("home/motion", current_value)

while True:
    # Probabilities
    if current_value:
        prob_1 = bias
        prob_0 = 1 - bias
    else:
        prob_0 = bias
        prob_1 = 1 - bias

    next_value = random.choices([False, True], weights=[prob_0, prob_1])[0]

    print(f"Step {step}: Picked {next_value} (bias={bias:.2f})")
    # print(f"[MotionSensor] Sent: {next_value})")

    # Check if value switched
    if next_value != current_value:
        current_value = next_value
        bias = initial_bias  # reset bias
        client.publish("home/motion", next_value) # changed to only publish when the state changes
        print("Published")
    else:
        bias = max(min_bias, bias - decay_rate)  # decay toward 50/50
        print("No change (Not published)")

    step += 1
    time.sleep(sleep_time)
