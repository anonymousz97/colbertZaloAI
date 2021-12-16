from elasticsearch import Elasticsearch
from underthesea import word_tokenize
es = Elasticsearch()


def query_text(question,n_docs=1000,index='legal_search'):
    # question = word_tokenize(question,format='text')
    query = {
        "match": {
            "text": question
        }
    }
    res = es.search(index=index, query=query,size=n_docs)
    return res


def query_title(question,n_docs=1000,index='legal_search'):
    # question = word_tokenize(question,format='text')
    query = {
        "match": {
            "title": question
        }
    }
    res = es.search(index=index, query=query,size=n_docs)
    return res

def query_by_id(id,index='legal_search'):
    res = es.get(index=index, id=id)
    return res['_source']


def get_doc_by_lawid_and_articleid(law_id,article_id,index='legal_search'):
    query = {
        "bool": {
            "must": [
                {
                "match": {
                    "law_id": law_id
                }
                },
                {
                "match": {
                    "article_id": article_id
                }
                },
            ]
        }
    }
    res = es.search(index=index, query=query,size=100)
    lst_res = []
    for hit in res['hits']['hits']:
        if hit['_source']['law_id'] == law_id and hit['_source']['article_id'] == article_id:
            lst_res.append(hit['_source'])
    return lst_res

def get_doc_by_lawid(law_id,index='legal_search'):
    query = {
        "bool": {
            "must": [
                {
                "match": {
                    "law_id": law_id
                }
                }
            ]
        }
    }
    res = es.search(index=index, query=query,size=1000)
    lst_res = []
    for hit in res['hits']['hits']:
        if hit['_source']['law_id'] == law_id:
            lst_res.append({"_id":hit['_id'],'text':hit['_source']})
    return lst_res