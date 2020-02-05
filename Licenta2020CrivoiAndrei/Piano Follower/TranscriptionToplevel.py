try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
    from tkinter import filedialog

from DefaultToplevel import DefaultToplevel
from Transcriptor import Transcriptor
from ScoreManager import ScoreManager


class TranscriptionToplevel(DefaultToplevel):
    def __init__(self, parent, path):
        self.path = path
        self.transcriptor = Transcriptor(self.path)
        self.transcriptor.transcript()
        super().__init__(parent)

    def init_ui(self):
        menu_frame = tk.Frame(self, bd=3, bg='darkgray', height=self.height, width=self.width)
        menu_frame.place(x=0, y=0)

        transcript_btn = tk.Button(menu_frame, text='Show Musical Score', relief='raised',
                                   command=lambda: self.transcriptor.show_stream())
        transcript_btn.place(relx=0, rely=0, relheight=1.0, relwidth=1.0 / 3.0)

        display_cqt_btn = tk.Button(menu_frame, text='Display CQT', relief='raised',
                                    command=lambda: self.transcriptor.display_cqt_tuning())
        display_cqt_btn.place(relx=1.0/3.0, rely=0, relheight=1.0, relwidth=1.0 / 3.0)

        compare_btn = tk.Button(menu_frame, text='Compare with another score', relief='raised',
                                command=lambda: self.compare_scores())
        compare_btn.place(relx=2.0/3.0, rely=0, relheight=1.0, relwidth=1.0 / 3.0)

    def compare_scores(self):
        score_obj = ScoreManager(self.transcriptor.stream)
        filename = filedialog.askopenfilename(initialdir="/", title="Select Score To Compare",
                                              filetypes=(('score files', '*.mxl'), ('all files', '*.*')))
        score_obj.compare(filename)


def main():
    root = tk.Tk()
    root.width = 600
    root.x = 0
    root.y = 0
    top = TranscriptionToplevel(root, '../samples/sweet_child.wav')
    root.mainloop()


if __name__ == '__main__':
    main()
