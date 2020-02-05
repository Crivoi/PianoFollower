import pyaudio
import time
import wave

from Transcriptor import Transcriptor


class AudioRecorder:
    def __init__(self, path):
        self.chunk = 1024 * 2
        self.format = pyaudio.paInt16
        self.channels = 1
        self.sr = 44100
        self.recording = False
        self.frames = []
        self.path = path

        self.transcriptor = None

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.sr,
            input=True,
            output=True,
            frames_per_buffer=self.chunk
        )

    def init_rec(self):
        print('stream started at time {}'.format(time.time()))
        self.recording = True
        while self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_rec(self):
        print('stream stopped at time {}'.format(time.time()))
        self.recording = False

    def export_wav(self):
        if len(self.frames) == 0:
            pass
        else:
            with wave.open(self.path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.format))
                wf.setframerate(self.sr)
                wf.writeframes(b''.join(self.frames))

                self.transcriptor = Transcriptor(self.path)
                self.exit_app()

    def exit_app(self):
        print('stream closed')
        self.p.close(self.stream)


if __name__ == '__main__':
    AudioRecorder("output.wav")
