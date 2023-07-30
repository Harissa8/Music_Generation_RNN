import os
import music21 as m21
import json as js
import numpy as np
import tensorflow.keras as keras
KERN_DATASET_PATH = "mydata\erk"
SAVE_DIR = "dataset"
SINGLE_FILE_DATASET = "file_dataset"
MAPPING_PATH = "mapping.json"
SEQUENCE_LENGTH = 64
# durations are expressed in quarter length
ACCEPTABLE_DURATIONS = [
    0.25, # 16th note
    0.5, # 8th note
    0.75,
    1.0, # quarter note
    1.5,
    2, # half note
    3,
    4 # whole note
]


def load_songs_in_kern(dataset_path):

    songs = []

    # go through all the files in dataset and load them with music21
    for path, subdirs, files in os.walk(dataset_path):
        for file in files:

            # consider only kern files
            if file[-3:] == "krn":
                song = m21.converter.parse(os.path.join(path, file))
                songs.append(song)
    return songs


def has_acceptable_durations(song, acceptable_durations):

    for note in song.flat.notesAndRests:
        if note.duration.quarterLength not in acceptable_durations:
            return False
    return True


def transpose(song):

#note

    # get key from the song
    parts = song.getElementsByClass(m21.stream.Part)
    measures_part0 = parts[0].getElementsByClass(m21.stream.Measure)
    key = measures_part0[0][4]

    # estimate key using music21
    if not isinstance(key, m21.key.Key):
        key = song.analyze("key")

    # get interval for transposition. E.g., Bmaj -> Cmaj
    if key.mode == "major":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
    elif key.mode == "minor":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

    # transpose song by calculated interval
    tranposed_song = song.transpose(interval)
    return tranposed_song


def encode_song(song, time_step=0.25):

    encoded_song = []

    for event in song.flat.notesAndRests:

        # handle notes
        if isinstance(event, m21.note.Note):
            symbol = event.pitch.midi # 60
        # handle rests
        elif isinstance(event, m21.note.Rest):
            symbol = "r"

        # convert the note/rest into time series notation
        steps = int(event.duration.quarterLength / time_step)
        for step in range(steps):

            # if it's the first time we see a note/rest, let's encode it. Otherwise, it means we're carrying the same
            # symbol in a new time step
            if step == 0:
                encoded_song.append(symbol)
            else:
                encoded_song.append("_")

    # cast encoded song to str
    encoded_song = " ".join(map(str, encoded_song))

    return encoded_song

def preprocess(dataset_path):
    # load folk songs
    print("Loading songs...")
    songs = load_songs_in_kern(dataset_path)
    print(f"Loaded {len(songs)} songs.")

    for i, song in enumerate(songs):

        # filter out songs that have non-acceptable durations
        if not has_acceptable_durations(song, ACCEPTABLE_DURATIONS):
            continue

        # transpose songs to Cmaj/Amin
        song = transpose(song)

        # encode songs with music time series representation
        encoded_song = encode_song(song)

        # save songs to text file
        save_path = os.path.join(SAVE_DIR, str(i))
        with open(save_path, "w") as fp:
            fp.write(encoded_song)

        if i % 10 == 0:
            print(f"Song {i} out of {len(songs)} processed")


def load(file_path):
    with open(file_path, "r") as fp:
        song = fp.read()
    return song

def create_single_file_dataset(dataset_path,file_dataset_path,sequence_length):
    new_song_delimiter = "/ " * sequence_length
    songs = ""
    #load encoded songs and add delimiters
    for path, _, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(path, file)
            song=load(file_path)
            songs = songs + song + " " + new_song_delimiter
    songs = songs[:-1]
    # save string that contains all dataset
    with open(file_dataset_path, "w") as fp:
        fp.write(songs)
    return songs
 #create dataset
def create_mapping(songs, mapping_path):
    mappings ={} # dict
 # create my own vocab(all data we have in dataset) to ->
    songs = songs.split()
    vocabulary = list(set(songs))
    # create mapping
    for i, symbol in enumerate(vocabulary):
        mappings[symbol] = i



 #<-be saved to jason file
    with open(mapping_path, "w") as fp :
        js.dump(mappings, fp, indent=4)


def convert_songs_to_int(songs):
    int_songs = []
    # load mapping
    with open(MAPPING_PATH, "r") as fp:
        mappings = js.load(fp)
    # cast songs strings to list
    songs = songs.split()
    # map songs to int
    for symbol in songs:
        int_songs.append(mappings[symbol])
    return int_songs


def generating_training_sequences(sequence_length):
    # convert or map songs to int
    songs = load(SINGLE_FILE_DATASET)
    int_songs = convert_songs_to_int(songs)

    #generate the training sequences
    inputs = []
    targets= []
    num_sequences = len (int_songs) - sequence_length #ig 64
    for i in range(num_sequences):
        inputs.append(int_songs[i:i+sequence_length])
        targets.append(int_songs[i+sequence_length])

   #one-hot encode the sequence
   #inputs:(# of sequences , sequence length)
    vocabulary_size = len(set(int_songs))
    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size)
    targets = np.array(targets)
    return inputs, targets
def main():
    preprocess(KERN_DATASET_PATH)
    songs = create_single_file_dataset(SAVE_DIR, SINGLE_FILE_DATASET, SEQUENCE_LENGTH)
    create_mapping(songs,MAPPING_PATH)
    #inputs, targets = generating_training_sequences(SEQUENCE_LENGTH)




if __name__ == "__main__":
    main()


