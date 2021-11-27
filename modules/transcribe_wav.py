from os import path, mkdir
from os.path import exists

import speech_recognition as sr
from pydub import AudioSegment
from chunk_wav import getChunksFromWav
from model.transcript_chunk import TranscriptChunk
#Credit to: https://pythonbasics.org/transcribe-audio/
#conversion to WAV

#converts given filename to wav and outputs the wav file to the outputdir. returns output filename
def writeMp3ToWav(filename):
    outputDir = './wav/'
    if (not path.exists(outputDir)):
        mkdir(outputDir)
    baseFilename = filename.rsplit(".", 1)[0].split("/")[-1]    #just the 'name' portion of the filename
    outputFilename = baseFilename + ".wav"
    if (not exists(outputDir + outputFilename)):
        audioSegment = AudioSegment.from_mp3(filename)
        audioSegment.export(outputDir + outputFilename, format="wav")
    return outputDir + outputFilename

#transcribes wav file and returns str of transcript
def transcribeWav(wavFile : str) -> str:
    chunks = getChunksFromWav(wavFile)
    print("okay, doing the fun stuff now. Transcribing audio chunks...")
    # use the audio file as the audio source  
    r = sr.Recognizer()
    transcript = ""
    count = 0
    transcriptChunks = []
    for chunk in chunks:
        count += 1
        audioFile = chunk.audioFile
        with audioFile as source:
            percentComplete = str(count * 100 // len(chunks))
            print("Progress " + percentComplete + "%", end="\r", flush=True)
            audio = r.record(source)
            text = _transcribe_chunk(audio,r)
            if text: 
                transcriptChunks.append(TranscriptChunk(text, chunk.timestampSeconds, chunk.episode))
                transcript += text
    return transcriptChunks

def _transcribe_chunk (audio, r): 
    transcript = None
    try:                                    
        transcript = r.recognize_google(audio) + " "
    except: pass
    return transcript

def transcribeWavToDisk (wavFile: str):
    transcriptDir = "./transcripts/"
    baseFileName = wavFile.rsplit(".", 1)[0].split("/")[-1]    #just the 'name' portion of the filename
    outputFilename = transcriptDir + baseFileName + '.txt'
    print('transcript filename: ' + outputFilename)
    with open (outputFilename, 'w') as transcript:
        audio_out = transcribeWav(wavFile)
        print(audio_out)
        transcript.write(audio_out)



if __name__ == '__main__':
    AUDIO_FILE = './files/wav/harvard.wav'
    chunks = transcribeWav(AUDIO_FILE)
    for chunk in chunks:
        print(chunk)
    