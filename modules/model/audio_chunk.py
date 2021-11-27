class AudioChunk:
    episode = None
    def __init__(self, audioFile, timestampSeconds, episode) -> None:
        self.audioFile = audioFile
        self.timestampSeconds = timestampSeconds
        self.episode = episode
    def __str__(self) -> str:
        return self.episode + " :: " + str(self.timestampSeconds) + "s" + " :: " + str(type(self.audioFile))
    