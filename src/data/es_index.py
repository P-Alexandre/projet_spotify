from data.connectors.elasticsearch_connector import ESConnector


db_client = ESConnector('https://{}'.format('localhost:9200/'), ('elastic', 'changeme'))


def restore_index(file='index_toto.json'):
    """ ElasticSearch bulk function """
    print '>>> Restoring index content'
    with open(file, 'r') as index_infile:
        index = db_client.post_data_response(
            post_url='_bulk',
            data=index_infile,
            headers={'Content-Type': 'application/json'}
        )
    print '<<< Restored index, response: {}'.format(index.content)
