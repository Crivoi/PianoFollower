try:
    import Tkinter as tk
    import TkFileDialog
except ImportError:
    import tkinter as tk
    from tkinter import filedialog

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from librosa import note_to_hz

import music21 as m21

matplotlib.use('TkAgg')


class ScoreComparerToplevel(tk.Toplevel):
    def __init__(self, stream1, stream2):
        self.height = 600
        self.width = 1000
        tk.Toplevel.__init__(self, height=self.height, width=self.width)
        self.resizable(False, False)

        self.stream1 = stream1
        self.stream2 = stream2

        self.init_ui()

    def init_ui(self):
        stream1_frame = tk.Frame(self, bd=3, bg='darkgray')
        stream1_frame.place(relx=0, rely=0, relheight=1.0 / 2.5, relwidth=1.0 / 2.0)

        stream2_frame = tk.Frame(self, bd=3, bg='darkgray')
        stream2_frame.place(relx=1.0 / 2.0, rely=0, relheight=1.0 / 2.5, relwidth=1.0 / 2.0)

        text1 = tk.Text(stream1_frame, bg='lightgray')
        text2 = tk.Text(stream2_frame, bg='lightgray')

        list1notes = []
        list1offsets = []
        list2notes = []
        list2offsets = []

        for i in range(min(len(self.stream1), len(self.stream2))):
            if self.stream2[i] != self.stream1[i]:
                text1.insert(tk.INSERT, str(i + 1) + ' ' + self.stream1[i] + '\n')
                list1notes.append(note_to_hz(self.stream1[i].split(' ')[0]))
                list1offsets.append(self.stream1[i].split(' ')[-1])
                text2.insert(tk.INSERT, str(i + 1) + ' ' + self.stream2[i] + ' Error ' + '\n')
                list2notes.append(note_to_hz(self.stream2[i].split(' ')[0]))
                list2offsets.append(self.stream2[i].split(' ')[-1])
            else:
                text1.insert(tk.INSERT, str(i + 1) + ' ' + self.stream1[i] + '\n')
                list1notes.append(note_to_hz(self.stream1[i].split(' ')[0]))
                list1offsets.append(self.stream1[i].split(' ')[-1])
                text2.insert(tk.INSERT, str(i + 1) + ' ' + self.stream2[i] + '\n')
                list2notes.append(note_to_hz(self.stream2[i].split(' ')[0]))
                list2offsets.append(self.stream1[i].split(' ')[-1])

        text1.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)
        text2.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        plt_frame = tk.Frame(self, bd=3, bg='darkgray')
        plt_frame.place(relx=0, rely=1.0 / 2.5, relheight=1.5 / 2.5, relwidth=1.0)

        f = Figure()
        a = f.add_subplot(211, xlabel='Offset', ylabel='Notes', ylim=(note_to_hz('B-3'), note_to_hz('B5')))
        b = f.add_subplot(212, xlabel='Offset', ylabel='Notes', ylim=(note_to_hz('B-3'), note_to_hz('B5')))
        a.plot(list1offsets, list1notes, color='green')
        b.plot(list2offsets, list2notes, color='blue')
        canvas = FigureCanvasTkAgg(f, master=plt_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def main():
    root = tk.Tk()
    stream1 = []
    stream2 = []

    # score = m21.converter.parse('C:\\Users\\Lenovo\\Desktop\\sc.mxl')
    score2 = m21.corpus.parse('bwv66.6')
    score = m21.corpus.parse('bwv67.4')

    for note in score.flat.notes:
        stream1.append(str(note.pitch) + ' ' + str(note.offset))

    for note in score2.flat.notes:
        stream2.append(str(note.pitch) + ' ' + str(note.offset))

    top = ScoreComparerToplevel(stream1, stream2)
    root.mainloop()


if __name__ == '__main__':
    main()
