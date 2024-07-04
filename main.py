import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from matplotlib.ticker import MaxNLocator

def decode_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))
    return samples, audio.frame_rate

def plot_spectrum(samples, sample_rate):
    if len(samples.shape) == 2:
        samples = samples.mean(axis=1)
    
    # This code was commented to fix the dB scale issue.
    # n = len(samples)
    # duration = n / sample_rate
    # time = np.linspace(0., duration, n)
    # plt.specgram(samples, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap='inferno')

    # This code was added to fix the dB Scale issue.
    plt.figure(figsize=(10, 6))
    Pxx, freqs, bins, im = plt.specgram(samples, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap='inferno', vmin=-120, vmax=0)

    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.colorbar(label='Intensity (dB)')
    plt.title('Spectrogram')

    # Adjust x-axis to show markers every 15 seconds
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both'))
    plt.xticks(np.arange(0, bins[-1], step=15))

    plt.show()

    return freqs, Pxx

def plot_spectrum_multiple(samples, sample_rate, title):
    if len(samples.shape) == 2:
        samples = samples.mean(axis=1)
    
    plt.figure(figsize=(10, 6))
    Pxx, freqs, bins, im = plt.specgram(samples, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap='inferno', vmin=-120, vmax=0)
    
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.colorbar(label='Intensity (dB)')
    plt.title(title)
    
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True, prune='both'))
    plt.xticks(np.arange(0, bins[-1], step=15))

    return freqs, Pxx


def determine_cutoff(freqs, Pxx):
    avg_intensity = np.mean(Pxx, axis=1)
    threshold_db = -60  # Threshold in dB to determine significant energy
    cutoff_index = np.where(avg_intensity > 10**(threshold_db / 10))[0]
    
    if cutoff_index.size == 0:
        return 0  # No significant energy found
    cutoff_freq = freqs[cutoff_index[-1]]
    return cutoff_freq  

def determine_dominant_frequency_band(freqs, Pxx, bands):
    avg_intensity = np.mean(Pxx, axis=1)
    band_energy = np.zeros(len(bands) - 1)
    
    for i in range(len(bands) - 1):
        band_indices = np.where((freqs >= bands[i]) & (freqs < bands[i + 1]))[0]
        band_energy[i] = np.sum(avg_intensity[band_indices])
    
    dominant_band_index = np.argmax(band_energy)
    dominant_band = (bands[dominant_band_index], bands[dominant_band_index + 1])
    return dominant_band

def run_spek_multiple_v2():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select Audio Files", filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.m4a"),("All Files", "*.*")])
    
    if file_paths:
        for file_path in file_paths:
            print(f"Processing file: {file_path}")
            samples, sample_rate = decode_audio(file_path)
            title = f"{file_path.split('/')[-1]}"
            freqs, Pxx = plot_spectrum_multiple(samples, sample_rate, title)
            cutoff_freq = determine_cutoff(freqs, Pxx)
            print(f"Cutoff Frequency: {cutoff_freq} Hz")
            
            # Define frequency bands (in Hz)
            bands = [0, 250, 500, 1000, 2000, 4000, 8000, 16000, 20000]
            dominant_band = determine_dominant_frequency_band(freqs, Pxx, bands)
            print(f"Dominant Frequency Band: {dominant_band[0]} Hz - {dominant_band[1]} Hz")
        
        plt.show()  # Show all plots at once
    else:
        print("No file selected")


def run_spek_multiple():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select Audio Files", filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.m4a"),("All Files", "*.*")])
    
    if file_paths:
        for file_path in file_paths:
            print(f"Processing file: {file_path}")
            samples, sample_rate = decode_audio(file_path)
            freqs, Pxx = plot_spectrum(samples, sample_rate)
            cutoff_freq = determine_cutoff(freqs, Pxx)
            print(f"Cutoff Frequency: {cutoff_freq} Hz")
            
            # Define frequency bands (in Hz)
            bands = [0, 250, 500, 1000, 2000, 4000, 8000, 16000, 20000]
            dominant_band = determine_dominant_frequency_band(freqs, Pxx, bands)
            print(f"Dominant Frequency Band: {dominant_band[0]} Hz - {dominant_band[1]} Hz")
    else:
        print("No file selected")


def run_spek():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.m4a"),("All Files", "*.*")])
    
    if file_path:
        samples, sample_rate = decode_audio(file_path)
        freqs, Pxx = plot_spectrum(samples, sample_rate)
        cutoff_freq = determine_cutoff(freqs, Pxx)
        print(f"Cutoff Frequency: {cutoff_freq} Hz")

        # Define frequency bands (in Hz)
        bands = [8000, 10000, 12000, 14000, 16000, 18000, 20000]
        dominant_band = determine_dominant_frequency_band(freqs, Pxx, bands)
        print(f"Dominant Frequency Band: {dominant_band[0]} Hz - {dominant_band[1]} Hz")
    else:
        print("No file selected")



if __name__ == "__main__":
    run_spek_multiple_v2()
