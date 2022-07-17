import os
from zipfile import ZipFile
import threading

import urllib


class MyWorker():

    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        '''
        This function loads the database
        '''
        # delete all the files in the folder tmp
        if os.path.exists('tmp'):
            for file in os.listdir("tmp"):
                os.remove("tmp/" + file)

        root = os.path.abspath(os.getcwd()) + r'/tmp'
        # create temp folder
        if not os.path.exists(root):
            os.makedirs(root)

        # download the zip file
        urllib.request.urlretrieve(r"https://tunescape.blob.core.windows.net/database/db.zip", r"tmp/db.zip")

        # unzip data
        with ZipFile(r"tmp/db.zip", 'r') as zip_ref:
            zip_ref.extractall(r"tmp/")

        # delete zip file
        os.remove(r"tmp/db.zip")
