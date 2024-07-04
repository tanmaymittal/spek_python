import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

def decode_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))
    return samples, audio.frame_rate

def plot_spectrum(samples, sample_rate):
    if len(samples.shape) == 2:
        samples = samples.mean(axis=1)
    
    # n = len(samples)
    # duration = n / sample_rate
    # time = np.linspace(0., duration, n)
    
    # plt.specgram(samples, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap='inferno')

    plt.figure(figsize=(10, 6))
    Pxx, freqs, bins, im = plt.specgram(samples, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap='inferno', vmin=-120, vmax=0)

    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.colorbar(label='Intensity (dB)')
    plt.title('Spectrogram')
    plt.show()

def run_spek():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.m4a"),("All Files", "*.*")])
    
    if file_path:
        samples, sample_rate = decode_audio(file_path)
        plot_spectrum(samples, sample_rate)
    else:
        print("No file selected")

if __name__ == "__main__":
    run_spek()
