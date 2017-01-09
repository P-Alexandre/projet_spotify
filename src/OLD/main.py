from spotify_client import create_spotify_client
from utilities.users import get_user_tracks
from utilities.tracks import get_audio_features

###
# Spotify client
###

username = 'soma999'
scope = 'playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private user-library-read user-library-modify user-top-read'
sp = create_spotify_client(username, scope)



# User tracks
user_tracks = get_user_tracks(sp)

# Audio features
audio_features = get_audio_features(sp, [user_track['track']['id'] for user_track in user_tracks][:101])


import pandas as pd

pdf = pd.DataFrame(audio_features)
track_ids = list(pdf.sort('tempo')['id'])


pname = 'My Library sort by BPM'
# Create playlist
created_playlist = sp.user_playlist_create(username, pname)
# Add tracks to playlist
# sp.user_playlist_add_tracks(username, created_playlist['id'], track_ids)
def add_tracks(username, playlist_id, track_ids):
    total_tracks = len(track_ids)
    offset = 0
    limit = 100

    sp.user_playlist_add_tracks(username, playlist_id, track_ids[offset:limit], position=offset)

    while limit < total_tracks:
        offset += 100
        limit = offset + 100
        sp.user_playlist_add_tracks(username, playlist_id, track_ids[offset:limit], position=offset)


playlist_id = '0M70L5TbFKx80HS90ipVSV'
add_tracks(username, playlist_id, track_ids)
