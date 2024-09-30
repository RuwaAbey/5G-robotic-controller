import asyncio
import websockets
import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import threading

broker = 'broker.hivemq.com'
port = 1883
topic = "test/command/laptop"
video_path = r'C:\Users\ruwaa\Downloads\video3.mp4'

async def upload_video(uri):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open the video at {video_path}")
        return

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to the server successfully")

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    print("End of video stream or error in reading the frame")
                    break

                # Show the video being transmitted
                cv2.imshow("Transmitting Video", frame)

                # Check for 'q' key to stop the video transmission
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Video transmission stopped by user.")
                    break

                # Resize and compress frame for faster transmission
                frame = cv2.resize(frame, (640, 360))  # Resize to 640x360
                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])  # Compress JPEG
                if buffer is None:
                    print("Failed to encode the image")
                    continue

                base64_frame = base64.b64encode(buffer).decode('utf-8')

                try:
                    await websocket.send(base64_frame)
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed.")
                    break

                # Simulate 30 FPS transmission rate
                await asyncio.sleep(1/30)

    except Exception as e:
        print(f"Connection error: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()  # Close the OpenCV window

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")

def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, 60)
    client.loop_forever()

async def main():
    server_ip = "13.60.222.225"
    port = "8765"
    uri = f"ws://{server_ip}:{port}"

    # Start MQTT loop in a separate thread
    mqtt_thread = threading.Thread(target=mqtt_loop)
    mqtt_thread.start()

    # Start video upload
    await upload_video(uri)

if __name__ == "__main__":
    asyncio.run(main())
