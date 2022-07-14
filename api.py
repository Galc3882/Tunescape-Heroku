from time import sleep
from zipfile import ZipFile
from django.http import HttpResponse
import flask
from flask import request, jsonify
import os
import Search
import urllib
import pickle
import gc
import Spotify_Search_v4
import threading

app = flask.Flask(__name__)
app.config["DEBUG"] = False


class MyWorker():

    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        '''
        This function loads the database
        '''
        root = os.path.abspath(os.getcwd()) + r'/tmp'
        # create temp folder
        if not os.path.exists(root):
            os.makedirs(root)

        # download data
        # First one is namelist
        id = '1Tqzp545fieWEcNSR-KIWh4PdKTnDdW9X'
        urllib.request.urlretrieve("https://drive.google.com/uc?export=download&id=" +
                                       id + "&confirm=t", r"tmp/db.zip")
        # unzip data
        with ZipFile(r"tmp/db.zip", 'r') as zip_ref:
            zip_ref.extractall(r"tmp/")

        # delete zip file
        os.remove(r"tmp/db.zip")


@app.route('/api/loaddata', methods=['GET'])
def loadData():
    '''
    Loads the database files
    '''

    root = os.path.abspath(os.getcwd()) + r'/tmp'
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            pathList.append(os.path.join(path, name))

    if len(pathList) == 0:
        MyWorker()

        response = jsonify("Database loaded")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

    response = jsonify("Database already loaded")
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Credentials", True)
    response.headers.add("Access-Control-Allow-Headers",
                         "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
    response.headers.add("Access-Control-Allow-Methods", "GET")
    return response


@app.route('/api/songs', methods=['GET'])
def songName():
    ''' 
    Returns a list of songs in the database that match the song title and their similarity score.
    '''

    # Check if an name was provided as part of the URL.
    # If not, then return an error in the HTTP response.
    if 'name' in request.args:
        name = request.args['name']
    else:
        response = jsonify(
            "Error: No name field provided. Please specify a name.")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

    sp = Spotify_Search_v4.authentiated_spotipy()
    response = jsonify({'array': Spotify_Search_v4.search(name, sp)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Credentials", True)
    response.headers.add("Access-Control-Allow-Headers",
                         "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
    response.headers.add("Access-Control-Allow-Methods", "GET")
    return response

# TODO: change this to spotify and make it work
@app.route('/api/recommend', methods=['GET'])
def songRecommendation():
    '''
    Returns a list of songs in the database that are similar to the song and their similarity score.
    '''

    # Check if an key was provided as part of the URL.
    # If not, then return an error in the HTTP response.
    if 'key' in request.args:
        key = request.args['key']
        key = key.split('\\u0000\\u0000')
        key = [i.replace('\\u0000', '\0') for i in key]
    else:
        response = jsonify(
            "Error: No key field provided. Please specify a key.")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

    root = os.path.abspath(os.getcwd()) + r'/tmp'
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if not name.startswith("namelist"):
                pathList.append(os.path.join(path, name))

    if len(pathList) == 0:
        response = jsonify("Database not loaded")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

    songValues = []
    # Find song value in the database
    for path in pathList:
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            handle.close()
            for song in key:
                if song in data.keys():
                    songValues.append(data[song])
        del data
        gc.collect()
    if songValues == []:
        response = jsonify("Songs not found")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

    # Find most similar song using cosine similarity
    numOfSongs = 5
    similarSongs = Search.reduceSongs(songValues, pathList, numOfSongs)

    response = jsonify({'array': similarSongs})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Credentials", True)
    response.headers.add("Access-Control-Allow-Headers",
                         "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
    response.headers.add("Access-Control-Allow-Methods", "GET")
    return response


def takeSecond(elem):
    '''
    take second element for sort
    '''
    return elem[1]


if __name__ == '__main__':
    app.run()
