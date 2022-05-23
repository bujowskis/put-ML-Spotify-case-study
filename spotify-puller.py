# ***** *** NOTE
# the following code requires SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET variables to be set

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


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


def extract_tracks_uri(tracks_items: list) -> list:
    """
    Extracts tracks uri from the list of all item info of songs
    :param tracks_items: list of all item info of all songs
    :return: list of tracks uri
    """
    return [item['track']['uri'] for item in tracks_items]


def make_tracks_data(sp: spotipy.Spotify, tracks_uri: list, liked: bool = None):
    """
    Creates pandas dataframe containing data useful for classification

    If given, adds on boolean `liked` attribute
    :param sp: Spotify API client
    :param tracks_uri: list of tracks uri
    :param liked: optional boolean attribute applied to all tracks (not used by default)
    :return: pandas dataframe with dataset for the classification
    """
    ...


if __name__ == "__main__":
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    example_playlist = "29e9lxxlte7IE7dwrSHhKP"

    tracks_items = get_all_playlist_items(sp, example_playlist)
    tracks_uri = extract_tracks_uri(tracks_items)

    # ***** *** NOTE - interesting to potentially get into later, but for now
    # aa = sp.audio_analysis(tracks_uri[0])
    # print(aa['meta'])  # metadata regarding the machine analysis was run on and software
    # print(aa['track'])  # seems to have some valuable things (?)
    # print(aa['bars'])  # rather not
    # print(aa['beats'])  # as above
    # print(aa['sections'])  # interesting, but rather too complicated
    # print(aa['segments'])  # as the above
    # print(aa['tatums'])  # as bars or beats

