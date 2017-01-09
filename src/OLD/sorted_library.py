from spotify_client import create_spotify_client
from utilities.users import get_user_tracks
from utilities.tracks import get_audio_features
import pandas as pd


###
# Spotify client
###

username = 'soma999'
scope = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-library-modify user-top-read'
sp = create_spotify_client(username, scope)


###
# Add tracks
###

def add_tracks(username, playlist_id, track_ids):
    total_tracks = len(track_ids)
    offset = 0
    limit = 100

    sp.user_playlist_add_tracks(username, playlist_id, track_ids[offset:limit], position=offset)

    while limit < total_tracks:
        offset += 100
        limit = offset + 100
        sp.user_playlist_add_tracks(username, playlist_id, track_ids[offset:limit], position=offset)


###
#
###

def create_sorted_playlist_from_library(username, pname, sort_field):
    user_tracks = get_user_tracks(sp)
    audio_features = get_audio_features(sp, [user_track['track']['id'] for user_track in user_tracks])
    pdf = pd.DataFrame(audio_features)
    sorted_track_ids = list(pdf.sort(sort_field)['id'])
    created_playlist = sp.user_playlist_create(username, pname)
    add_tracks(username, created_playlist['id'], sorted_track_ids)


pname = 'My Library sorted by energy'
sort_field = 'energy'
# create_sorted_playlist_from_library(username, pname, sort_field)

user_tracks = get_user_tracks(sp)
audio_features = get_audio_features(sp, [user_track['track']['id'] for user_track in user_tracks])
pdf = pd.DataFrame(audio_features)


import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
plt.hist(pdf['energy'])
