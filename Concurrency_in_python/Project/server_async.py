
import asyncio
import paho.mqtt.client as mqtt
import cv2
import base64
import websockets
import numpy as np

broker = 'broker.hivemq.com'
port = 1883
topic = "test/command/laptop"
video_file = 'video.mp4'

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, message):
    print(f"{message.payload.decode()} ")

# Asynchronous MQTT loop
async def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)

    while True:
        client.loop(timeout=1.0)
        await asyncio.sleep(0.01)

# Asynchronous function to upload video frames
async def upload_video():
    uri = "ws://0.0.0.0:8765"
    cap = cv2.VideoCapture(video_file)

    try:
        async with websockets.connect(uri) as websocket:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Failed to read video frame or end of video.")
                    break

                # Encode the frame to JPEG
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                # Encode the bytes to base64
                base64_frame = base64.b64encode(frame_bytes).decode('utf-8')

                # Send the base64-encoded frame to the WebSocket server
                await websocket.send(base64_frame)
                await asyncio.sleep(0.03)  # Simulating frame rate

    except Exception as e:
        print(f"An error occurred during video upload: {e}")
    finally:
        cap.release()

async def main():
    mqtt_task = asyncio.create_task(mqtt_loop())
    video_task = asyncio.create_task(upload_video())

    await asyncio.gather(mqtt_task, video_task)

if __name__ == "__main__":
    asyncio.run(main())
