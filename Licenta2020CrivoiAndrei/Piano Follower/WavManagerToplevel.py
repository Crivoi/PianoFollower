try:
    import Tkinter as tk
    import TkFileDialog
except ImportError:
    import tkinter as tk

import librosa

from DefaultToplevel import DefaultToplevel
from TranscriptionToplevel import TranscriptionToplevel
from Plotter import Plotter


def plot_waveform(wav_data, sr):
    wav_plotter = Plotter(wav_data, sr)
    wav_plotter.plot_waveform()


def plot_spectogram(wav_data, sr):
    spec_plotter = Plotter(wav_data, sr)
    spec_plotter.plot_spectrogram()


class WavManagerToplevel(DefaultToplevel):
    def __init__(self, parent, path):
        self.path = path
        self.filename = self.path.split('/')[-1].split('.')[0]
        self.wav_file, self.sr = librosa.load(self.path, sr=None, mono=True)
        super().__init__(parent)

    def init_ui(self):
        menu_frame = tk.Frame(self, bd=3, bg='darkgray', height=self.height, width=self.width)
        menu_frame.place(x=0, y=0)

        name_label = tk.Label(menu_frame, text=self.filename)
        name_label.place(x=0, y=0, relwidth=1.0, relheight=2.0 / 5.0)

        waveform_btn = tk.Button(menu_frame, text='Plot Waveform', relief='raised',
                                 command=lambda: plot_waveform(self.wav_file, self.sr))
        spec_btn = tk.Button(menu_frame, text='Plot Spectrogram', relief='raised',
                             command=lambda: plot_spectogram(self.wav_file, self.sr))
        convert_btn = tk.Button(menu_frame, text='Convert', relief='raised',
                                command=lambda: self.open_transcription_toplevel(self.path))

        waveform_btn.place(relx=0.0, rely=2.0 / 5.0, relwidth=1.0 / 3.0, relheight=3.0 / 5.0)
        spec_btn.place(relx=1.0 / 3.0, rely=2.0 / 5.0, relwidth=1.0 / 3.0, relheight=3.0 / 5.0)
        convert_btn.place(relx=2.0 / 3.0, rely=2.0 / 5.0, relwidth=1.0 / 3.0, relheight=3.0 / 5.0)

    def open_transcription_toplevel(self, path):
        self.destroy()
        return TranscriptionToplevel(self.parent, path)


def main():
    root = tk.Tk()
    root.width = 600
    root.x = 100
    root.y = 100
    top = WavManagerToplevel(root, 'D:/An3Sem2/licenta/samples/sweet_child.wav')
    root.mainloop()


if __name__ == '__main__':
    main()
