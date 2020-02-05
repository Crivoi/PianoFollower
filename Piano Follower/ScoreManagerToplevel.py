try:
    import Tkinter as tk
    import TkFileDialog
except ImportError:
    import tkinter as tk
    from tkinter import filedialog

from DefaultToplevel import DefaultToplevel
from ScoreManager import ScoreManager


class ScoreManagerToplevel(DefaultToplevel):
    def __init__(self, parent, path):
        self.path = path
        self.score_object = ScoreManager(self.path)
        super().__init__(parent)

    def init_ui(self):
        menu_frame = tk.Frame(self, bd=3, bg='darkgray', height=self.height, width=self.width)
        menu_frame.place(x=0, y=0)

        show_btn = tk.Button(menu_frame, text='Show Music Sheet', bd=2, command=lambda: self.score_object.show())
        midi_btn = tk.Button(menu_frame, text='Convert to Midi File', bd=2,
                             command=lambda: self.score_object.convert_stream_to_midi())
        compare_scores_btn = tk.Button(menu_frame, text='Compare to another Score File', bd=2,
                                       command=lambda: self.compare_scores())

        show_btn.place(relx=0, relwidth=1.0 / 3.0, relheight=1.0)
        midi_btn.place(relx=1.0 / 3.0, relwidth=1.0 / 3.0, relheight=1.0)
        compare_scores_btn.place(relx=2.0 / 3.0, relwidth=1.0 / 3.0, relheight=1.0)

    def compare_scores(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select Score To Compare",
                                              filetypes=(('score files', '*.mxl'), ('all files', '*.*')))
        self.score_object.compare(filename)


def main():
    root = tk.Tk()
    root.width = 600
    root.x = 100
    root.y = 100
    top = ScoreManagerToplevel(root, 'C:/users/Lenovo/Desktop/sc.mxl')
    root.mainloop()


if __name__ == '__main__':
    main()
