import asyncio
import websockets
import json
import numpy as np
import wfdb
import neurokit2 as nk
from datetime import datetime

# Load the ECG signal
sig, fields = wfdb.rdsamp('./I01')

# Set the desired sampling rate
target_sampling_rate = 1500

# Resample the ECG signal if the original sampling rate is different
ecg_signal = nk.signal_resample(sig[:, 0], sampling_rate=fields['fs'], desired_sampling_rate=target_sampling_rate, method="interpolation")

# Clean the ECG signal using NeuroKit2
ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate=target_sampling_rate, method='neurokit')

# Buffer for real-time processing
buffer = []
buffer_max_length = 5000

async def simulate_realtime_ecg_data(websocket):
    for ecg_data_mv in ecg_cleaned:
        await asyncio.sleep(1 / target_sampling_rate)
        buffer.append(ecg_data_mv)
        if len(buffer) == buffer_max_length:
            # R-peaks detection using NeuroKit2
            _, rpeaks = nk.ecg_peaks(buffer, sampling_rate=target_sampling_rate, method="neurokit")
            r_peaks = rpeaks['ECG_R_Peaks']
            
            # Calculate BPM using ecg_rate
            bpm = nk.ecg_rate(r_peaks, sampling_rate=target_sampling_rate)
            mean_bpm = np.mean(bpm)
            
            ecg_recording = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ecg': buffer,
                'r_peaks': r_peaks.tolist(),
            }

            bpm_recording = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'bpm': mean_bpm
            }

            # Convert the dictionaries to JSON strings and send them
            ecg_json = json.dumps(ecg_recording)
            bpm_json = json.dumps(bpm_recording)

            # WebSocket communication
            await websocket.send(ecg_json)
            await websocket.send(bpm_json)

            print("Processed ecg:", ecg_recording)
            print("Bpm:", bpm_recording)

            buffer.clear()

# WebSocket communication setup
async def connect_websocket():
    uri = "ws://192.168.180.153:8000/ws"  # Replace with the actual IP of your FastAPI server
    async with websockets.connect(uri) as websocket:
        # Run the asynchronous simulation
        await simulate_realtime_ecg_data(websocket)

# Run the event loop for data generation and WebSocket communication
asyncio.get_event_loop().run_until_complete(connect_websocket())

