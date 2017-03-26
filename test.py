import argparse
import os
from time import sleep
import pygame
from pathlib import Path
from random import randrange
from midiutil import MIDIFile


class MusicGenerator(object):
    def __init__(self, name, mood, path, time):
        self._name = name
        self._mood = mood
        self._path = path
        self._time = time
        self.generate()

    def generate(self):
        # degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
        track = 0
        channel = 0
        time = 0  # In beats
        duration = 1  # In beats
        tempo = randrange(80, 120)  # In BPM
        volume = 100  # 0-127, as per the MIDI standard

        octave = randrange(4, 7) * 12

        print(octave)

        # following lists all make for a fully-fledged chord progression mixer including circle of the fifths

        majorMap = [[9, 11, 1, 2, 4, 6, 8], [11, 1, 3, 4, 6, 8, 10], [0, 2, 4, 5, 7, 9, 11], [2, 4, 6, 7, 9, 11, 1],
                    [4, 6, 8, 9, 11, 1, 3], [5, 7, 9, 11, 0, 2, 4], [7, 9, 11, 0, 2, 4, 6], [1, 3, 5, 6, 8, 10, 12],
                    [6, 8, 10, 11, 1, 3, 5], [8, 10, 0, 1, 3, 5, 7], [10, 0, 2, 3, 5, 7, 9], [-1, 1, 3, 4, 6, 8, 10],
                    [1, 3, 5, 6, 8, 10, 0], [3, 5, 7, 8, 10, 0, 2], [6, 8, 10, -1, 1, 3, 5]]

        minorMap = [[9, 11, 1, 2, 4, 6, 8], [11, 1, 3, 4, 6, 8, 10], [0, 2, 4, 5, 7, 9, 11], [], [], [], []]

        moodSadMap = [[0, 3, 4, 4], [0, 0, 3, 5], [0, 5, 3, 4], [0, 5, 1, 4]]
        moodUpbeatMap = [[0, 3, 0, 4], [3, 4, 3], [0, 2, 3, 5], [0, 3, 4]]

        majorWheel = [2, 6, 3, 0, 4, 1, 8, 12, 9, 13, 10, 5]
        minorWheel = [0, 4, 1, 8, 7, 14, 13, 10, 5, 0, 6, 3]

        degrees = []
        sadMood = randrange(0, 4)
        key = randrange(0, 6)
        #print(key)

        for note in moodUpbeatMap[sadMood]:
            if note == 0:
                degrees.append(majorMap[key][note] + octave)
            else:
                degrees.append(majorMap[key][note] + octave)

        indexOfKey = majorWheel.index(key)

        key = majorWheel[(indexOfKey + 1) % 12]

        # print(key)

        for note in moodUpbeatMap[sadMood]:
            degrees.append(majorMap[key][note] + octave)

        for note in moodUpbeatMap[sadMood]:
            degrees.append(majorMap[key][note] + octave)

        key = majorWheel[indexOfKey - 1]

        # print(key)

        for note in moodUpbeatMap[sadMood]:
            degrees.append(majorMap[key][note] + octave)

        for note in moodUpbeatMap[sadMood]:
            degrees.append(majorMap[key][note] + octave)

        key = minorWheel[indexOfKey]

        for note in moodUpbeatMap[sadMood]:
            degrees.append(majorMap[key][note] + octave)

        key = majorWheel[indexOfKey]

        for note in moodUpbeatMap[sadMood]:
            degrees.append(majorMap[key][note] + octave)

        # print(degrees)

        MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track
        MyMIDI.addProgramChange(track, channel, time, randrange(0, 128))
        # automatically created)
        MyMIDI.addTempo(track, time, tempo)


        for pitch in degrees:
            MyMIDI.addNote(track, channel, pitch, time, duration, volume)
            time = time + 1

        MyMIDI.addNote(track, channel, 0, time, duration, 0)

        # Create in the same dir as the app
        if self._path is None:
            my_path = str(self._name)
            with open(my_path, "wb") as output_file:
                MyMIDI.writeFile(output_file)

        else:
            # Create dir if it doesn't exist beforehand
            if not os.path.exists(self._path):
                os.makedirs(self._path)
            if str(self._path).endswith('/'):
                my_path = Path(str(self._path) + str(self._name)).absolute()
                with open(my_path, "w+b") as output_file:
                    MyMIDI.writeFile(output_file)
            else:
                my_path = Path(str(self._path) + '/' + str(self._name)).absolute()
                with open(my_path, "w+b") as output_file:
                    MyMIDI.writeFile(output_file)

        print(my_path)
        try:
            self.play_music(my_path)

        except KeyboardInterrupt:
            pygame.mixer.music.fadeout(1000)
            sleep(1)
            pygame.mixer.music.stop()
            raise SystemExit


    def play_music(self, output):
        freq = 44100  # audio CD quality
        bitsize = -16  # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 4096  # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        clock = pygame.time.Clock()
        pygame.mixer.music.load(str(output))

        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple music generator based on Chord Progressions. Press ctrl+c to '
                                                 'interrupt playback')
    parser.add_argument('-n', '--name', help="output file name", required=True)
    parser.add_argument('-t', '--time', help="track length grade, between 1 (min) and 10 (max)", required=False)
    parser.add_argument('-m', '--mood', help='sad / happy', required=False)
    parser.add_argument('-o', '--out', help='output directory, defaults to current dir', required=False)
    args = vars(parser.parse_args())

    mood = ''
    path = ''
    time = 3
    if 'time' in args and args['time'] is not None:
        time = int(args['time'])
    if 'mood' in args:
        mood = args['mood']
    if 'out' in args:
        path = args['out']

    gen = MusicGenerator(args['name'], mood, path, time)

