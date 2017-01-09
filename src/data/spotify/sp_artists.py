from collections import Counter


def get_artists_genres(sp, playlist_artists, weighted=True):
    """ Get artist genre """
    artists = Counter(playlist_artists)
    artist_ids = artists.keys()
    total_artists = len(artist_ids)

    def get_artist_genres(artist, artists_counter=artists):
        if weighted:
            return artist['genres'] * artists_counter[artist['id']]
        else:
            return artist['genres']

    offset = 0
    limit = 50
    scrolled_artists = sp.artists(artist_ids[offset:limit])['artists']

    total_scrolled_artists = len(scrolled_artists)
    res = [get_artist_genres(artist) for artist in scrolled_artists]

    while total_scrolled_artists < total_artists:
        offset += 50
        limit = offset + 50
        scrolled_artists = sp.artists(artist_ids[offset:limit])['artists']
        total_scrolled_artists += len(scrolled_artists)
        res += [get_artist_genres(artist) for artist in scrolled_artists]

    return reduce(lambda x, y: x + y, res)
