import asyncio
import websockets
import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import threading
import keyboard

broker = 'broker.hivemq.com'
port = 1883
topic = "test/command/laptop"

# MQTT client setup
client = mqtt.Client()

def publish_message(key):
    message = key
    client.publish(topic, message)

def handle_keypresses():
    def set_key(event):
        publish_message(event.name)

    # Register the key press event
    keyboard.on_press(set_key)
    
    print("Press any key to send it via MQTT. Press 'Esc' to quit.")
    keyboard.wait('esc')
    
    keyboard.unhook_all()

async def receive_video(uri):
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket server.")

            while True:
                base64_frame = await websocket.recv()
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

def start_mqtt():
    client.connect(broker, port, 60)
    client.loop_start()

if __name__ == "__main__":
    # Start MQTT and keypress threads
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.start()

    keypress_thread = threading.Thread(target=handle_keypresses)
    keypress_thread.start()

    uri = "ws://13.60.222.225:8765"
    
    try:
        asyncio.run(receive_video(uri))
    except KeyboardInterrupt:
        print("Program interrupted")

    # Clean up
    client.loop_stop()
    client.disconnect()
    keyboard.unhook_all()
