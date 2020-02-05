import matplotlib.pyplot as plt
import matplotlib.figure as fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
plt.rc("figure", figsize=(8, 3))

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class Plotter(tk.Toplevel):
    def __init__(self, wav_data, sr):
        tk.Toplevel.__init__(self)
        self.wav_data = wav_data
        self.sr = sr

    def plot_waveform(self):
        f = fig.Figure()
        f.add_subplot(111).plot(self.wav_data)
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_spectrogram(self):
        f = fig.Figure()
        f.add_subplot(111).specgram(self.wav_data, NFFT=1024, noverlap=900, Fs=self.sr)
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

