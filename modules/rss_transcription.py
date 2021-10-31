import argparse
from extract_rss_files import getFeedFiles
from file_downloader import downloadFiles
from transcribe_wav import transcribeWavToDisk, writeMp3ToWav
from transcribe_wav import transcribeWav
#if run as main, creates list of urls based on the given RSS feed and writes it to a file
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('feed', metavar='f', type=str, help='xml rss feed file', default='feed')
    args = parser.parse_args()

    print('extracting file urls from RSS feed...')
    fileUrls = getFeedFiles(args.feed)
    reducedFileNames = fileUrls[:1]

    print('downloading mp3 files...')
    mp3Filenames = downloadFiles(reducedFileNames)
    first_mp3 = mp3Filenames[0]
    print('file to transcribe: ' + first_mp3)

    print('converting mp3 to wav...')
    wavFilename = writeMp3ToWav(first_mp3, './wav/')
    print('wav filename: ' + wavFilename)

    print('chunking and transcribing wav...')
    transcription = transcribeWavToDisk(wavFilename)

