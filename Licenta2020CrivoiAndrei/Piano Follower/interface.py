try:
    import Tkinter as tk
    import TkFileDialog
except ImportError:
    import tkinter as tk
    from tkinter import filedialog

import time as t
import pygame as pg
import pygame.midi as midi
import simpleaudio as sa

from UploadToplevel import UploadToplevel
from RecorderToplevel import RecorderToplevel
from PianoManagerToplevel import PianoManagerToplevel

from _thread import start_new_thread


pg.init()
pg.mixer.init()
midi.init()

start = t.time()
octave = 3
recording = False
midi_recording = False

file = open('../recordings/rec.txt', 'w')
file.close()

file = open('../recordings/midi_rec.txt', 'w')
file.close()


def increment_octave():
    global octave
    octave += 1
    if octave >= 6:
        octave = 6
    print('Octave set to: ' + str(octave))


def decrement_octave():
    global octave
    octave -= 1
    if octave <= 1:
        octave = 1
    print('Octave set to: ' + str(octave))


def play_note(note, mode='sa'):
    global octave
    try:
        if mode == 'pg':
            sound = pg.mixer.Sound('../samples/grand_piano_samples/piano_notes ' + str(note) + str(octave) + '.wav')
            sound.play()
            sound.fadeout(150)
            return
        elif mode == 'sa':
            sound = sa.WaveObject.from_wave_file('../samples/grand_piano_samples/piano_notes ' + str(note) +
                                                 str(octave) + '.wav')
            sound.play()
            return
    except FileNotFoundError:
        pass


def play_midi(note, mode='sa'):
    try:
        if mode == 'pg':
            sound = pg.mixer.Sound('../samples/grand_piano_samples/piano_notes ' + str(note) + '.wav')
            sound.play()
            sound.fadeout(150)
            return
        elif mode == 'sa':
            sound = sa.WaveObject.from_wave_file('../samples/grand_piano_samples/piano_notes ' + str(note) + '.wav')
            sound.play()
            return
    except FileNotFoundError:
        pass


def label_press(event):
    if len(event.widget.name) == 1:
        img = '../pictures/white_key_pressed.gif'
    elif len(event.widget.name) == 2:
        img = '../pictures/black_key_pressed.gif'
    elif event.widget.name == 'rec_button':
        img = '../pictures/red_button_pressed.gif'
    else:
        img = '../pictures/green_button_pressed.gif'
    key_img = tk.PhotoImage(file=img)
    event.widget.configure(image=key_img)
    event.widget.image = key_img


def label_release(event):
    if len(event.widget.name) == 1:
        img = '../pictures/white_key.gif'
        info = [128, event.widget.name + str(octave)]
        if recording:
            record('../recordings/rec.txt', info)
    elif len(event.widget.name) == 2:
        img = '../pictures/black_key.gif'
    elif event.widget.name == 'rec_button':
        img = '../pictures/red_button.gif'
    else:
        img = '../pictures/green_button.gif'
    key_img = tk.PhotoImage(file=img)
    event.widget.configure(image=key_img)
    event.widget.image = key_img


def find_label(name, keys):
    for x in range(len(keys)):
        if name == keys[x][1]:
            return keys[x][2]


def find_key(note):
    for i in KEYS_TO_NOTES:
        if KEYS_TO_NOTES[i] == note[0]:
            return i


def find_midi_by_key(note):
    for i in MIDI_TO_NOTES.keys():
        if MIDI_TO_NOTES[i] == note:
            return i


def midi_press(event, keys):
    note = MIDI_TO_NOTES.get(event[0][1])
    if note:
        play_midi(note)
        if recording:
            record_midi('../recordings/midi_rec.txt', event)
        if len(note) == 2:
            img = '../pictures/white_key_pressed.gif'
        elif len(note) == 3:
            img = '../pictures/black_key_pressed.gif'
        try:
            key_img = tk.PhotoImage(file=img)
            find_label(note[:-1], keys).configure(image=key_img)
            find_label(note[:-1], keys).image = key_img
        except TypeError:
            pass


