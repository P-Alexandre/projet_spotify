from data.connectors.spotify_client import create_spotify_client
from data.sp_playlists import get_playlist_tracks
from data.sp_artists import get_artists_genres
from data.sp_users import get_user_playlists
from features.playlists import get_playlist_tracks_artists

from wordcloud import WordCloud
from collections import Counter
import unicodedata
import os

###
# Spotify client
###

sp = create_spotify_client()


###
# Generate WordCloud
###

def generate_wordcloud(username, pname, playlist_genres, max_words):
    wc = WordCloud(max_words=max_words)
    words = Counter(playlist_genres).most_common(max_words)
    wc.generate_from_frequencies(words)
    wc.to_file('../results/{}/{}.png'.format(username, pname))


###
# Playlists
###

def generate_user_wordclouds(username):
    user_playlists = get_user_playlists(sp, username)

    try:
        os.mkdir('../results/{}'.format(username))
    except:
        pass

    for playlist in user_playlists:
        pname = unicodedata.normalize('NFKD', playlist['name']).encode('ascii', 'ignore').replace('/', '')
        print '>>> Processing playlist : {}'.format(pname)
        playlist_tracks = get_playlist_tracks(sp, playlist)
        playlist_artists = get_playlist_tracks_artists(playlist_tracks)
        playlist_genres = get_playlist_artists_genres(sp, playlist_artists) if len(playlist_artists) is not 0 else ['Unkown']
        generate_wordcloud(username, pname, playlist_genres, 15)


###
# Main
###

# Sylvain

generate_user_wordclouds('sylrouss')
