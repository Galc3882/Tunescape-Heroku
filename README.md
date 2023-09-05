# Tunescape API Documentation

Welcome to the Tunescape API documentation! This document provides an in-depth overview of the Tunescape project, its purpose, how it works, code walkthrough, and more. Tunescape is a startup created by Efe Tascioglu, Gal Cohen, and Micol Altomare, aiming to provide a song recommendation service based on the underlying characteristics of songs. This service is designed to offer highly personalized song recommendations to users, allowing them to explore a wide range of music tailored to their tastes.

## Introduction

Tunescape is a project developed by Efe Tascioglu, Gal Cohen, and Micol Altomare with the goal of creating a unique song recommendation service. This service employs a sophisticated algorithm that prioritizes the underlying characteristics of songs, such as key signature and tempo, to make recommendations that resonate with users.

## Purpose

The primary purpose of the Tunescape Heroku container is to provide a RESTful API for various endpoints, including song search, recommended songs, and a similarity score calculation based on the user's musical preferences. This API allows developers to integrate Tunescape's recommendation engine into their applications, enabling users to discover music that aligns with their specific musical tastes.

## Overview

Tunescape is a song recommendation system built around the idea of prioritizing the musical characteristics of songs. Here's an overview of how it works:

- Tunescape utilizes an algorithm to analyze the underlying characteristics of songs, including key signature, tempo, and more.

- Users can make requests to the Tunescape API to perform actions such as searching for songs, retrieving song recommendations, and calculating similarity scores.

- The API is designed to return highly relevant results based on the user's input. For example, when searching for a song, the API will return a list of songs that match the query along with their similarity scores.

- Tunescape makes use of the Spotify API to access additional song information and enhance the recommendation process.

## Example

Let's walk through an example of how you can use the Tunescape API:

**Search for Songs:**

Suppose you want to search for songs with the title "Summer Vibes." You can make a GET request to the following endpoint:

```
GET /api/songs?name=Summer\u0000Vibes
```

The API will return a list of songs that match the title "Summer Vibes" along with their similarity scores using fuzzy search.

**Retrieve Song Recommendations:**

To get song recommendations based on a key, you can make a GET request to the following endpoint:
```
GET /api/recommend?key=your_song_key
```

Replace `your_song_key` with the actual key of the song you're interested in. The API will return a list of songs that are similar to the provided song key, along with their similarity scores using our proprietary algorithm.

## Detailed Walkthrough of the Code and Features

Now, let's dive into the code and explore the features of the Tunescape API:

### `api.py`

- `loadData()`: This route loads the database files required for song recommendations. It checks if the database is already loaded and, if not, downloads and initializes it.

- `songName()`: Returns a list of songs in the database that match the song title and their similarity scores based on user input.

- `songRecommendation()`: Provides a list of songs in the database that are similar to a given song, along with their similarity scores. It uses cosine similarity for recommendation.

### `download.py`

- `MyWorker`: This class handles the downloading and extraction of the database files. It ensures that the database is up to date and accessible to the API.

### `requirements.txt`

This file lists all the required Python packages and libraries needed to run the Tunescape API on your server.

## Requirements and File Architecture

To run the Tunescape API, you'll need to install the required packages listed in the `requirements.txt` file. Additionally, you should be aware of the following file structure:

- `api.py`: The main Python script that defines the API endpoints and their functionality.
- `download.py`: Responsible for downloading and maintaining the database used for song recommendations.
- `requirements.txt`: A file specifying the required Python packages.
- Other Python scripts like `FeatureSimilarity.py`, `Search.py`, and `Spotify_Search_v4.py` that are used to implement the core features of the Tunescape API.

## Conclusion

Tunescape is an innovative project that leverages musical characteristics to offer highly personalized song recommendations to users. This API documentation provides an overview of its purpose, functionality, and code structure.

## Next Steps

Here are some potential next steps for the Tunescape project:

- [ ] Implement user authentication and user-specific playlists.
- [ ] Enhance the API endpoints with more features.
- [ ] Scale the infrastructure to handle a larger user base and song database.

**Project Developers:**
- Efe Tascioglu
- Gal Cohen
- Micol Altomare


<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.
