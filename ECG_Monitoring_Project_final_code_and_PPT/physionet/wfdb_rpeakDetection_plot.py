import neurokit2 as nk
import matplotlib.pyplot as plt
import numpy as np
import wfdb

# Load the ECG signal
sig, fields = wfdb.rdsamp('./I01')

# Set the desired sampling rate
target_sampling_rate = 257

# Resample the ECG signal if the original sampling rate is different
ecg_signal = nk.signal_resample(sig[:, 0], sampling_rate=fields['fs'], desired_sampling_rate=target_sampling_rate, method="interpolation")

# Clean the ECG signal using NeuroKit2
ecg_cleaned = nk.ecg_clean(ecg_signal, sampling_rate=target_sampling_rate, method='neurokit')

# Extract R-peaks locations using NeuroKit2
_, rpeaks = nk.ecg_peaks(ecg_cleaned, sampling_rate=target_sampling_rate, method="neurokit")

# Access R-peaks from the dictionary
rpeaks = rpeaks['ECG_R_Peaks']

# Set the desired duration (e.g., 10 seconds)
duration = 10
num_samples = int(duration * target_sampling_rate)

# Visualize ECG signal with detected R-peaks for the specified duration
time_seconds = np.arange(num_samples) / target_sampling_rate
plt.figure(figsize=(12, 6))
plt.plot(time_seconds, ecg_cleaned[:num_samples], color='blue', label='Cleaned ECG Signal')
plt.plot(np.array(rpeaks[rpeaks < num_samples]) / target_sampling_rate, np.array(ecg_cleaned)[rpeaks[rpeaks < num_samples]], 'ro', markersize=8, label='R-peaks')
plt.xlabel('Time (seconds)')
plt.ylabel('ECG Value (mV)')
plt.title(f'Cleaned ECG Signal with Detected R-peaks (Duration: {duration} seconds) at {target_sampling_rate} Hz')
plt.legend()
plt.grid(True)
plt.show()

