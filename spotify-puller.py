# ***** *** NOTE
# the following code requires SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET variables to be set

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

from unidecode import unidecode

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def get_all_playlist_items(sp: spotipy.Spotify, playlist_id) -> list:
    """
    Pulls all songs from the given playlist, even if it exceeds the limit of 100 tracks
    :param sp: Spotify API client
    :param playlist_id: id of playlist to pull from
    :return: list of all item info of all songs in the playlist
    """
    # https://stackoverflow.com/questions/39086287/spotipy-how-to-read-more-than-100-tracks-from-a-playlist
    results = sp.playlist_items(playlist_id=playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def make_tracks_data(sp: spotipy.Spotify, playlist, liked: bool = None) -> pd.DataFrame:
    """
    Creates pandas dataframe containing data useful for classification

    If given, adds on boolean `liked` attribute

    :param sp: Spotify API client
    :param playlist: uri of the playlist
    :param liked: optional boolean attribute applied to all tracks (not used by default)
    :return: pandas dataframe with dataset for the classification
    """

    # NOTE - stupid python won't change single quote to nothing
    # (e.g. Noisekick's and Terrordrang and is the result...)
    def wekafier_text(text):
        rejects = {',': ' ', ';': ' ', "'": ''}
        for key in rejects:
            text = text.replace(key, rejects[key])

        text = unidecode(text)

        return ''.join([x if x != "'" else '' for x in text])  # That's the workaround...

    tracks_items = get_all_playlist_items(sp, playlist)

    df = pd.DataFrame(columns=[
        # ***** *** meta
        'name',                   # dropped because of WEKA csv reading process
        'artists',                # dropped because of WEKA csv reading process
        'uri',                      # easy access to the song
        # ***** *** functional
        'acousticness',             # [0.0, 1.0]            - (not acoustic - acoustic)
        'danceability',             # [0.0, 1.0]            - (not for dancing - suitable for dance)
        'energy',                   # [0.0, 1.0]            - (not energetic, most energetic)
        'instrumentalness',         # [0.0, 1.0]            - (lyrical, instrumental)
        'key',                      # [0, 1, (...), 11]     - key according to standard Pitch Class notation
                                    #                         https://en.wikipedia.org/wiki/Pitch_class
        'liveness',                 # [0.0, 1.0]            - (studio recording, live performance)
        'loudness',                 # [-60, 0]              - (quiet, loud)
        'mode',                     # binary                - 0 (minor) or 1 (major)
        'speechiness',              # [0.0, 1.0]            - (no speech, speech-intensive)
        'tempo',                    # [0, inf)              - overall estimated tempo in BPM
        'time_signature',           # [0, 1, (...),  inf)   - no. of beats in each bar TODO - inf?
        'valence'                   # [0.0, 1.0]            - (sounds negative, sounds positive)
    ])

    tracks = [ti['track'] for ti in tracks_items]
    for track in tracks:
        track_data = dict()

        # ***** *** meta TODO - comma handling
        track_data['name'] = wekafier_text(track['name'])
        artists = ''
        for artist in track['artists']:
            artists += artist['name'] + ' and '
        artists = wekafier_text(artists)
        track_data['artists'] = artists  # track['artists'][0]['name']
        track_data['uri'] = track['uri']

        # ***** *** functional
        track_audio_features = sp.audio_features(track['uri'])[0]
        track_data['acousticness'] = track_audio_features['acousticness']
        track_data['danceability'] = track_audio_features['danceability']
        track_data['energy'] = track_audio_features['energy']
        track_data['instrumentalness'] = track_audio_features['instrumentalness']
        track_data['key'] = track_audio_features['key']  # TODO - map keys
        track_data['liveness'] = track_audio_features['liveness']
        track_data['loudness'] = track_audio_features['loudness']
        track_data['mode'] = track_audio_features['mode']  # TODO - map into category OR binary True/False
        track_data['speechiness'] = track_audio_features['speechiness']
        track_data['tempo'] = track_audio_features['tempo']
        track_data['time_signature'] = track_audio_features['time_signature']
        track_data['valence'] = track_audio_features['valence']

        df = df.append(track_data, ignore_index=True)

    if liked is not None:
        df['liked'] = liked

    return df


if __name__ == "__main__":
    # setting up
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # playlists
    liked_playlist = '5RjMFH5S8IVDgfQ1Ieb1tE'
    dislike_playlist = '0MdJYjGcqxXeGvCInR5AaA'
    validation_playlist = '3TYkNBdCNc726vILtliMuo'

    # making data
    liked_tracks_data = make_tracks_data(sp, liked_playlist, True)
    liked_tracks_data.index.name = 'idx'
    liked_tracks_data.to_csv('data/liked.csv')

    disliked_tracks_data = make_tracks_data(sp, dislike_playlist, False)
    disliked_tracks_data.index.name = 'idx'
    disliked_tracks_data.to_csv('data/disliked.csv')

    # TODO - may need to manually assign if the following are liked or not
    validation_tracks_data = make_tracks_data(sp, validation_playlist)
    validation_tracks_data.index.name = 'idx'
    validation_tracks_data.to_csv('data/validation.csv')

    combined_tracks_data = pd.concat([liked_tracks_data, disliked_tracks_data])
    combined_tracks_data = combined_tracks_data.reset_index(drop=True)
    combined_tracks_data.index.name = 'idx'
    combined_tracks_data.to_csv('data/combined.csv')


# ***** *** NOTE - interesting to potentially get into later, but for now
    # aa = sp.audio_analysis(tracks_uri[0])
    # print(aa['meta'])  # metadata regarding the machine analysis was run on and software
    # print(aa['track'])  # seems to have some valuable things (?)
    # print(aa['bars'])  # rather not
    # print(aa['beats'])  # as above
    # print(aa['sections'])  # interesting, but rather too complicated
    # print(aa['segments'])  # as the above
    # print(aa['tatums'])  # as bars or beats
