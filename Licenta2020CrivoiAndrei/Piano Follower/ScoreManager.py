import music21 as m21
from tkinter import filedialog

from ScoreComparerToplevel import ScoreComparerToplevel


class ScoreManager:
    def __init__(self, path):
        if type(path) is str:
            self.path = path
            self.score_obj = m21.converter.parse(path)
        elif type(path) is m21.stream.Stream:
            self.score_obj = path
        else:
            raise(TypeError, 'Score Manager Unsupported Type')

    def show(self):
        self.score_obj.show()

    def show_text(self):
        self.score_obj.show('text')

    def convert_stream_to_midi(self):
        midi_file = m21.midi.translate.streamToMidiFile(self.score_obj)
        filename = filedialog.asksaveasfilename(initialdir="/", title="Save Midi File",
                                                filetypes=('midi files', ('*.mid', '*.midi')))
        midi_file.open(filename, 'wb')
        midi_file.write()
        midi_file.close()

    def compare(self, filename):
        stream1 = []
        stream2 = []

        score = m21.converter.parse(filename)

        for note in self.score_obj.flat.notes:
            if type(note) == m21.note.Note:
                stream1.append(str(note.pitch) + ' ' + str(note.offset))
            elif type(note) == m21.chord.Chord:
                for pitch in note.pitches:
                    stream1.append(str(pitch) + ' ' + str(note.offset))
        for note in score.flat.notes:
            if type(note) == m21.note.Note:
                stream2.append(str(note.pitch) + ' ' + str(note.offset))
            elif type(note) == m21.chord.Chord:
                for pitch in note.pitches:
                    stream2.append(str(pitch) + ' ' + str(note.offset))

        return ScoreComparerToplevel(stream1, stream2)


def main():
    s = ScoreManager('C:/users/Lenovo/Desktop/sc.mxl')
    s.compare('sc.mxl')


if __name__ == '__main__':
    main()
