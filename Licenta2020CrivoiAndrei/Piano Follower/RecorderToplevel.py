try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from _thread import start_new_thread

from DefaultToplevel import DefaultToplevel
from AudioRecorder import AudioRecorder


class RecorderToplevel(DefaultToplevel):
    def __init__(self, parent):
        self.recorder = AudioRecorder('output.wav')
        super().__init__(parent)

    def convert_mxl(self):
        self.recorder.transcriptor.transcript()
        self.recorder.transcriptor.show_stream()

    def init_ui(self):
        menu_frame = tk.Frame(self, bd=3, bg='darkgray', height=self.height, width=self.width)
        menu_frame.place(x=0, y=0)

        rec_btn = tk.Button(menu_frame, text='Record', bd=2, relief='raised',
                            command=lambda: start_new_thread(self.recorder.init_rec, ()))
        rec_btn.place(relx=0, y=0, relwidth=1.0 / 5.0, relheight=menu_frame.winfo_height())

        stop_btn = tk.Button(menu_frame, text='Stop \nRecording', bd=2, relief='raised',
                             command=lambda: self.recorder.stop_rec())
        stop_btn.place(relx=1.0 / 5.0, y=0, relwidth=1.0 / 5.0,
                       relheight=menu_frame.winfo_height())

        export_btn = tk.Button(menu_frame, text='Export \nWav', bd=2, relief='raised',
                               command=lambda: self.recorder.export_wav())
        export_btn.place(relx=2.0 / 5.0, y=0, relwidth=1.0 / 5.0,
                         relheight=menu_frame.winfo_height())

        convert_mid_btn = tk.Button(menu_frame, text='Convert To Midi', bd=2, relief='raised',
                                    command=lambda: self.recorder.transcriptor.convert_stream_to_midi())
        convert_mid_btn.place(relx=3.0 / 5.0, y=0, relwidth=1.0 / 5.0,
                              relheight=menu_frame.winfo_height())

        convert_mxl_btn = tk.Button(menu_frame, text='Convert To Score', bd=2, relief='raised',
                                    command=lambda: self.convert_mxl())
        convert_mxl_btn.place(relx=4.0 / 5.0, y=0, relwidth=1.0 / 5.0,
                              relheight=menu_frame.winfo_height())


def main():
    root = tk.Tk()
    top = RecorderToplevel()
    root.mainloop()


if __name__ == '__main__':
    main()
