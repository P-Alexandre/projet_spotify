def extract_playlist_tracks_artists(playlist_tracks):
    """ Get artists in playlist """
    artists_ids = list()
    for track in playlist_tracks:
        for artist in track['track']['artists']:
            artists_ids.append(artist['id'])
    return [artist_id for artist_id in artists_ids if artist_id is not None]
