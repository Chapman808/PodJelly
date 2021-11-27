#!/usr/bin/python3

import argparse
import xml.etree.ElementTree as ET

#takes in xml filename, and returns a list of audio urls
def getFeedFiles(feed) -> list:
    try:
        tree = ET.parse(feed)
        xmlRoot = tree.getroot()
    except:
        print('could not read rss feed file')
        exit(0)

    fileList = []
    for x in xmlRoot.findall('.//enclosure'):
        fileList.append(x.attrib.get('url'))

    return fileList

#if run as main, creates list of urls based on the given RSS feed and writes it to a file
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('feed', metavar='f', type=str, help='xml rss feed file', default='feed')
    args = parser.parse_args()
    files = getFeedFiles(args.feed)
    with open('urls', 'w') as outFile:
        outFile.writelines(file + '\n' for file in files)
