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
    global database
    # Check if an name was provided as part of the URL.
    # If not, then return an error in the HTTP response.
    if 'name' in request.args:
        name = request.args['name']
    else:
        return "Error: No name field provided. Please specify an name."

    '''
    Parse url variables and return a list of songs
        :	Separate protocol (http) from address	%3B
        /	Separate domain and directories	%2F
        #	Separate anchors	%23
        ?	Separate query string	%3F
        &	Separate query elements	%24
        @	Separate username and password from domain	%40
        %	Indicates an encoded character	%25
        +	Indicates a space	%2B
        <space>	Not recommended in URLs	%20 or +
    '''
    return jsonify(Search.fuzzyGetSongTitle(name, database.keys(), threshold=40))

@app.route('/api/recommend', methods=['GET'])
def songRecommendation():
    global database
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
    with open('database.pickle', 'rb') as handle:
        global database
        database = pickle.load(handle)

    #HttpResponse('Hello! ' * times)
    app.run()
