import argparse
from extract_rss_files import getFeedFiles
from file_downloader import downloadFiles
#if run as main, creates list of urls based on the given RSS feed and writes it to a file
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('feed', metavar='f', type=str, help='xml rss feed file', default='feed')
    args = parser.parse_args()
    
    fileNames = getFeedFiles(args.feed)
    reducedFileNames = fileNames[:1]
    downloadFiles(reducedFileNames)