def midi_release(event, keys):
    note = MIDI_TO_NOTES.get(event[0][1])
    if note:
        print(str(note))
        if recording:
            record_midi('../recordings/midi_rec.txt', event)
        if len(note) == 2:
            img = '../pictures/white_key.gif'
        elif len(note) == 3:
            img = '../pictures/black_key.gif'
        try:
            key_img = tk.PhotoImage(file=img)
            find_label(note[:-1], keys).configure(image=key_img)
            find_label(note[:-1], keys).image = key_img
        except TypeError:
            pass


def key_press(event):
    note = KEYS_TO_NOTES.get(event.char, None)
    info = [144, note]
    if note:
        play_note(note)
        if recording:
            record('../recordings/rec.txt', info)
        if len(note) == 1:
            img = '../pictures/white_key_pressed.gif'
        else:
            img = '../pictures/black_key_pressed.gif'
        key_img = tk.PhotoImage(file=img)
        find_label(note, event.widget.keys).configure(image=key_img)
        find_label(note, event.widget.keys).image = key_img


def key_release(event):
    note = KEYS_TO_NOTES.get(event.char, None)
    info = [128, note]
    if note:
        # print(str(note) + str(octave))
        if recording:
            record('../recordings/rec.txt', info)
        if len(note) == 1:
            img = '../pictures/white_key.gif'
        else:
            img = '../pictures/black_key.gif'
        key_img = tk.PhotoImage(file=img)
        find_label(note, event.widget.keys).configure(image=key_img)
        find_label(note, event.widget.keys).image = key_img


def button_press(event):
    try:
        if event.widget.x <= 300:
            wave_obj = sa.WaveObject.from_wave_file('../samples/grand_piano_samples/piano_notes ' + event.widget.name +
                                                    str(octave) + '.wav')
            wave_obj.play()
            print(event.widget.name + str(octave))
            if recording:
                info = [144, event.widget.name + str(octave)]
                record('../recordings/rec.txt', info)
        else:
            wave_obj = sa.WaveObject.from_wave_file('../samples/grand_piano_samples/piano_notes ' + event.widget.name +
                                                    str(octave + 1) + '.wav')
            wave_obj.play()
            if recording:
                info = [144, event.widget.name + str(octave + 1)]
                record('../recordings/rec.txt', info)
        label_press(event)
    except FileNotFoundError:
        pass


def record_on_off(event):
    global recording
    recording = not recording
    print('Recording: ', recording)
    if recording:
        label_press(event)
    else:
        label_release(event)


def record(filename, info):
    print("info: " + str(info))
    song_file = open(filename, 'a')
    note = info[1]
    msg_type = info[0]
    velocity = 100
    end = t.time()
    time = end - start
    if len(note) == 1:
        if msg_type == 144:
            song_file.write(note + str(octave) + ' ' + str(time) + ' ' + str(msg_type))
            song_file.write('\n')
        midi_msg = [[msg_type, find_midi_by_key(str(note) + str(octave)), velocity, 0], round(time * 1000)]
        midi_file = open('../recordings/midi_rec.txt', 'a')
        midi_file.write(str(midi_msg) + '\n')
    elif len(note) == 2 and '#' not in note or len(note) == 3:
        if msg_type == 144:
            song_file.write(note + ' ' + str(time) + ' ' + str(msg_type))
            song_file.write('\n')
        midi_msg = [[msg_type, find_midi_by_key(str(note)), velocity, 0], round(time * 1000)]
        midi_file = open('../recordings/midi_rec.txt', 'a')
        midi_file.write(str(midi_msg) + '\n')
    elif len(note) == 2 and '#' in note:
        if msg_type == 144:
            song_file.write(note + str(octave) + ' ' + str(time) + ' ' + str(msg_type))
            song_file.write('\n')
        midi_msg = [[msg_type, find_midi_by_key(str(note) + str(octave)), velocity, 0], round(time * 1000)]
        midi_file = open('../recordings/midi_rec.txt', 'a')
        midi_file.write(str(midi_msg) + '\n')


