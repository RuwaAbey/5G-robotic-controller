    
import asyncio
import websockets
import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import keyboard
import threading

broker = 'broker.hivemq.com'
port = 1883
topic = "test/command/laptop"

# MQTT client setup
client = mqtt.Client()

# Function to publish MQTT message
def publish_message(key):
    message = key
    client.publish(topic, message)

# Function to handle keypresses and publish MQTT messages
def handle_keypresses():
    key = None
    def set_key(event):
        nonlocal key
        key = event.name
        publish_message(key)

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

# Wrapper to run asyncio task for video streaming
def video_thread():
    asyncio.run(receive_video())

# Main function to run video streaming and keypress handling concurrently
def main():
    # Start MQTT connection
    client.connect(broker, port, 60)
    client.loop_start()  # Start MQTT client loop

    # Create and start the video thread
    video_thread_instance = threading.Thread(target=video_thread)
    video_thread_instance.start()

    # Run the MQTT keypress handler on the main thread
    handle_keypresses()

    # Join threads
    video_thread_instance.join()

if __name__ == "__main__":
    main()

    
