from data.connectors.elasticsearch_connector import ESConnector


db_client = ESConnector('https://{}'.format('localhost:9200/'), ('elastic', 'changeme'))


def get_playlists_info_for_tracks(playlists_ids):
    """ Get users in mission M """
    query = {
        "_source": {"includes": ['owner.id', 'id']},
        "query": {"term": {"_id": playlists_ids}}
    }
    search = db_client.get_json_response(
        search_url='/spotify/playlists/_search',
        json_data=query
    )
    db_client.raise_search_error(search, 'Error')
    return search['hits']['hits'][0]['_source']
