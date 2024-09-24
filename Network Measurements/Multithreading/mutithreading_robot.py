import asyncio
import websockets
import cv2
import base64
import gmqtt
import threading
import time

broker = 'broker.hivemq.com'
port = 1883
topic = "test/command/laptop"
video_path = r'C:\Users\Pasindu\Downloads\video1.mp4'

# Timing start
start_time = time.time()

# MQTT client setup using gmqtt
class MqttClient(gmqtt.Client):
    async def on_connect(self, client, flags, rc, properties):
        print(f"Connected to MQTT broker with result code {rc}")
        await client.subscribe(topic)

    async def on_message(self, client, topic, payload, qos, properties):
        print(f"Received message on {topic}: {payload.decode()}")

# Function to upload video
async def upload_video():
    serverIp = "13.60.222.225"
    port = "8765"
    uri = f"ws://{serverIp}:{port}"

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open the video at {video_path}")
        return

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the WebSocket server successfully")
            
            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    print("End of the video stream or error in reading the frame")
                    break

                cv2.imshow("Transmitting Video", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Video transmission stopped by user.")
                    break

                _, buffer = cv2.imencode('.jpg', frame)
                if buffer is None:
                    print("Failed to encode the image")
                    continue

                base64_frame = base64.b64encode(buffer).decode('utf-8')

                try:
                    await websocket.send(base64_frame)
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed.")
                    break

                await asyncio.sleep(1/120)

    finally:
        cap.release()
        cv2.destroyAllWindows()

# Function to start the MQTT client loop
async def mqtt_loop():
    client = MqttClient("mqtt_client")
    client.on_connect = client.on_connect
    client.on_message = client.on_message

    await client.connect(broker, port)

    while True:
        await client.loop()

# Main async function to run tasks concurrently
async def main():
    mqtt_task = asyncio.create_task(mqtt_loop())
    video_task = asyncio.create_task(upload_video())

    await asyncio.gather(mqtt_task, video_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program interrupted")

    finally:
        # Timing end
        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds")
