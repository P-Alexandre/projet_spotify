from data.connectors.elasticsearch_connector import ESConnector


db_client = ESConnector('https://{}'.format('localhost:9200/'), ('elastic', 'changeme'))


def restore_index(index_file='index_toto.json'):
    """ ElasticSearch bulk function """
    print '>>> Restoring index content'
    with open(index_file, 'r') as index_infile:
        index = db_client.post_response(
            post_url='_bulk',
            json_data=index_infile,
            headers={'Content-Type': 'application/json'}
        )
    print '<<< Restored index, response: {}'.format(index.content)
