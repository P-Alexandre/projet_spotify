from data.connectors.spotify_client import create_spotify_client
from data.spotify.sp_playlists import search_playlists
from data.es_index import restore_index

import os
import argparse
from itertools import product


sp = create_spotify_client()


def scrape_sp_playlists(sp, queries):
    def next_queries(queries):
        chars = list('abcdefghijklmnopqrstuvwxyz1234567890')
        next_queries = []
        for toto in product(queries, chars):
            next_queries.append(''.join(toto))
        return next_queries

    dead_char = []
    for query in queries:
        search_results = search_playlists(sp, query, write=True)
        if search_results is False:
            dead_char.append(query)
    if len(dead_char) > 0:
        return scrape_sp_playlists(sp, next_queries(dead_char))
    else:
        return True


def main():
    # ARG
    parser = argparse.ArgumentParser(description='Scrape Spotify playlists')
    parser.add_argument('--query', metavar='Query string',
                        help='Set a list of string to be search')
    args = parser.parse_args()
    # Search playlists from spotify
    scrape_sp_playlists(sp, args.query)
    # Recover filename
    files = ['../../data/raw/playlists_test/{}'.format(filename) for filename in os.listdir('../../data/raw/playlists_test') if 'json' in filename]
    # Post playlists on ES
    for file in files:
        restore_index(file)


if __name__ == "__main__":
    main()
