import json 
import os
from utils.search import get_doc_by_lawid
from tqdm import tqdm
from underthesea import word_tokenize


with open('submission.json','r') as f:
    data = json.load(f)

with open('./data/public_test_question.json','r') as f:
    q = json.load(f)

cnt = 0
with open('second.txt','a+') as f:
    for question in tqdm(q['items']):
        query = question['question']
        # query = testFuncNew(query)
        query = word_tokenize(query,format='text')
        # if len(query.split(' ')) < 10:
        #     cnt += 1
        #     run_elastic_search()
        # else:
        total_res = []
        for item in data:
            if item['question_id'] == question['question_id']:
                for i in item['relevant_articles']:
                    res = get_doc_by_lawid(i['law_id'])
                    for j in res:
                        pid = j['_id']
                        passage = j['text']['text']
                        # if len(passage.split(' ')) < 50:
                        #     continue
                        s = question['question_id']+"\t"+pid+"\t"+query+"\t"+passage
                        f.write(s)
                        f.write('\n')
            
