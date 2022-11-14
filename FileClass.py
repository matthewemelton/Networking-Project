import os

class File:
  def __init__(self, name):
    self.name = name
    self.path = f"./{name}"
    self.downloads = 0
    self.fileContents = None

  def initSize(self):
    self.fileSize = os.path.getsize(f"./ServerFiles/{self.name}")