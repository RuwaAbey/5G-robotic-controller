import asyncio
import websockets
import threading
import paho.mqtt.client as mqtt
import keyboard  # For key press event handling

clients = set()
broker = 'broker.hivemq.com'
mqtt_port = 1883
topic = "test/command/laptop"

# MQTT Client Setup
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()}")

def mqtt_publish(key):
    """Publish MQTT message when a key is pressed."""
    mqtt_client.publish(topic, key)
    print(f"Published key press '{key}' to MQTT.")

def mqtt_loop():
    """Run MQTT client loop."""
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(broker, mqtt_port, 60)
    mqtt_client.loop_forever()

async def relay_video(websocket, path):
    print("New client connected.")
    clients.add(websocket)
    try:
        async for message in websocket:
            print("Received message from client.")
            # Broadcast the message (video frame) to all clients except the sender
            for client in clients:
                if client != websocket:
                    try:
                        await client.send(message)
                        print("Frame sent to another client.")
                    except Exception as e:
                        print(f"Error sending frame to client: {e}")
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Client disconnected.")
        clients.remove(websocket)

def start_server():
    asyncio.run(main())

async def main():
    # Start the WebSocket server on all interfaces, port 8765
    server = await websockets.serve(relay_video, "0.0.0.0", 8765)
    print("Server is running on port 8765")
    await server.wait_closed()

def handle_keypress():
    """Listen for key presses and publish them via MQTT."""
    keyboard.on_press(lambda event: mqtt_publish(event.name))
    keyboard.wait()  # Keeps the thread alive to listen for keypresses

if __name__ == "__main__":
    try:
        # Start the WebSocket server in a separate thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        # Start the MQTT loop in a separate thread
        mqtt_thread = threading.Thread(target=mqtt_loop)
        mqtt_thread.start()

        # Start listening for keyboard presses in a separate thread
        keypress_thread = threading.Thread(target=handle_keypress)
        keypress_thread.start()

        # Keep the main thread alive
        server_thread.join()
        mqtt_thread.join()
        keypress_thread.join()

    except Exception as e:
        print(f"Server encountered an error: {e}")
