import requests


class BColors:
    ERROR = '\033[91m'
    ENDC = '\033[0m'


class ESConnector():

    def __init__(self, url_prefix, auth):
        self.AUTH = auth
        self.URL_PREFIX = url_prefix

    def get_json_response(self, search_url=None, json_data=None):
        url = '{}{}'.format(self.URL_PREFIX, search_url)
        return requests.get(url=url, auth=self.AUTH, verify=False, json=json_data).json()

    def post_response(self, post_url=None, json_data=None, headers=None):
        url = '{}{}'.format(self.URL_PREFIX, post_url)
        return requests.post(url=url, auth=self.AUTH, verify=False, json=json_data, headers=headers)

    @staticmethod
    def raise_search_error(search, error_msg=None):
        if search.get('error', None) is not None:
            raise Exception('{}{}{} : {}'.format(
                BColors.ERROR, error_msg, BColors.ENDC, search['error']))

    @staticmethod
    def raise_post_error(post, error_msg=None):
        if post.status_code not in [200, 201]:
            raise Exception('{}{} {} : {}'.format(
                BColors.ERROR, error_msg, BColors.ENDC, post.json()['error']))

    def get_all_documents_matching_query(self, url, query, extract_function=lambda x: x):
        search = self.get_json_response(
            search_url=url,
            json_data=query
        )
        self.raise_search_error(search, 'Get documents fail')

        scroll_id = search['_scroll_id']
        total_count = search['hits']['total']
        scrolled_documents = search['hits']['hits']
        documents_count = len(search['hits']['hits'])

        while documents_count < total_count:
            query = {'scroll': '1m', "scroll_id": scroll_id}
            post = self.post_response(
                post_url='/_search/scroll',
                json_data=query
            ).json()
            scroll_id = post['_scroll_id']
            scrolled_documents += post['hits']['hits']
            documents_count += len(post['hits']['hits'])

        return extract_function(scrolled_documents)


class ExtractFunction():

    @staticmethod
    def document_id(documents):
        return [document['_id'] for document in documents]

    @staticmethod
    def document_source(documents):
        return [document['_source'] for document in documents]

    @staticmethod
    def document_type_source(documents):
        return [{'_type': document['_type'], '_source': document['_source']} for document in documents]

    @staticmethod
    def document_id_type_source(documents):
        return [
            {'_id': document['_id'], '_type': document['_type'], '_source': document['_source']}
            for document in documents
        ]
