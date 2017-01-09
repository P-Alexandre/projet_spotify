import json


def write_es_bulk_playlists(playlists, filename, path='../../data/raw/playlists_test'):
    with open('{}/playlists_{}.json'.format(path, filename), 'a') as index_infile:
        for playlist in playlists:
            bulk_var = {"index": {"_index": "spotify", "_type": "playlists"}}
            json.dump(bulk_var, index_infile)
            index_infile.write('\n')
            json.dump(playlist, index_infile)
            index_infile.write('\n')
