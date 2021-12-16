import os
import json
from utils.search import query_text,query_title,get_doc_by_lawid_and_articleid
from underthesea import word_tokenize
import random
from tqdm import tqdm


with open('data/train_question_answer.json','r') as f:
    data = json.load(f)


def create_triple_pair(query,positive=[],n_generate=100):
    query = word_tokenize(query,format='text')
    res = query_text(query,1000)
    lst_res = []
    negative_list = [x['_source']['text'] for x in res['hits']['hits'][100:350]]
    for item in range(n_generate):
        s = "" + query+"\t"
        pos = random.sample(positive,1)
        s = s + pos[0] + "\t"
        neg = random.sample(negative_list,1)
        s = s + neg[0]
        lst_res.append(s)
    return lst_res

def create_hard_triple_pair(query,positive=[],n_generate=20):
    query = word_tokenize(query,format='text')
    res = query_text(query,500)
    lst_res = []
    negative_list = []
    for item in res['hits']['hits']:
        if item['_source']['text'] not in positive:
            negative_list.append(item['_source']['text'])

    
    for item in range(n_generate):
        s = "" + query+"\t"
        pos = random.sample(positive,1)
        s = s + pos[0] + "\t"
        neg = negative_list[item+10]
        s = s + neg
        lst_res.append(s)
    return lst_res
    
        


for item in tqdm(data['items']):
    lst_relevant = []
    for i in item['relevant_articles']:
        lst_relevant += get_doc_by_lawid_and_articleid(i['law_id'],i['article_id'])
    lst_relevant = [x['text'] for x in lst_relevant]
    triples = create_hard_triple_pair(item['question'],lst_relevant,50)
    with open('triples_hard_10.txt','a+') as f:
        for it in triples:
            f.write(it)
            f.write('\n')
# create_triple_pair("Công an xã xử phạt lỗi không mang bằng lái xe có đúng không?")
