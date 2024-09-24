import multiprocessing
import subprocess

# Function to run the MQTT publish script
def run_mqtt_publish():
    subprocess.run(['python', r'C:\Users\Pasindu\OneDrive\Desktop\websocket\Robot Application\SBC_Side\subscribe_mqtt.py'])
    #C:\Users\Pasindu\OneDrive\Desktop\websocket\Robot Application\Laptop_Side

# Function to run the video receiver script
def run_receiver():
    subprocess.run(['python',r'C:\Users\Pasindu\OneDrive\Desktop\websocket\Robot Application\SBC_Side\loacl_video_sender.py'])

if __name__ == "__main__":
    # Create processes for each script
    mqtt_process = multiprocessing.Process(target=run_mqtt_publish)
    receiver_process = multiprocessing.Process(target=run_receiver)

    # Start both processes
    mqtt_process.start()
    receiver_process.start()

    # Wait for both processes to finish (optional)
    #mqtt_process.join()
    #receiver_process.join()

    print("Both scripts have completed execution.")
