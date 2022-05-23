# ***** *** NOTE
# the following code requires SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET variables to be set

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_all_playlist_items(sp: spotipy.Spotify, playlist_id):
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


if __name__ == "__main__":
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    like_playlist = "29e9lxxlte7IE7dwrSHhKP"  # TODO - change
    long_playlist = "6IKQrtMc4c00YzONcUt7QH"

    print(get_all_playlist_items(sp, like_playlist)[0])
