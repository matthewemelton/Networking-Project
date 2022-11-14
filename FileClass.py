import os

FORMAT = "utf-8"


class File:
    def __init__(self, name):
        self.name = name
        self.path = f"./{name}"
        self.downloads = 0
        self.fileContents = None
        self.fileBytes = None
        self.fileSize = -1

    def addFileToServer(self):
        with open(f"./ServerFiles/{self.name}", "w") as f:
            f.write(self.fileContents)

        self.fileSize = os.path.getsize(f"./ServerFiles/{self.name}")

    def initContentGivenBytes(self, bytes: bytes):
        self.fileBytes = bytes
        self.fileContents = bytes.decode(FORMAT)

    def initBytesGivenContent(self, content: str):
        self.fileContents = content
        self.fileBytes = content.encode(FORMAT)
