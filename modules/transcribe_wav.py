from os import path, mkdir
from os.path import exists

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from chunk_wav import get_large_audio_transcription
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
def transcribeWav(wavFile : str):
    chunks = get_large_audio_transcription(wavFile)
    print("okay, doing the fun stuff now. Transcribing audio chunks...")
    # use the audio file as the audio source  
    r = sr.Recognizer()
    # r.energy_threshold = 1000
    r.pause_threshold = .5
    transcript = ""
    count = 0
    for chunk in chunks:
        count += 1
        with chunk as source:
            percentComplete = str(count * 100 // len(chunks))
            print("Progress " + percentComplete + "%", end="\r", flush=True)
            audio = r.record(source)
            text = transcribe_chunk(audio,r)
            if text: transcript += text
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

def transcribe_chunk (audio, r): 
    transcript = None
    try:                                    
        transcript = r.recognize_google(audio) + " "
    except: pass
    return transcript

if __name__ == '__main__':
    outputDir = "./wav/"
    transcriptDir = "./transcripts/"
    AUDIO_FILE = './wav/demo.wav'
    transcribeWavToDisk(AUDIO_FILE)
    