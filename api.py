import time
import flask
from flask import request, jsonify
import os
import Search
import pickle
import gc
import Spotify_Search_v4
import download

app = flask.Flask(__name__)
app.config["DEBUG"] = False

@app.route('/api/loaddata', methods=['GET'])
def loadData():
    '''
    Loads the database files
    '''
    force = 'false'
    if 'f' in request.args:
        force = request.args['f']

    root = os.path.abspath(os.getcwd()) + r'/tmp'
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            pathList.append(os.path.join(path, name))

    if len(pathList) == 0 or force == 'true':
        download.MyWorker()

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
        keys = request.args['key']
        keys = keys.split('\\u0000\\u0000')
        keys = [i.replace('\\u0000', '\0') for i in keys]
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
            pathList.append(os.path.join(path, name))

    if len(pathList) < 4:
        response = jsonify("Database not loaded")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers",
                             "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response
 
    # Find most similar song using cosine similarity
    numOfSongs = 5

    # print time taken for this function
    sp = Spotify_Search_v4.authentiated_spotipy()
    songValues = [[key.split("\0")[0]]+[key.split("\0")[1]]+Spotify_Search_v4.get_features(key.split("\0")[2], sp) for key in keys]
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
