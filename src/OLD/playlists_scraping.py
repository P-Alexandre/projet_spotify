import json


def write_playlists(user_playlists, filename):
    with open('../playlists_scraped/playlists_{}.json'.format(filename), 'a') as index_infile:
        for playlist in user_playlists:
            bulk_var = {"index": {"_index": "spotify", "_type": "playlists"}}
            json.dump(bulk_var, index_infile)
            index_infile.write('\n')
            json.dump(playlist, index_infile)
            index_infile.write('\n')


def search_write_playlists(sp, query):
    search = sp.search(query, limit=50, offset=0, type='playlist')['playlists']
    total_playlists = search['total']
    print ">>>> Total number of playlist for query : {} is {}".format(query, total_playlists)

    if total_playlists > 100000:
        print "Too many results for query : {}".format(query)
        return None

    write_playlists(search['items'], query)
    print "Playlists processed for {} : {}/{}".format(query, search['offset'] + 50, total_playlists)

    while search['next']:
        try:
            search = sp.next(search)['playlists']
            write_playlists(search['items'], query)
        except:
            print ">> Playlists for offset {} are dead".format(search['offset'])
            new_offset = search['offset'] + 100
            search = sp.search(query, limit=50, offset=new_offset, type='playlist')['playlists']
        print "Playlists processed for {} : {}/{}".format(query, search['offset'] + 50, total_playlists)

    return True


def scrape_playlists(sp, qchars='s12'):
    chars = list('abcdefghijklmnopqrstuvwxyz1234567890')
    dead_char = []
    for char in qchars:
        query_chars = zip(len(chars) * char, chars)
        for query_char in query_chars:
            qq = ''.join(query_char)
            playlists = search_write_playlists(sp, qq)
            if playlists is None:
                dead_char.append(qq)
    return dead_char


scrape_playlists(sp)


import requests
import os


[filename for filename in os.listdir('./playlists_scraped') if 'json' in filename]


def restore_index(db):
    print '>>> Restoring index content'
    with open('index_{}.json'.format('toto'), 'r') as index_infile:
        index = requests.post(
            url='https://localhost:9200/_bulk',
            auth=('elastic', 'changeme'),
            verify=False,
            data=index_infile,
            headers={'Content-Type': 'application/json'}
        )
    print '<<< Restored index, response: {}'.format(index.content)
