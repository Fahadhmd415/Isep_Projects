import neurokit2 as nk
import asyncio
import websockets
import json
from datetime import datetime
import pymongo
import paho.mqtt.client as mqtt
import numpy as np
from flask import Flask, jsonify
import time

# MongoDB connection
mongo_client = pymongo.MongoClient("mongodb+srv://raspberry1:87654321@cluster1.xor1vo8.mongodb.net/?retryWrites=true&w=majority")  # Update with your MongoDB connection string
mongo_db = mongo_client["cluster1"]  # Replace with your database name
ecg_collection = mongo_db["ecg_bpm_data"]  # Replace with your collection name

buffer = []
buffer_max_length = 500
ecg_value = 0.0  # Buffer to store ECG data received from MQTT
target_sampling_rate = 22 # Adjust as needed

def on_message(client, userdata, message):
    global ecg_value
    ecg_value = float(message.payload.decode())
  
    update_data(ecg_value)
    
def update_data(ecg_value):
    buffer.append(ecg_value)
    
    if len(buffer) == buffer_max_length:
        start_time = time.time()
        
        _, rpeaks = nk.ecg_peaks(buffer, sampling_rate=target_sampling_rate, method="pantompkins1985")
        r_peaks = rpeaks['ECG_R_Peaks']
        
        bpm = nk.ecg_rate(r_peaks, sampling_rate=target_sampling_rate)
        mean_bpm = np.mean(bpm)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(r_peaks)
        print(mean_bpm)
        print(f"Time required to process a 500 sample window: {processing_time} seconds")
        
        
        
        ecg_recording = {
            'time_stamps': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ecg': buffer,
            'r_peaks': r_peaks.tolist(),
        }

        bpm_recording = {
            'time_stamps': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'bpm': mean_bpm
        }

        # Save to MongoDB
        ecg_collection.insert_one(ecg_recording)
        ecg_collection.insert_one(bpm_recording)
        
        print("Processed ecg:", ecg_recording)
        print("Bpm:", bpm_recording)
        
        

        buffer.clear()

client = mqtt.Client("RaspberryPiClient")
client.on_message = on_message

mqtt_broker = "192.168.180.153"
mqtt_topic = "ecgData"

client.connect(mqtt_broker, 1883, 60)
client.subscribe(mqtt_topic)

print("MQTT Subscriber started...")
client.loop_start()
