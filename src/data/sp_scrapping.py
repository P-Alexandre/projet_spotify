from data.connectors.spotify_client import create_spotify_client
from data.spotify.sp_playlists import search_playlists


sp = create_spotify_client()


def scrape_sp_playlists(sp, qchars='s12', write=True):
    chars = list('abcdefghijklmnopqrstuvwxyz1234567890')
    dead_char = []
    output = []
    for char in qchars:
        query_chars = zip(len(chars) * char, chars)
        for query_char in query_chars:
            qq = ''.join(query_char)
            playlists = search_playlists(sp, qq, write)
            if playlists is None:
                dead_char.append(qq)
            elif not write:
                output += playlists
    if write:
        return dead_char
    else:
        print dead_char
        return output
