import argparse
import urllib.request
import uuid
import sys
import os
import urllib.parse

#takes list of file urls and downloads them to ./downloads directory
def downloadFiles(files : list):
    if (not os.path.exists('downloads')):
        os.mkdir('downloads')
    newFilenames = []
    for file in files:
        filename = urllib.parse.urlsplit(file).path.split('/')[-1]
        urllib.request.urlretrieve(file, 'downloads/' + filename)
        newFilenames.append('./downloads/' + filename)
    return newFilenames
#if run as main, downloads given list of files
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fileList', metavar='f', type=str, help='file list of urls to download', default='urls')
    args = parser.parse_args()
    urls = []
    with open(args.fileList, 'r') as inFile:
        urls = inFile.readlines()
    downloadFiles(urls)
