try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class MidiViewerToplevel(tk.Toplevel):
    def __init__(self, midi_obj):
        self.height = 500
        self.width = 1000
        tk.Toplevel.__init__(self, height=self.height, width=self.width)
        self.resizable(False, False)
        self.midi_object = midi_obj

        self.init_ui()

    def init_ui(self):
        info_frame = tk.Frame(self, bd=3, bg='darkgray')
        info_frame.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        midi_text = tk.Text(info_frame, bg='lightgray')

        for i, track in enumerate(self.midi_object.midi_file.tracks):
            midi_text.insert(tk.INSERT, 'Track {}: {}'.format(i, track.name))
            for msg in track:
                midi_text.insert(tk.INSERT, msg)
                midi_text.insert(tk.INSERT, '\n')

        midi_text.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)