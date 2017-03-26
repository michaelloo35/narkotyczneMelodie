from miditime.miditime import MIDITime


class MidiGenerator:

    def __init__(self):
        self.bpm = 120

    @property
    def bpm(self):
        return self.bpm

    @bpm.setter
    def bpm(self, x):
        self.bpm = x

    def generate(self, file_name):
        # Instantiate the class with a tempo (120bpm is the default) and an output file destination.
        mymidi = MIDITime(self.bpm, './output/' + file_name + '.midi')

        # Create a list of notes. Each note is a list: [time, pitch, velocity, duration]
        midinotes = [
            [0, 60, 127, 0]  # At 0 beats (the start), Middle C with velocity 127, for 3 beats
        ]

        # Add a track with those notes
        mymidi.add_track(midinotes)

        # Output the .mid file
        mymidi.save_midi()