def record_midi(filename, msg):
    print(type(msg))
    midi_file = open(filename, 'a')
    midi_file.write(str(msg) + '\n')
    if msg[0][0] == 144:
        song_file = open('../recordings/rec.txt', 'a')
        song_file.write(str(MIDI_TO_NOTES[msg[0][1]]) + ' ' + str(0.03 * round(msg[1] / 1000 / 0.03)) + ' ' + str(msg[0][0]))
        song_file.write('\n')


def play(filename):
    song_file = open(filename, 'r')
    print("Playback Started")
    first_line = song_file.readline().split()
    note = first_line[0]
    time_scale = float(first_line[1])
    for line in song_file:
        wave_obj = sa.WaveObject.from_wave_file('../samples/grand_piano_samples/piano_notes ' + note + '.wav')
        wave_obj.play()
        line_elements = line.split()
        note = line_elements[0]
        time = float(line_elements[1])
        t.sleep(time - time_scale)
        time_scale = time
    wave_obj = sa.WaveObject.from_wave_file('../samples/grand_piano_samples/piano_notes ' + note + '.wav')
    wave_obj.play()
    print("Playback Stopped")
    song_file.close()


def play_back(event):
    label_press(event)
    start_new_thread(play, ('../recordings/rec.txt',))


def save_file():
    filename = filedialog.asksaveasfile(initialdir="/", title="Save file")
    print(filename)


KEYS_TO_NOTES = {
    'a': 'C',
    's': 'D',
    'd': 'E',
    'f': 'F',
    'g': 'G',
    'h': 'A',
    'j': 'B',
    'w': 'C#',
    'e': 'D#',
    't': 'F#',
    'y': 'G#',
    'u': 'A#'
}

NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
OCTAVES = ['1', '2', '3', '4']
counter = 24

MIDI_TO_NOTES = {}

for octv in OCTAVES:
    for nt in NOTES:
        MIDI_TO_NOTES[counter] = nt + octv
        counter += 1
        if nt in ['C', 'D', 'F', 'G', 'A']:
            MIDI_TO_NOTES[counter] = nt + '#' + octv
            counter += 1


