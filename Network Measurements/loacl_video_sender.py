import asyncio
import websockets
import cv2
import base64

video_path = r'C:\Users\Pasindu\Downloads\video1.mp4'

async def upload_video():

    serverIp = "13.60.222.225"
    port = "8765"
    uri = f"ws://{serverIp }:{port}"

    try:
        #connect to the server
        async with websockets.connect(uri) as websocket:
            print("Connected to the server succesfully ")

            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened:
                print(f"Error:Unable to open the video at {video_path}")
            
            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    print("End of the video stream or error in reading the frame")
                    break

                #show the current frame in window

                cv2.imshow("Transmitting Video",frame)

                # Break if 'q' key is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Video transmission stopped by user.")
                    break

                #encode frame to JPEG and base64
                _,buffer = cv2.imencode('.jpg',frame)
                if buffer is None:
                    print("fail to encode the image")
                    continue

                base64_frame = base64.b64encode(buffer).decode('utf-8')

                try:
                    #send the base64_encoded frame to the server
                    await websocket.send(base64_frame)
                    
                except websocket.extensions.ConnectionClosed:
                    break

                await asyncio.sleep(1/120) #delay to simulate video frame rate

    finally:
            cap.release() # When done capturing frames, release it to free the resource.
            cv2.destroyAllWindows() #close the video window

if __name__ == "__main__":
    asyncio.run(upload_video())

                

                








            


        

