#credit: https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python

# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

from model.audio_chunk import AudioChunk

# create a speech recognition object
r = sr.Recognizer()

'''
splits the audio file into chunks
returns list of speech_recognition.AudioFile objects
'''
def getChunksFromWav(path) -> list: 
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    print("splitting audio... this might take a while...")
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk into an AudioChunk object
    processedChunks = []
    timestamp = 0
    for i, audio_chunk in enumerate(chunks, start=1):
        timestamp += audio_chunk.duration_seconds
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # read the newly created wav into an AudioChunk object (stores timestamp and other metadata)
        with sr.AudioFile(chunk_filename) as source:
            episodeName = path.split("/")[-1].split(".")[0]
            processedChunks.append(AudioChunk(source, int(timestamp), episodeName))
    return processedChunks

if __name__ == '__main__':
    AUDIO_FILE = './files/wav/demo.wav'
    audioChunks = getChunksFromWav(AUDIO_FILE)
    for chunk in audioChunks:
        print(chunk)