class PianoFollower(tk.Frame):
    def __init__(self, parent):
        self.width = 750
        self.height = 250
        tk.Frame.__init__(self, parent, background='SkyBlue')

        self.parent = parent
        self.parent.title('Piano Follower')
        self.parent.resizable(False, False)

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        self.x = int((sw - self.width) / 2)
        self.y = int((sh - self.height) / 2)
        self.parent.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))

        self.init_ui()
        try:
            self.midi_input = pg.midi.Input(1, 0)
            self.midi_input.read(1)
            self.midi_handle()
        except (AttributeError, pg.midi.MidiException) as MidiException:
            print(MidiException, "\nNo MIDI controller detected.")

    def open_upload_toplevel(self):
        return UploadToplevel(self)

    def open_record_toplevel(self):
        return RecorderToplevel(self)

    def open_piano_toplevel(self):
        return PianoManagerToplevel(self)

    def midi_handle(self):
        if self.midi_input.poll():
            midi_events = self.midi_input.read(1)[0]
            print(midi_events)
            if midi_events[0][0] == 144:
                midi_press(midi_events, self.parent.keys)
            elif midi_events[0][0] == 128:
                midi_release(midi_events, self.parent.keys)
        self.after(1, self.midi_handle)

    def create_key(self, img, key):
        y_coord = self.height - 200  # decrease 200px so that white key image fits perfectly
        key_image = tk.PhotoImage(file=img)
        label = tk.Label(self, image=key_image, bd=0)
        label.image = key_image
        label.place(x=key[0], y=y_coord)
        label.name = key[1]
        label.x = key[0]
        label.bind('<Button-1>', button_press)
        label.bind('<ButtonRelease-1>', label_release)
        return label

    def init_ui(self):
        keys = [
            [0, 'C'],
            [50, 'D'],
            [100, 'E'],
            [150, 'F'],
            [200, 'G'],
            [250, 'A'],
            [300, 'B'],
            [35, 'C#'],
            [85, 'D#'],
            [185, 'F#'],
            [235, 'G#'],
            [285, 'A#'],
            [350, 'C'],
            [400, 'D'],
            [450, 'E'],
            [500, 'F'],
            [550, 'G'],
            [600, 'A'],
            [650, 'B'],
            [385, 'C#'],
            [435, 'D#'],
            [535, 'F#'],
            [585, 'G#'],
            [635, 'A#']
        ]

        for key in keys:
            if len(key[1]) == 1:
                img = '../pictures/white_key.gif'
                key.append(self.create_key(img, key))
            elif len(key[1]) > 1:
                img = '../pictures/black_key.gif'
                key.append(self.create_key(img, key))

        menu_frame = tk.Frame(self, bd=3, bg='darkgray', height=50, width=self.width)
        menu_frame.place(x=0, y=self.height - 250)

        file_btn = tk.Button(menu_frame, text='Import File', bd=2, relief='raised',
                             command=lambda: self.open_upload_toplevel())
        file_btn.name = 'file_btn'
        file_btn.place(x=0, y=0, relwidth=1.0 / 3.0, relheight=menu_frame.winfo_height())

        record_btn = tk.Button(menu_frame, text='Record External Audio', bd=2, relief='raised',
                               command=lambda: self.open_record_toplevel())
        record_btn.name = 'record_btn'
        record_btn.place(relx=1.0 / 3.0, y=0, relwidth=1.0 / 3.0, relheight=menu_frame.winfo_height())

        img = tk.PhotoImage(file='../pictures/red_button.gif')
        record_btn = tk.Label(self, image=img, bd=1)
        record_btn.image = img
        record_btn.name = 'rec_button'
        record_btn.bind('<Button-1>', record_on_off)
        record_btn.place(x=700, y=self.height - 200)

        img = tk.PhotoImage(file='../pictures/green_button.gif')
        play_btn = tk.Label(self, image=img, bd=1)
        play_btn.image = img
        play_btn.name = 'play_button'
        play_btn.bind('<Button-1>', play_back)
        play_btn.bind('<ButtonRelease-1>', label_release)
        play_btn.place(x=700, y=self.height - 150)

        octave_up_frame = tk.Frame(menu_frame, width=25, height=50, bg='darkgray')
        octave_up_frame.pack_propagate(0)
        octave_up_frame.place(relx=5.0 / 6.0, y=0, relwidth=1.0 / 6.0, relheight=menu_frame.winfo_height())

        octave_up_btn = tk.Button(octave_up_frame, text="Oct\n+", bd=1, relief='raised',
                                  height=octave_up_frame['height'])
        octave_up_btn.name = 'octave_up'
        octave_up_btn.bind('<Button-1>', lambda event: increment_octave())
        octave_up_btn.pack(fill=tk.BOTH)

        octave_down_frame = tk.Frame(menu_frame, width=25, height=50, bg='darkgray')
        octave_down_frame.pack_propagate(0)
        octave_down_frame.place(relx=2.0 / 3.0, y=0, relwidth=1.0 / 6.0, relheight=menu_frame.winfo_height())

        octave_down_btn = tk.Button(octave_down_frame, text='Oct\n-', bd=1, relief='raised',
                                    height=octave_down_frame['height'])
        octave_down_btn.name = 'octave_down'
        octave_down_btn.bind('<Button-1>', lambda event: decrement_octave())
        octave_down_btn.pack(fill=tk.BOTH)

        transcribe_frame = tk.Frame(self, width=50, height=100, bg='darkgray')
        transcribe_frame.pack_propagate(0)
        transcribe_frame.place(x=700, y=self.height - 100)

        transcribe_btn = tk.Button(transcribe_frame, text='Convert\nPiano\nRoll', bd=2, relief='raised',
                                   height=transcribe_frame['height'], command=lambda: self.open_piano_toplevel())
        transcribe_btn.pack()

        self.parent.keys = keys
        self.parent.bind('z', lambda event: decrement_octave())
        self.parent.bind('x', lambda event: increment_octave())
        self.parent.bind('<KeyPress>', key_press)
        self.parent.bind('<KeyRelease>', key_release)
        self.pack(fill=tk.BOTH, expand=True)


def main():
    root = tk.Tk()
    app = PianoFollower(root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()
