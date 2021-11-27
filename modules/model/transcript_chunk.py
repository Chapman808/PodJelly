class TranscriptChunk:
    episode = None
    def __init__(self, transcript, timestamp, episode) -> None:
        self.transcript = transcript
        self.timestamp = timestamp
        self.episode = episode
    def __str__(self) -> str:
        return self.episode + " :: " + str(self.timestamp) + "s" + " :: " + self.transcript
    