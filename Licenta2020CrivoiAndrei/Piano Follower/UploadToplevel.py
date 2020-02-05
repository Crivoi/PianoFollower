try:
    import Tkinter as tk
    import TkFileDialog
except ImportError:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import StringVar

from DefaultToplevel import DefaultToplevel
from WavManagerToplevel import WavManagerToplevel
from MidiManagerToplevel import MidiManagerToplevel
from ScoreManagerToplevel import ScoreManagerToplevel


class UploadToplevel(DefaultToplevel):
    def __init__(self, parent):
        super().__init__(parent)

    def init_ui(self):
        menu_frame = tk.Frame(self, bd=3, bg='darkgray', height=self.height, width=self.width)
        menu_frame.place(x=0, y=0)

        wav_btn = tk.Button(menu_frame, text='Import Wav', bd=2, relief='raised',
                            command=lambda: self.upload_file(file_types=(('wav files', ('*.wav', '*.wave')),
                                                                         ('all files', '*.*'))))
        wav_btn.name = 'wav_btn'
        wav_btn.place(x=0, y=0, relwidth=1.0 / 3.0, relheight=menu_frame.winfo_height())

        midi_btn = tk.Button(menu_frame, text='Import Midi', bd=2, relief='raised',
                             command=lambda: self.upload_file(file_types=(('midi files', ('*.mid', '*.midi')),
                                                                          ('all files', '*.*'))))
        midi_btn.name = 'midi_btn'
        midi_btn.place(relx=1.0 / 3.0, y=0, relwidth=1.0 / 3.0, relheight=menu_frame.winfo_height())

        score_btn = tk.Button(menu_frame, text='Import Score', bd=2, relief='raised',
                              command=lambda: self.upload_file(file_types=(('score files', '*.mxl'),
                                                                           ('all files', '*.*'))))
        score_btn.name = 'score_btn'
        score_btn.place(relx=2.0 / 3.0, y=0, relwidth=1.0 / 3.0, relheight=menu_frame.winfo_height())

    def upload_file(self, file_types=('all files', '*.*')):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=file_types)
        extension = file_path.split('/')[-1].split('.')[-1]
        if extension == 'wav' or extension == 'wave':
            self.open_wav_toplevel(file_path)
        elif extension == 'mid' or extension == 'midi':
            self.open_midi_toplevel(file_path)
        elif extension == 'mxl':
            self.open_mxl_toplevel(file_path)

    def open_wav_toplevel(self, path):
        self.destroy()
        return WavManagerToplevel(self.parent, path)

    def open_midi_toplevel(self, path):
        self.destroy()
        return MidiManagerToplevel(self.parent, path)

    def open_mxl_toplevel(self, path):
        self.destroy()
        return ScoreManagerToplevel(self.parent, path)


if __name__ == '__main__':
    pass
