try:
    import Tkinter as tk
    import TkFileDialog
except ImportError:
    import tkinter as tk
    from tkinter import filedialog

from DefaultToplevel import DefaultToplevel
from MidiManager import MidiManager


class PianoManagerToplevel(DefaultToplevel):
    def __init__(self, parent):
        self.midi_object = MidiManager('../recordings/midi_rec.txt')
        super().__init__(parent)

    def init_ui(self):
        menu_frame = tk.Frame(self, bd=3, bg='darkgray', height=self.height, width=self.width)
        menu_frame.place(x=0, y=0)

        midi_btn = tk.Button(menu_frame, text='Convert to Midi File', bd=2, command=lambda: self.convert_to_midi())
        score_btn = tk.Button(menu_frame, text='Convert to Score File', bd=2, command=lambda: self.convert_to_score())

        midi_btn.place(relx=0, relwidth=1.0 / 2.0, relheight=1.0)
        score_btn.place(relx=1.0/2.0, relwidth=1.0 / 2.0, relheight=1.0)

    def convert_to_midi(self):
        self.midi_object.midi_msg_to_mido_msg()
        file = filedialog.asksaveasfile(initialdir="/", title="Save file",
                                        filetypes=(('midi files', ('*.mid', '*.midi')),
                                                   ('all files', '*.*')))

        self.midi_object.save_midi(file.name)

    def convert_to_score(self):
        file_path = filedialog.askopenfilename(initialdir='/', title='Open Midi',
                                               filetypes=(('midi files', ('*.mid', '*.midi')),
                                                          ('all files', '*.*')))
        self.midi_object.convert_midi_to_stream(file_path)
