import paho.mqtt.client as mqtt

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to HiveMQ Broker successfully!")
        # Subscribe to a topic after connecting
        client.subscribe("your/topic/here")  # You can update the topic as needed
    else:
        print(f"Failed to connect, return code {rc}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"{msg.payload.decode()}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# HiveMQ broker IP and port
broker_ip = "broker.hivemq.com"  # Public HiveMQ broker
port = 1883  # Default MQTT port

# Connect to the HiveMQ broker
client.connect(broker_ip, port, 60)

# Start the MQTT client loop to handle network traffic and callbacks
client.loop_start()

# Keep the program running and listen for messages
try:
    while True:
        pass  # You can add other functionality here if needed
except KeyboardInterrupt:
    print("Disconnecting...")
    client.loop_stop()  # Stop the loop
    client.disconnect()  # Disconnect from the broker

