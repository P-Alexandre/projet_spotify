from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.client import IndicesClient


es = Elasticsearch(
    ['localhost:9200'],
    connection_class=RequestsHttpConnection,
    use_ssl=True,
    verify_certs=False,
    http_auth=('elastic', 'changeme')
)


IndicesClient(es).create(
    index='spotify',
    body
)

es.search(
    index='spotify',
    doc_type='playlists',
    _source_include=['owner.id', 'id'],
    body={
        'query': {
            'bool': {
                'filter': {
                    'term': {'owner.id': '1169485801'}
                }
            }
        }
    })

