import asyncio
import websockets

clients = set()

async def relay_video(websocket, path):
    print("New client connected.")
    clients.add(websocket)

    try:
        async for message in websocket:
            print("Received message from client.")
            # Broadcast the message to all clients except the sender
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

async def main():
    server = await websockets.serve(relay_video, "0.0.0.0", 8765)
    print("Server is running on port 8765")
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Server encountered an error: {e}")
