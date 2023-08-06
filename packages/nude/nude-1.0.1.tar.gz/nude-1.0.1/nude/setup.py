from os import path
from io import BytesIO
from requests import get
from zipfile import ZipFile
def setup():
    print("Starting setup, this may take a very long time")
    ZipFile(BytesIO(get('https://github.com/donno2048/nude/releases/download/v1.0.0/data.zip').content)).extractall(path.dirname(__file__))
if __name__ == '__main__': setup()
