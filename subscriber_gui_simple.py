import tkinter as tk
from datetime import datetime
import paho.mqtt.client as mqtt

class MQTTDashboard:
    def __init__(self, master):
        self.master = master
        master.title("MQTT Smart Environment Monitor")

        # 🌀 FAN STATUS
        self.fan_label = tk.Label(master, text="🌀 Fan Status:", font=("Arial", 14))
        self.fan_label.pack()
        self.fan_state = tk.Label(master, text="OFF", bg="red", fg="white", font=("Arial", 16), width=10)
        self.fan_state.pack(pady=5)

        # 🔥 HEATER STATUS
        self.heater_label = tk.Label(master, text="🔥 Heater Status:", font=("Arial", 14))
        self.heater_label.pack()
        self.heater_state = tk.Label(master, text="OFF", bg="red", fg="white", font=("Arial", 16), width=10)
        self.heater_state.pack(pady=5)

        # 🚶 MOTION STATUS
        self.motion_label = tk.Label(master, text="🚶 Motion Detected:", font=("Arial", 14))
        self.motion_label.pack()
        self.motion_state = tk.Label(master, text="NO", bg="red", fg="white", font=("Arial", 16), width=10)
        self.motion_state.pack(pady=5)

        # 🌡️ TEMPERATURE
        self.temp_label = tk.Label(master, text="🌡️ Temperature:", font=("Arial", 14))
        self.temp_label.pack()
        self.temp_value = tk.Label(master, text="-- °C", font=("Arial", 16))
        self.temp_value.pack(pady=5)

        # 📋 LOG AREA
        self.text_area = tk.Text(master, height=12, width=60)
        self.text_area.pack(padx=10, pady=10)
        self.scrollbar = tk.Scrollbar(master, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)

        # 🔌 MQTT Setup
        self.client = mqtt.Client(client_id="monitor_gui")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.connected_once = False
        self.client.connect("localhost", 1883)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if not self.connected_once:
            self.append_text(f"[INFO] Connected with result code {rc}\n")
            self.connected_once = True
        client.subscribe("home/#")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode().strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.append_text(f"[{timestamp}] [{topic}] {payload}\n")

        # Update temperature
        if topic == "home/temp":
            self.temp_value.config(text=f"{payload} °C")

        # Update fan state
        elif topic == "home/fan":
            if payload.upper() == "ON":
                self.fan_state.config(text="ON", bg="green")
            else:
                self.fan_state.config(text="OFF", bg="red")

        # Update heater state
        elif topic == "home/heater":
            if payload.upper() == "ON":
                self.heater_state.config(text="ON", bg="green")
            else:
                self.heater_state.config(text="OFF", bg="red")

        # Update motion status
        elif topic == "home/motion":
            if payload.lower() == "true":
                self.motion_state.config(text="YES", bg="green")
            else:
                self.motion_state.config(text="NO", bg="red")

    def append_text(self, text):
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

# 🚀 Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    dashboard = MQTTDashboard(root)
    root.mainloop()
