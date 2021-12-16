import os
import json
from utils.search import query_text
from underthesea import word_tokenize
from tqdm import tqdm

with open('./data/public_test_question.json','r') as f:
    q = json.load(f)

with open('vietnamese-stopwords.txt','r',encoding='utf-8') as f:
    cachedStopWords = f.read()

def run_elastic_search():
    pass

def testFuncNew(text):
    text = ' '.join([word for word in text.split() if word not in cachedStopWords])
    return text

cnt = 0
with open('public_test_top25.txt','a+') as f:
    for question in tqdm(q['items']):
        query = question['question']
        # query = testFuncNew(query)
        query = word_tokenize(query,format='text')
        # if len(query.split(' ')) < 10:
        #     cnt += 1
        #     run_elastic_search()
        # else:
        res = query_text(query,25)
        for item in res['hits']['hits']:
            pid = item['_id']
            passage = item['_source']['text']
            # if len(passage.split(' ')) < 50:
            #     continue
            s = question['question_id']+"\t"+pid+"\t"+query+"\t"+passage
            f.write(s)
            f.write('\n')

print("{} short question search by elasticsearch".format(str(cnt)))
print("{} long question search by Colbert".format(len(q['items'])-cnt))