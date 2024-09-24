import asyncio
import websockets
import cv2
import base64
import numpy as np
import gmqtt
import keyboard
import threading
import time

broker = 'broker.hivemq.com'
port = 1883 
topic = "test/command/laptop"

# Timing start
start_time = time.time()

# MQTT client setup using gmqtt
class MqttClient(gmqtt.Client):
    async def on_connect(self, client, flags, rc, properties):
        print("Connected to MQTT broker.")

    async def on_message(self, client, topic, payload, qos, properties):
        print(f"Received message on {topic}: {payload.decode()}")

# Function to publish MQTT message
async def publish_message(key):
    message = key
    await client.publish(topic, message)

# Function to handle keypresses and publish MQTT messages
def handle_keypresses():
    key = None
    def set_key(event):
        nonlocal key
        key = event.name
        asyncio.run_coroutine_threadsafe(publish_message(key), loop)

    # Register the key press event
    keyboard.on_press(set_key)

    print("Press any key to send it via MQTT. Press 'Esc' to quit.")
    keyboard.wait('esc')

# Asynchronous function to receive video from WebSocket
async def receive_video():
    uri = "ws://13.60.222.225:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server.")

            while True:
                # Receive a message (base64-encoded frame) from the server
                base64_frame = await websocket.recv()

                # Decode the base64-encoded frame
                frame_data = base64.b64decode(base64_frame)
                # Convert the byte data to a NumPy array and then to an OpenCV image
                np_arr = np.frombuffer(frame_data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is not None:
                    # Display the received frame
                    cv2.imshow('Received Video', frame)

                    # Break if 'q' key is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("Video reception stopped by user.")
                        break
                else:
                    print("Error: Frame decoding failed.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cv2.destroyAllWindows()  # Close the video window

# Function to start the MQTT client loop asynchronously
async def start_mqtt():
    await client.connect(broker, port)
    await client.subscribe(topic)

if __name__ == "__main__":
    client = MqttClient("mqtt_client")
    loop = asyncio.get_event_loop()

    # Start MQTT in a separate thread
    mqtt_thread = threading.Thread(target=lambda: loop.run_until_complete(start_mqtt()))
    mqtt_thread.start()

    # Start keypress handling in a separate thread
    keypress_thread = threading.Thread(target=handle_keypresses)
    keypress_thread.start()

    try:
        asyncio.run(receive_video())
    except KeyboardInterrupt:
        print("Program interrupted")

    finally:
        client.disconnect()
        keyboard.unhook_all()
        print(f"Total execution time: {time.time() - start_time:.2f} seconds")
