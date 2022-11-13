import os

class File:
  def __init__(self, name):
    self.name = name
    self.path = f"./{name}"
    self.downloads = 0
    self.fileSize = os.path.getsize(f"./ServerFiles/{name}")
    self.fileContents = None