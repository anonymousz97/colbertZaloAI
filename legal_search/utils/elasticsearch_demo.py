from datetime import datetime
import json
import os
from tqdm import tqdm
from underthesea import word_tokenize
from elasticsearch import Elasticsearch
es = Elasticsearch()

with open('../data/legal_corpus.json','r') as f:
    legal_corpus = json.load(f)

def create_docs(item):
    doc_format = {
        "law_id" : item['law_id'],
        "article_id" : "",
        "title" : "",
        "text" : ""
    }
    docs = []
    for it in item['articles']:
        it['text'] = word_tokenize(it['text'],format='text')
        it['title'] = word_tokenize(it['title'],format='text')
        cnt = len(it['text'].split(' ')) // 200
        for i in range(2):
            docs.append({
                "law_id" : item['law_id'],
                "article_id" : it['article_id'],
                "title" : it['title'],
                "text" : " ".join(it['text'].split(' ')[100*i:100*(i+1)])
            })
    return docs
            
cnt = 0
for item in tqdm(legal_corpus):
    #print(item['articles'])
    docs = create_docs(item)
    for doc in docs:
        cnt += 1
        res = es.index(index="legal_search_2", id=cnt, document=doc)
es.indices.refresh(index="legal_search_2")

# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': datetime.now(),
# }
# res = es.index(index="test-index", id=1, document=doc)
# print(res['result'])

# res = es.get(index="test-index", id=1)
# print(res['_source'])

# es.indices.refresh(index="test-index")

# res = es.search(index="test-index", query={"match_all": {}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])