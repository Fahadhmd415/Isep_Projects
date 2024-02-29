import neurokit2 as nk
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import numpy as np

ecg_data = []  # Buffer to store ECG data received from MQTT

def on_message(client, userdata, message):
    ecg_value = float(message.payload.decode())
    ecg_data.append(ecg_value)

client = mqtt.Client("RaspberryPiClient")  # Change the client ID if needed
client.on_message = on_message

mqtt_broker = "192.168.180.153"  # Replace with your MQTT broker's IP address
mqtt_topic = "ecgData"  # MQTT topic for ECG data

client.connect(mqtt_broker, 1883, 60)
client.subscribe(mqtt_topic)

print("MQTT Subscriber started...")
client.loop_start()

try:
    while True:
        if len(ecg_data) >= 600:  # Number of samples for processing (adjust as needed)
            # Sample ECG data received from MQTT
            ecg_signal = np.array(ecg_data)
            sampling_rate = 22  # Sampling rate in Hz (adjust if different)

            # Extract R-peaks locations using NeuroKit2
            _, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=sampling_rate, method="pantompkins1985")

            # Calculate threshold based on the amplitude of the ECG signal
            threshold = 1.2  # You can adjust the multiplier as needed
            print(threshold)

            # Filter R-peaks based on amplitude
            filtered_rpeaks = [peak for peak in rpeaks['ECG_R_Peaks'] if ecg_signal[peak] > threshold]

            # Calculate average heart rate in BPM
            average_heart_rate = np.mean(nk.ecg_rate(filtered_rpeaks, sampling_rate=sampling_rate))

            # Visualize ECG signal with detected R-peaks
            time_seconds = np.arange(len(ecg_signal)) / sampling_rate
            plt.figure(figsize=(12, 6))
            plt.plot(time_seconds, ecg_signal, color='blue', label='ECG Signal')
            plt.plot(np.array(filtered_rpeaks) / sampling_rate, np.array(ecg_signal)[filtered_rpeaks], 'ro', markersize=8, label='R-peaks')
            plt.xlabel('Time (seconds)')
            plt.ylabel('ECG Value (mV)')
            plt.title('ECG Signal with Detected R-peaks')
            plt.legend()
            plt.grid(True)
            plt.show()

            ecg_data.clear()  # Clear the buffer for the next set of data



except KeyboardInterrupt:
    print("Interrupted. Exiting...")
    client.loop_stop()

