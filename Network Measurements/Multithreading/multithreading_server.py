import asyncio
import websockets
import threading

clients = set()

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

async def start_server():
    # Start the WebSocket server on all interfaces, port 8765
    server = await websockets.serve(relay_video, "0.0.0.0", 8765)
    print("Server is running on port 8765")
    await server.wait_closed()

def run_server():
    asyncio.run(start_server())

if __name__ == "__main__":
    # Start the WebSocket server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    try:
        # Here, you can perform other tasks in the main thread if needed
        while True:
            # This loop keeps the main thread running
            # You can add any other tasks or logic here
            pass
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        # Clean up if needed (not strictly necessary with websockets)
        server_thread.join()  # Ensure the server thread has finished
