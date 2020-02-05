try:
    import Tkinter as tk
    import TkFileDialog
except ImportError:
    import tkinter as tk
    from tkinter import filedialog

from DefaultToplevel import DefaultToplevel
from MidiManager import MidiManager
from MidiViewerToplevel import MidiViewerToplevel


class MidiManagerToplevel(DefaultToplevel):
    def __init__(self, parent, path):
        self.path = path
        self.midi_object = MidiManager(self.path, midi_file=True)
        super().__init__(parent)

    def init_ui(self):
        menu_frame = tk.Frame(self, bd=3, bg='darkgray', height=self.height, width=self.width)
        menu_frame.place(x=0, y=0)

        midi_btn = tk.Button(menu_frame, text='Show Midi Info', bd=2, command=lambda: self.show_midi())
        score_btn = tk.Button(menu_frame, text='Convert to Score File', bd=2, command=lambda: self.convert_to_score())

        midi_btn.place(relx=0, relwidth=1.0 / 2.0, relheight=1.0)
        score_btn.place(relx=1.0/2.0, relwidth=1.0 / 2.0, relheight=1.0)

    def show_midi(self):
        return MidiViewerToplevel(self.midi_object)

    def convert_to_score(self):
        self.midi_object.convert_midi_to_stream(self.path)


def main():
    root = tk.Tk()
    root.width = 750
    root.x = 0
    root.y = 0
    top = MidiManagerToplevel(root, 'C:/users/Lenovo/Desktop/sc.mid')
    root.mainloop()


if __name__ == '__main__':
    main()
