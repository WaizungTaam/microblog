from flask import current_app

def elasticsearch_required(func):
    def wrapper(*args, **kwargs):
        if current_app.elasticsearch:
            return func(*args, **kwargs)
    return wrapper

@elasticsearch_required
def add_to_index(index, model):
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
        current_app.elasticsearch.index(
            index=index, doc_type=index, id=model.id, body=payload)

@elasticsearch_required
def remove_from_index(index, model):
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)

@elasticsearch_required
def query_index(index, query, page, per_page):
    search = current_app.elasticsearch.search(
        index=index, body={
            'query': {
                'multi_match': {
                    'query': query,
                    'fields': ['*']
                }},
            'from': (page - 1) * per_page,
            'size': per_page
        })
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']
