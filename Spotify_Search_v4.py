import spotipy
from datetime import timedelta
from spotipy.oauth2 import SpotifyClientCredentials


def authentiated_spotipy():
    '''Returns an authentiated Spotipy Instance'''
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    CLIENT_ID = 'd513b538756244beaabe189f5ba75be1'
    CLIENT_SECRET = '943e6dab04c34d78a05752b515e3fb2a'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def search(track_name, sp, debug=False):
    '''Returns an array with up to 50 tracks (arrays)
    Each track-array contains: 
    0: song name, 1: artists names, 2: duration, 3: album art, 4: release date, 5: popularity, 6: explicit (T/F), 7: spotify url, 8: id (uri)'''
    result = sp.search(track_name, limit=50, type='track')
    if debug:
        print("DEBUG:", result['tracks']['total'], "tracks found")
    num_tracks_capped = len(result['tracks']['items'])

    results_trimmed = []

    for i in range(0, num_tracks_capped):
        name = result['tracks']['items'][i]['name']
        artists = ""
        for j in range(0, len(result['tracks']['items'][i]['artists'])):
            artists += result['tracks']['items'][i]['artists'][j]['name'] + " "
        artists = artists[:-1]  # Remove last space
        # TODO: Check Time Complexity of this last opperation
        duration = str(timedelta(
            seconds=result['tracks']['items'][i]['duration_ms']/1000))
        if duration[0] == '0':
            if duration[2] == '0':
                duration = duration[3:7]
            else:
                duration = duration[2:7]
        else:
            duration = duration[:7]
        album_art = result['tracks']['items'][i]['album']['images'][1]['url']
        release_date = result['tracks']['items'][i]['album']['release_date']
        popularity = result['tracks']['items'][i]['popularity']
        explicit = result['tracks']['items'][i]['explicit']
        url = result['tracks']['items'][i]['external_urls']['spotify']
        id = result['tracks']['items'][i]['id']

        track_info = [name, artists, duration, album_art,
                      release_date, popularity, explicit, url, id]

        results_trimmed.append(track_info)
    return results_trimmed


def get_features(track_id, sp, debug=False):
    '''Returns an array with the features of a track
    The features returned are: 
    0: Key, 1: Mode, 2: Tempo, 3: Loudness, 4: Time-Signature, 5: Section Starts, 6: Segment Pitches, 7: Segment Timbre, 8: Bars Start, 9: Beats Start 10: Tatums Start'''
    # TODO: What do we actually do with sections start?
    get_audio_features = sp.audio_features(track_id)
    get_audio_analysis = sp.audio_analysis(track_id)

    if debug:
        print("DEBUG: AUDIO FEATURES:\t", get_audio_features)
        print("DEBUG: AUDIO ANALYSIS:\t", get_audio_analysis)

    key = get_audio_features[0]['key']
    mode = get_audio_features[0]['mode']
    tempo = get_audio_features[0]['tempo']
    loudness = get_audio_features[0]['loudness']
    time_signature = get_audio_features[0]['time_signature']
    section_starts = get_audio_analysis['sections'][0]['start']
    segment_pitches = get_audio_analysis['segments'][0]['pitches']
    segment_timbre = get_audio_analysis['segments'][0]['timbre']
    bars_start = get_audio_analysis['bars'][0]['start']
    beats_start = get_audio_analysis['beats'][0]['start']
    tatums_start = get_audio_analysis['tatums'][0]['start']

    result = [key, mode, tempo, loudness, time_signature, section_starts,
              segment_pitches, segment_timbre, bars_start, beats_start, tatums_start]
    return result


if __name__ == "__main__":
    sp = authentiated_spotipy()
    tracks = search("Smooth Criminal", sp)
    print(tracks[0])
    print(get_features(tracks[0][8], sp))

# TODO: Ceck out the following API fucntons on https://spotipy.readthedocs.io/en/master/#api-reference:
'''
current_user_playlists(limit=50, offset=0)
current_user_recently_played(limit=50, after=None, before=None)
current_user_saved_albums(limit=20, offset=0, market=None)
current_user_saved_tracks(limit=20, offset=0, market=None)

playlist_add_items(playlist_id, items, position=None)
playlist_change_details(playlist_id, name=None, public=None, collaborative=None, description=None)
playlist_cover_image(playlist_id)
playlist_items(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
playlist_upload_cover_image(playlist_id, image_b64)

recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None, **kwargs)
'''

#start_time = time.time()
#name = ["Smooth Criminal"]
# print(time.time()-start_time)
# for i in range(len(result)):
#print("Song", i + 1)
# print(result[i])

'''
# API_URL = 'https://api.spotify.com/v1/search?type=album&include_external=audio'
API_URL = 'https://api.spotify.com/v1/search?'

search_query = 'Firework'
search_query2 = 'test'
'''
