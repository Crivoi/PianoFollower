import music21 as m21
import sys

# STREAM TO MIDI

if(sys.argv[1] == '1'):
    stream = m21.stream.Stream()

    c4 = m21.note.Note('C4')
    d4 = m21.note.Note('D4')
    e4 = m21.note.Note('E4')
    f4 = m21.note.Note('F4')
    g4 = m21.note.Note('G4')
    a4 = m21.note.Note('A4')
    b4 = m21.note.Note('B4')
    c5 = m21.note.Note('C5')

    cMajor = [c4, d4, e4, f4, g4, a4, b4, c5]

    stream.append(cMajor)

    midi_file = m21.midi.translate.streamToMidiFile(stream)
    midi_file.open('midi_scale.mid', 'wb')
    midi_file.write()
    midi_file.close()

# MIDI TO STREAM

elif sys.argv[1] == '2':
    midi_file = m21.midi.MidiFile()
    midi_file.open('midi_scale.mid', 'rb')
    midi_file.read()
    midi_file.close()

    stream = m21.midi.translate.midiFileToStream(midi_file)
    stream.show()
