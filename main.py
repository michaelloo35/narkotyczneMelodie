import argparse
from melodies_generator import MidiGenerator

if __name__ == '__main__':

    generator = MidiGenerator()
    generator.generate('test')
    # parser = argparse.ArgumentParser(description='Simple music generator based on Chord Progressions. Press ctrl+c to'
    #                                             'interrupt playback')
    # parser.add_argument('-n', '--name', help="output file name", required=True)
    # parser.add_argument('-t', '--time', help="track length grade, between 1 (min) and 10 (max)", required=False)
    # parser.add_argument('-m', '--mood', help='sad / happy', required=False)
    # parser.add_argument('-o', '--out', help='output directory, defaults to current dir', required=False)
    # args = vars(parser.parse_args())
