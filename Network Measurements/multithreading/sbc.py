import asyncio
import websockets
import cv2
import base64
import paho.mqtt.client as mqtt
import threading

broker = 'broker.hivemq.com'
port = 1883
topic = "test/command/laptop"
video_path = r'C:\\Users\\Pasindu\\Downloads\\video1.mp4'

# Video streaming function via WebSocket
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
            print("Connected to the server successfully")
            
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

# MQTT event handlers
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, message):
    print(f"Message received: {message.payload.decode()}")

# MQTT loop function
def mqtt_loop():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.loop_forever()  # Blocking loop for MQTT

# Wrapper to run the asyncio task for video upload
def video_thread():
    asyncio.run(upload_video())

# Main function to run video streaming and MQTT handling concurrently
def main():
    # Create and start the video thread
    video_thread_instance = threading.Thread(target=video_thread)
    video_thread_instance.start()

    # Run the MQTT loop in the main thread
    mqtt_loop()

    # Join threads
    video_thread_instance.join()

if __name__ == "__main__":
    main()
