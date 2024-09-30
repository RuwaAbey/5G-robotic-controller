import asyncio
import websockets
import threading

clients = set()

# Function to handle relaying video frames between clients
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

# WebSocket server setup in a separate thread
def start_websocket_server():
    asyncio.run(websocket_server())

# Function to start the WebSocket server
async def websocket_server():
    server = await websockets.serve(relay_video, "0.0.0.0", 8765)
    print("WebSocket server is running on port 8765")
    await server.wait_closed()

# Placeholder function for any additional tasks (like MQTT handling)
def additional_task():
    while True:
        # Simulate some background task here
        print("Running additional task...")
        asyncio.sleep(5)

# Main function to start multithreaded server
def main():
    # Create a thread for the WebSocket server
    websocket_thread = threading.Thread(target=start_websocket_server)
    websocket_thread.start()

    # Create and start any additional threads (e.g., MQTT server or other tasks)
    additional_thread = threading.Thread(target=additional_task)
    additional_thread.start()

    # Join threads (optional, if you want to wait for them to finish)
    websocket_thread.join()
    additional_thread.join()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Server encountered an error: {e}")
