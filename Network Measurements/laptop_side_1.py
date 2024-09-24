import asyncio
import websockets
import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import keyboard

broker = 'broker.hivemq.com'
port = 1883
topic = "your/topic/here"

client = mqtt.Client()

async def publish_message(key):
    client.publish(topic, key)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")

async def handle_keypresses():
    print("Press any key to send it via MQTT. Press 'Esc' to quit.")

    def set_key(event):
        asyncio.run_coroutine_threadsafe(publish_message(event.name), loop)

    keyboard.on_press(set_key)
    keyboard.wait('esc')
    keyboard.unhook_all()

async def receive_video():
    uri = "ws://13.60.222.225:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server.")
            while True:
                base64_frame = await websocket.recv()
                print("Frame received from server.")

                frame_data = base64.b64decode(base64_frame)
                np_arr = np.frombuffer(frame_data, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is not None:
                    cv2.imshow('Received Video', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("Video reception stopped by user.")
                        break
                else:
                    print("Error: Frame decoding failed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cv2.destroyAllWindows()

async def mqtt_loop():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, 60)

    while True:
        client.loop(timeout=1.0)
        await asyncio.sleep(0.01)

async def main():
    global loop
    loop = asyncio.get_event_loop()
    mqtt_task = asyncio.create_task(mqtt_loop())
    keypress_task = asyncio.create_task(handle_keypresses())
    video_task = asyncio.create_task(receive_video())

    await asyncio.gather(mqtt_task, keypress_task, video_task)

if __name__ == "__main__":
    asyncio.run(main())
