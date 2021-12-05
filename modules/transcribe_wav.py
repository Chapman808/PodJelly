from os import path, mkdir
from os.path import exists
import argparse
import speech_recognition as sr
from pydub import AudioSegment
from modules import chunk_wav
from modules.model.transcript_chunk import TranscriptChunk
from modules.connection import mongo_client



#transcribes wav file and returns str of transcript
def transcribeWav(wavFile : str) -> str:
    chunks = chunk_wav.getChunksFromWav(wavFile)
    print("okay, doing the fun stuff now. Transcribing audio chunks...")
    # use the audio file as the audio source  
    r = sr.Recognizer()
    transcript = ""
    transcriptChunks = []
    for count, chunk in enumerate(chunks):
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

def transcribeWavToDb (wavFile: str):
    client = mongo_client.getConfiguredMongoClient()
    db = client.podJelly
    db_transcripts = db.transcripts
    chunks = transcribeWav(wavFile)
    for chunk in chunks:
        db_transcripts.insert_one(chunk.__dict__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--send', help='send transcripts to configured db.', action='store_true')
    args = parser.parse_args()

    AUDIO_FILE = './files/wav/harvard.wav'

    if args.send:
        transcribeWavToDb(AUDIO_FILE)
    else:
        chunks = transcribeWav(AUDIO_FILE)
        for chunk in chunks:
            print(chunk)

    '''
def transcribeWavToDisk (wavFile: str):
    transcriptDir = "./transcripts/"
    baseFileName = wavFile.rsplit(".", 1)[0].split("/")[-1]    #just the 'name' portion of the filename
    outputFilename = transcriptDir + baseFileName + '.txt'
    print('transcript filename: ' + outputFilename)
    with open (outputFilename, 'w') as transcript:
        audio_out = transcribeWav(wavFile)
        print(audio_out)
        transcript.write(audio_out)
'''
'''
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
'''