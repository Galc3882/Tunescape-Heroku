from time import sleep
from django.http import HttpResponse
import flask
from flask import request, jsonify
import os
import Search
import urllib
import pickle
import gc

app = flask.Flask(__name__)
app.config["DEBUG"] = False


# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>Tunescape</h1>'''

@app.route('/api/loaddata', methods=['GET'])
def loadData():
    '''
    Loads the database files
    '''
    
    root = os.path.abspath(os.getcwd()) + r'\tmp'
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            pathList.append(os.path.join(path, name))

    if len(pathList) == 0:
        # First one is namelist
        idList = ('1Rqrue1s6O4BPclNC0fkEkJm302JLqjjl', '1zDwM-vL87DpF762LGoWK-ITXZSGUd99_', '16yj4rBPqdgxK9qmA8tR08Kpo_iErNomL')
        idNames = ('namelist', 'database0', 'database1')
        for i in range(len(idList)):
            urllib.request.urlretrieve("https://drive.google.com/uc?export=download&id=" + idList[i] + "&confirm=t", "tmp/" + idNames[i] + ".pickle")
        return jsonify("Database loaded")

    return jsonify("Database already loaded")

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
        return "Error: No name field provided. Please specify a name."
    
    print(os.path.isfile(os.path.abspath(os.getcwd()) + r'\tmp\namelist.pickle'))
    if os.path.isfile(os.path.abspath(os.getcwd()) + r'\tmp\namelist.pickle'):
        return jsonify(Search.fuzzyGetSongTitle(name, os.path.abspath(os.getcwd()) + r'\tmp\namelist.pickle', 40))
    return jsonify("Database not loaded")

    

@app.route('/api/recommend', methods=['GET'])
def songRecommendation():
    '''
    Returns a list of songs in the database that are similar to the song and their similarity score.
    '''

    # Check if an key was provided as part of the URL.
    # If not, then return an error in the HTTP response.
    if 'key' in request.args:
        key = request.args['key']
        key = key.replace('\\u0000', '\0') 
    else:
        return "Error: No key field provided. Please specify a key."


    root = os.path.abspath(os.getcwd()) + r'\tmp'
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if not name.startswith("namelist"):
                pathList.append(os.path.join(path, name))

    if len(pathList) == 0:
        return jsonify("Database not loaded")

    songValue = None
    # Find song value in the database
    for path in pathList:
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            handle.close()
            if key in data.keys():
                songValue = data[key]
                break
        del data
        gc.collect()
    if len(pathList) > 0:
        del data
        gc.collect()
    if songValue == None:
        return jsonify(406)

    # Find most similar song using cosine similarity
    numOfSongs = 5
    similarSongs = Search.multiProcessing(
        Search.findSimilarSongs, 32, songValue, pathList, numOfSongs)

    # Sort the list by the similarity score
    sortedSimilarSongs = sorted(
        similarSongs, key=Search.takeSecond, reverse=True)
    if len(sortedSimilarSongs) > numOfSongs:
        sortedSimilarSongs = sortedSimilarSongs[:numOfSongs]
    
    return jsonify(sortedSimilarSongs)


# take second element for sort
def takeSecond(elem):
    return elem[1]

if __name__ == '__main__':
    #HttpResponse('Hello! ' * times)
    app.run()
