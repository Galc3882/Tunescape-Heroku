import os
from django.http import HttpResponse
import flask
from flask import request, jsonify
import pickle
import Search

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Tunescape</h1>'''


# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     return jsonify(books)


@app.route('/api/songs', methods=['GET'])
def songName():
    # Check if an name was provided as part of the URL.
    # If not, then return an error in the HTTP response.
    if 'name' in request.args:
        name = request.args['name']
    else:
        return "Error: No name field provided. Please specify an name."

    
    return jsonify(Search.fuzzyGetSongTitle(name, database.keys(), threshold=40))

@app.route('/api/recommend', methods=['GET'])
def songRecommendation():
    # Check if an key was provided as part of the URL.
    # If not, then return an error in the HTTP response.
    if 'key' in request.args:
        key = request.args['key']
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
    # get request count and initialize database if it doesn't exist
    i = int(os.environ.get('TIMES', 1))
    if i == 1:
        with open('database.pickle', 'rb') as handle:
            database = pickle.load(handle)
        
    # update request count
    os.environ['TIMES'] = str(i+1)

    #HttpResponse('Hello! ' * times)
    app.run()
