from fastapi import FastAPI, WebSocket
from pymongo import MongoClient
import json

app = FastAPI()

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://raspberry1:87654321@cluster1.xor1vo8.mongodb.net/?retryWrites=true&w=majority")
db = client["cluster1"]
collection = db["ecg_bpm_data"]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        ecg_json = await websocket.receive_text()
        bpm_json = await websocket.receive_text()

        try:
            # Parse the received JSON strings for ECG and BPM
            ecg_data = json.loads(ecg_json)
            bpm_data = json.loads(bpm_json)

            # Insert ECG data into MongoDB
            collection.insert_one(ecg_data)

            # Insert BPM data into MongoDB
            collection.insert_one(bpm_data)

            print(f"Received and stored ECG data: {ecg_data}")
            print(f"Received and stored BPM data: {bpm_data}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

