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
    
    root = os.path.abspath(os.getcwd()) + r'/tmp'
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            pathList.append(os.path.join(path, name))

    if len(pathList) == 0:
        # creat temp folder
        if not os.path.exists(root):
            os.makedirs(root)

        # download data
        # First one is namelist
        idList = ('1Rqrue1s6O4BPclNC0fkEkJm302JLqjjl', '1zDwM-vL87DpF762LGoWK-ITXZSGUd99_', '16yj4rBPqdgxK9qmA8tR08Kpo_iErNomL')
        idNames = ('namelist', 'database0', 'database1')
        for i in range(len(idList)):
            urllib.request.urlretrieve("https://drive.google.com/uc?export=download&id=" + idList[i] + "&confirm=t", r"tmp/" + idNames[i] + r".pickle")
        response = jsonify("Database loaded")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

    response = jsonify("Database already loaded")
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Credentials", True)
    response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
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
        response = jsonify( "Error: No name field provided. Please specify a name.")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response
    
    if os.path.isfile(os.path.abspath(os.getcwd()) + r'/tmp/namelist.pickle'):
        l = [[i[0].split('\0')[0], i[0].split('\0')[1]] for i in Search.fuzzyGetSongTitle(name, os.path.abspath(os.getcwd()) + r'/tmp/namelist.pickle', 40)]
        response = jsonify({'array':l})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

    response = jsonify("Database not loaded")
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Credentials", True)
    response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
    response.headers.add("Access-Control-Allow-Methods", "GET")
    return response

    

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
        response = jsonify("Error: No key field provided. Please specify a key.")
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
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
        response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

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
        response = jsonify("Song not found")    
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add("Access-Control-Allow-Credentials", True)
        response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
        response.headers.add("Access-Control-Allow-Methods", "GET")
        return response

    # Find most similar song using cosine similarity
    numOfSongs = 5
    similarSongs = Search.multiProcessing(
        Search.findSimilarSongs, 32, songValue, pathList, numOfSongs)

    # Sort the list by the similarity score
    sortedSimilarSongs = sorted(
        similarSongs, key=Search.takeSecond, reverse=True)
    if len(sortedSimilarSongs) > numOfSongs:
        sortedSimilarSongs = sortedSimilarSongs[:numOfSongs]
    
    response = jsonify({'array':sortedSimilarSongs})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Credentials", True)
    response.headers.add("Access-Control-Allow-Headers", "Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale")
    response.headers.add("Access-Control-Allow-Methods", "GET")
    return response

# take second element for sort
def takeSecond(elem):
    return elem[1]

if __name__ == '__main__':
    #HttpResponse('Hello! ' * times)
    app.run()
