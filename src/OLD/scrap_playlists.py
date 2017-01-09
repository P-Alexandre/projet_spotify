import json
from spotify_client import create_spotify_client


sp = create_spotify_client()


def write_playlists(user_playlists, filename):
    with open('../playlists_scraped/playlists_{}.json'.format(filename), 'a') as index_infile:
        for playlist in user_playlists:
            bulk_var = {"index": {"_index": "spotify", "_type": "playlists"}}
            json.dump(bulk_var, index_infile)
            index_infile.write('\n')
            json.dump(playlist, index_infile)
            index_infile.write('\n')


def search_playlists(sp, query):
    search = sp.search(query, limit=50, offset=0, type='playlist')['playlists']

    if search['total'] > 100000:
        print "Too many results for query : {}".format(query)
        return None

    playlists = search['items']

    while search['next']:
        search = sp.next(search)['playlists']
        playlists += search['items']

    return playlists


# query = 'aaaaaaaaaaaa'
# playlists = search_playlists(sp, query)
# write_playlists(playlists, 'toto')


def get_playlists(sp, chars='abcdefghijklmnopqrstuvwxyz123456789'):
    dead_char = []
    for char in chars:
        print "Search playlists : {}".format(char)
        playlists = search_playlists(sp, char)
        if playlists is not None:
            write_playlists(playlists, char)
        else:
            dead_char.append(char)
    return dead_char


# dead_char = get_playlists(sp)


def search_write_playlists(sp, query):
    search = sp.search(query, limit=50, offset=0, type='playlist')['playlists']

    print ">>> Total number of playlist for query : {} is {}".format(query, search['total'])

    if search['total'] > 100000:
        print "Too many results for query : {}".format(query)
        return None

    write_playlists(search['items'], query)
    print "Playlists procesed : {}".format(search['offset'])

    while search['next']:
        search = sp.next(search)['playlists']
        write_playlists(search['items'], query)
        print "Playlists procesed : {}".format(search['offset'])

    return True


def scrape_playlists(sp, chars='abcdefghijklmnopqrstuvwxyz123456789'):
    dead_char = []
    for char in chars:
        playlists = search_write_playlists(sp, char)
        if playlists is None:
            dead_char.append(char)
    return dead_char


dead_char = scrape_playlists(sp)
