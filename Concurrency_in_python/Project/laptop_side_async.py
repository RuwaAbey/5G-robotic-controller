
import asyncio
import websockets
import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import keyboard

broker = 'broker.hivemq.com'
port = 1883 
topic = "test/command/laptop"

# MQTT client setup
client = mqtt.Client()

# Function to publish MQTT message
def publish_message(key):
    message = key
    client.publish(topic, message)

# Asynchronous function to handle keypresses and publish MQTT messages
async def handle_keypresses():
    key = None
    def set_key(event):
        nonlocal key
        key = event.name
        publish_message(key)

    # Register the key press event
    keyboard.on_press(set_key)

    print("Press any key to send it via MQTT. Press 'Esc' to quit.")
    while not keyboard.is_pressed('esc'):
        await asyncio.sleep(0.1)  # Non-blocking sleep to prevent excessive CPU usage

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
        cv2.destroyAllWindows()

async def main():
    # Start both the video receiving and keypress handling tasks concurrently
    video_task = asyncio.create_task(receive_video())
    keypress_task = asyncio.create_task(handle_keypresses())

    await asyncio.gather(video_task, keypress_task)

if __name__ == "__main__":
    # Connect to MQTT broker
    client.connect(broker, port, 60)
    
    # Run the asyncio main loop
    asyncio.run(main())
