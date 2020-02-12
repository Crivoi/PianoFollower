import mido
import music21.midi as midi
from music21 import converter
from ast import literal_eval


class MidiManager:
    def __init__(self, path, midi_file=False):
        self.path = path
        if midi_file is False:
            self.midi_file = mido.MidiFile()
            self.midi_track = mido.MidiTrack()
            self.m21_file = midi.MidiFile()
            self.midi_file.tracks.append(self.midi_track)
            self.midi_track.append(mido.Message('program_change', program=1, time=0))
        else:
            self.midi_file = mido.MidiFile(self.path)
            self.m21_file = midi.MidiFile()

    def midi_msg_to_mido_msg(self):
        with open(self.path) as mf:
            time = 0
            for line in mf.readlines():
                midi_msg = literal_eval(line)
                old_time = time
                time = int(midi_msg[1])
                if old_time == 0:
                    delta_time = 0
                else:
                    delta_time = round((time - old_time) / 16) * 16
                    print(delta_time)
                if midi_msg[0][0] == 144:
                    self.midi_track.append(mido.Message('note_on', note=midi_msg[0][1],
                                                        velocity=midi_msg[0][2],
                                                        time=delta_time))
                elif midi_msg[0][0] == 128:
                    self.midi_track.append(mido.Message('note_off', note=midi_msg[0][1],
                                                        velocity=midi_msg[0][2],
                                                        time=delta_time))

    def save_midi(self, filename):
        self.midi_file.save(filename)

    def convert_midi_to_stream(self, path):
        self.m21_file.open(path, 'rb')
        self.m21_file.read()
        self.m21_file.close()
        # stream = midi.translate.midiFileToStream(self.m21_file)
        stream = converter.parse(path)
        # stream.show('text')
        stream.show()


def main():
    pass


if __name__ == '__main__':
    main()
