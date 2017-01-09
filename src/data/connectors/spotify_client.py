import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.util import prompt_for_user_token


###
# Application constants
###

SPOTIPY_CLIENT_ID = 'b32c952630e24cd08d0dea3bf942d34e'
SPOTIPY_CLIENT_SECRET = 'ed99345197a74023a908a4829936bac4'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888'


###
# Spotify client
###

def create_spotify_client(username=None, scope=None):
    """ Create Spotify client """
    if username is not None:
        token = prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
    else:
        token = None
    client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    return spotipy.Spotify(auth=token, client_credentials_manager=client_credentials_manager)
