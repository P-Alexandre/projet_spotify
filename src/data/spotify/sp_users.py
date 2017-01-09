def get_user_playlists(sp, username=None):
    """ Get user playlists """
    username = sp.me()['id'] if username is None else username
    scrolled_playlists = sp.user_playlists(username, limit=50)
    total_playlists = scrolled_playlists['total']
    res = scrolled_playlists['items']

    while len(res) < total_playlists:
        scrolled_playlists = sp.next(scrolled_playlists)
        res += scrolled_playlists['items']

    return res


def get_user_library_tracks(sp):
    """ Get logged user saved tracks """
    scrolled_tracks = sp.current_user_saved_tracks(limit=50)

    total_tracks = scrolled_tracks['total']
    res = scrolled_tracks['items']

    while len(res) < total_tracks:
        scrolled_tracks = sp.next(scrolled_tracks)
        res += scrolled_tracks['items']

    return res


def get_user_library_albums(sp):
    """ Get logged user saved albums """
    scrolled_albums = sp.current_user_saved_albums(limit=50)

    total_tracks = scrolled_albums['total']
    res = scrolled_albums['items']

    while len(res) < total_tracks:
        scrolled_albums = sp.next(scrolled_albums)
        res += scrolled_albums['items']

    return res
