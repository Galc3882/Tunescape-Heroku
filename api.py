from time import sleep
from django.http import HttpResponse
import flask
from flask import request, jsonify
import pickle
import Search
from urllib.request import urlopen

app = flask.Flask(__name__)
app.config["DEBUG"] = False


# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>Tunescape</h1>'''


@app.route('/api/loadpickle', methods=['GET'])
def loadPickle():
    '''
    Loads the pickle file
    '''
    global database
    if "database" not in globals():
        database = pickle.load(urlopen("https://drive.google.com/uc?export=download&id=1OlMk7v2K2JZnOtehY8eRBEdw89NXIXWU&confirm=t"))
        sleep(100)
        return jsonify("Database loaded")
    return jsonify("Database already loaded")

@app.route('/api/songs', methods=['GET'])
def songName():
    '''
    Returns a list of songs in the database that match the song title and their similarity score.
    '''
    global database
    if "database" not in globals():
        sleep(0.1)
        if "database" not in globals():
            return jsonify("Database not loaded")

    # Check if an name was provided as part of the URL.
    # If not, then return an error in the HTTP response.
    if 'name' in request.args:
        name = request.args['name']
    else:
        return "Error: No name field provided. Please specify an name."

    return jsonify(Search.fuzzyGetSongTitle(name, database.keys(), threshold=40))

@app.route('/api/recommend', methods=['GET'])
def songRecommendation():
    '''
    Returns a list of songs in the database that are similar to the song and their similarity score.
    '''
    global database
    if "database" not in globals():
        sleep(0.1)
        if "database" not in globals():
            return jsonify("Database not loaded")

    # Check if an key was provided as part of the URL.
    # If not, then return an error in the HTTP response.
    if 'key' in request.args:
        key = request.args['key']
        key = key.replace('\\u0000', '\0') 
    else:
        return "Error: No key field provided. Please specify an key."

    # Find the most similar songs to the song with key.
    similarSongs = Search.findSimilarSongs(database[key], database, 5)
    # Return a sorted list of the most similar songs.
    sortedSimilarSongs = sorted(similarSongs, key=takeSecond, reverse=True)
    
    return jsonify(sortedSimilarSongs)


# take second element for sort
def takeSecond(elem):
    return elem[1]

if __name__ == '__main__':
    #HttpResponse('Hello! ' * times)
    app.run()
