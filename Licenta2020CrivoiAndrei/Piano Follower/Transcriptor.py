from tkinter import filedialog

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from music21.tempo import MetronomeMark
from music21.note import Note, Rest
from music21.stream import Stream
from music21 import midi
from music21 import metadata
from music21 import instrument
from music21.duration import DurationException
plt.rc("figure", figsize=(16, 8))


def second_to_quarter(duration, tempo):
    return tempo * duration / 60


def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class Transcriptor:
    def __init__(self, path):
        self.path = path
        self.nfft = 2048
        self.overlap = 0.5
        self.hop_length = int(self.nfft * (1 - self.overlap))
        self.n_bins = 72
        self.mag_exp = 4
        self.pre_post_max = 6
        self.threshold = -61

        self.audio_sample, self.sr = self.load()
        self.cqt = self.compute_cqt()
        self.thresh_cqt = self.compute_thresholded_cqt(self.cqt)

        self.onsets = self.compute_onset(self.thresh_cqt)

        self.tempo, self.beats, self.mm = self.estimate_tempo()

        self.music_info = np.array([
            self.estimate_pitch_and_notes(i)
            for i in range(len(self.onsets[1]) - 1)
        ])
        self.note_info = list(self.music_info[:, 2])

        self.stream = Stream()

    def load(self):
        x, sr = librosa.load(self.path, sr=None, mono=True)
        print("x Shape =", x.shape)
        print("Sample rate =", sr)
        print("Audio Length in seconds = {} [s]" .format(x.shape[0] / sr))
        return x, sr

    def compute_cqt(self):
        c = librosa.cqt(self.audio_sample, sr=self.sr, hop_length=self.hop_length,
                        fmin=None, n_bins=self.n_bins, res_type='fft')
        c_mag = librosa.magphase(c)[0] ** self.mag_exp
        cdb = librosa.amplitude_to_db(c_mag, ref=np.max)
        return cdb

    def compute_thresholded_cqt(self, cqt):
        new_cqt = np.copy(cqt)
        new_cqt[new_cqt < self.threshold] = -120
        return new_cqt

    def compute_onset_env(self, cqt):
        return librosa.onset.onset_strength(S=cqt, sr=self.sr, aggregate=np.mean,
                                            hop_length=self.hop_length)

    def compute_onset(self, cqt):
        onset_env = self.compute_onset_env(cqt)
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env,
                                                  sr=self.sr, units='frames',
                                                  hop_length=self.hop_length,
                                                  pre_max=self.pre_post_max,
                                                  post_max=self.pre_post_max,
                                                  backtrack=False)

        onset_boundaries = np.concatenate([[0], onset_frames, [cqt.shape[1]]])
        onset_times = librosa.frames_to_time(onset_boundaries, sr=self.sr,
                                             hop_length=self.hop_length)

        return [onset_times, onset_boundaries, onset_env]

    def display_cqt_tuning(self):
        plt.figure()
        librosa.display.specshow(self.thresh_cqt, sr=self.sr, hop_length=self.hop_length,
                                 x_axis='time', y_axis='cqt_note', cmap='coolwarm')
        plt.ylim([librosa.note_to_hz('B2'), librosa.note_to_hz('B5')])
        plt.vlines(self.onsets[0], 0, self.sr / 2, color='k', alpha=0.8)
        plt.title("CQT")
        plt.colorbar()
        plt.show()

    def estimate_tempo(self):
        tempo, beats = librosa.beat.beat_track(y=None, sr=self.sr,
                                               onset_envelope=self.onsets[2],
                                               hop_length=self.hop_length,
                                               start_bpm=120.0,
                                               tightness=100.0,
                                               trim=True,
                                               units='frames')
        tempo = int(2 * round(tempo / 2))
        mm = MetronomeMark(referent='quarter', number=tempo)
        return tempo, beats, mm

    def generate_note(self, f0_info, n_duration, round_to_sixteenth=True):
        f0 = f0_info[0]
        a = remap(f0_info[1], self.cqt.min(), self.cqt.max(), 0, 1)
        duration = librosa.frames_to_time(n_duration, sr=self.sr, hop_length=self.hop_length)
        note_duration = 0.02 * np.around(duration / 2 / 0.02)  # Round to 2 decimal places for music21 compatibility
        midi_duration = second_to_quarter(duration, self.tempo)
        midi_velocity = int(round(remap(f0_info[1], self.cqt.min(), self.cqt.max(), 80, 120)))
        if round_to_sixteenth:
            midi_duration = round(midi_duration * 16) / 16
        try:
            if f0 is None:
                midi_note = None
                note_info = Rest(type=self.mm.secondsToDuration(note_duration).type)
                f0 = 0
            else:
                midi_note = round(librosa.hz_to_midi(f0))
                note = Note(librosa.midi_to_note(midi_note), type=self.mm.secondsToDuration(note_duration).type)
                note.volume.velocity = midi_velocity
                note_info = [note]
        except DurationException:
            if f0 is None:
                midi_note = None
                note_info = Rest(type='32nd')
            else:
                midi_note = round(librosa.hz_to_midi(f0))
                note = Note(librosa.midi_to_note(midi_note),
                            type='16th')
                note.volume.velocity = midi_velocity
                note_info = [note]

        midi_info = [midi_note, midi_duration, midi_velocity]
        n = np.arange(librosa.frames_to_samples(n_duration, hop_length=self.hop_length))
        sine_wave = a * np.sin(2 * np.pi * f0 * n / float(self.sr))
        return [sine_wave, midi_info, note_info]

    def estimate_pitch(self, segment, threshold):
        freqs = librosa.cqt_frequencies(n_bins=self.n_bins, fmin=librosa.note_to_hz('C1'),
                                        bins_per_octave=12)
        if segment.max() < threshold:
            return [None, np.mean((np.amax(segment, axis=0)))]
        else:
            f0 = int(np.mean((np.argmax(segment, axis=0))))
        return [freqs[f0], np.mean((np.amax(segment, axis=0)))]

    def estimate_pitch_and_notes(self, i):
        n0 = self.onsets[1][i]
        n1 = self.onsets[1][i + 1]
        f0_info = self.estimate_pitch(np.mean(self.cqt[:, n0:n1], axis=1), threshold=self.threshold)
        return self.generate_note(f0_info, n1 - n0)

    def transcript(self):
        self.stream.append(self.mm)
        electric_guitar = instrument.fromString('grand piano')
        electric_guitar.midiChannel = 0
        electric_guitar.midiProgram = 1
        self.stream.append(electric_guitar)
        self.stream.insert(0, metadata.Metadata())
        self.stream.metadata.title = self.path.split('/')[-1]
        for note in self.note_info:
            self.stream.append(note)
        key = self.stream.analyze('key')
        print(key.name)
        # Insert Key to Stream
        self.stream.insert(0, key)

        # self.stream.show('text')

    def show_stream(self):
        self.stream.show()

    def convert_stream_to_midi(self):
        midi_file = midi.translate.streamToMidiFile(self.stream)
        midi_file.open('midi_scale.mid', 'wb')
        midi_file.write()
        midi_file.close()

        midi_file = midi.translate.streamToMidiFile(self.stream)
        filename = filedialog.asksaveasfile(initialdir="/", title="Save Midi File",
                                            filetypes=('midi files', ('*.mid', '*.midi')))
        midi_file.open(filename.name, 'wb')
        midi_file.write()
        midi_file.close()


def main():
    tr = Transcriptor('../samples/sweet_child.wav')
    tr.display_cqt_tuning()
    tr.transcript()


if __name__ == '__main__':
    main()
