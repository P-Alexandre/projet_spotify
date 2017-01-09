from data.hdd_write_es_bulk import write_es_bulk_playlists


def get_playlist_tracks(sp, user_playlist):
    """ Get tracks in playlist """
    playlist_ower = user_playlist['owner']['id']
    playlist_id = user_playlist['id']
    scrolled_tracks = sp.user_playlist_tracks(playlist_ower, playlist_id, limit=100)

    total_tracks = scrolled_tracks['total']
    res = scrolled_tracks['items']

    while len(res) < total_tracks:
        scrolled_tracks = sp.next(scrolled_tracks)
        res += scrolled_tracks['items']

    return res


def search_playlists(sp, query, write=True):
    """ Search by playlist name """
    limit = 50

    def get_results(write, search):
        if write:
            write_es_bulk_playlists(search['items'], query)
            return []
        else:
            return search['items']

    search = sp.search(query, limit=limit, offset=0, type='playlist')['playlists']
    total_playlists = search['total']
    print ">>>> Total number of playlist for query : {} is {}".format(query, total_playlists)

    if total_playlists > 100000:
        print "Too many results for query : {}".format(query)
        return False

    output = get_results(write, search)
    print "Playlists processed for {} : {}/{}".format(query, min(search['offset'] + limit, total_playlists), total_playlists)

    while search['next']:
        try:
            search = sp.next(search)['playlists']
        except:
            offset = search['offset'] + limit
            print ">> Playlists for offset {} are dead".format(offset)
            search = sp.search(query, limit=limit, offset=offset + 1, type='playlist')
            while search is None:
                print ">> Playlists for offset {} are dead".format(offset)
                offset += 1
                search = sp.search(query, limit=limit, offset=offset, type='playlist')
            search = search['playlists']
        print "Playlists processed for {} : {}/{}".format(query, min(search['offset'] + limit, total_playlists), total_playlists)
        output += get_results(write, search)

    return output
