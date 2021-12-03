![image](https://user-images.githubusercontent.com/16928672/139945152-1d71c4eb-53e2-4834-892e-b13813514149.png)

PodJelly is a tool for generating transcriptions from a podcast/RSS audio feed.
The parsing and transcription service is operational. Future developments are planned in the order listed:

- [ ] Persistent database for transcript storage along with metadata (episode number, length, tags, etc).
- [ ] Config yaml
- [ ] Front end web application for viewing transcripts (React.js)
- [ ] Automation of ingest process
- [ ] Add searching feature for specific words/phrases from transcript
- [ ] Containerization


# Architecture

![image](https://user-images.githubusercontent.com/16928672/139929165-a4e81ebb-1800-41ea-abfb-2da6469f4716.png)

## DB/Storage Schema

A main goal of this project is to support interactive indexing and listening of audio based on search terms. To fulfill this requirement, we will store each transcript as a series of chunks. For each chunk we will store an episode id, timestamp, and chunk transcript. 
