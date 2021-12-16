import os
import json
from utils.search import query_by_id,query_text
from tqdm import tqdm
from underthesea import word_tokenize

with open('./data/public_test_question.json','r') as f:
    q = json.load(f)


def retrieve_rank(result_file):
    with open(result_file,'r') as f:
        rerank = f.read().split('\n')
    lst_top10 = {}
    for item in rerank:
        try:
            qid , pid , rank, score = item.split('\t')
            if qid not in lst_top10.keys():
                lst_top10[qid] = []
            if int(rank) <= 2: # number of docs we take to submit
                lst_top10[qid].append(pid)
        except:
            continue
    return lst_top10

def retrieve_rank_dynamic(result_file,threshold=21):
    with open(result_file,'r') as f:
        rerank = f.read().split('\n')
    lst_top10 = {}
    for item in rerank:
        try:
            qid , pid , rank, score = item.split('\t')
            if qid not in lst_top10.keys():
                lst_top10[qid] = []
                lst_top10[qid].append(pid)
                continue
            if score >= threshold: # number of docs we take to submit
                lst_top10[qid].append(pid)
        except:
            continue
    return lst_top10

# colbert_result = retrieve_rank('../ColBERT/experiments/dirty/test.py/2021-12-06_15.48.25/ranking.tsv')
colbert_result = retrieve_rank('../ColBERT/experiments/dirty/test.py/2021-12-06_15.48.25/ranking.tsv')



submission = []
for question in tqdm(q['items']):
    query = question['question']
    query = word_tokenize(query,format='text')
    # if len(query.split(' ')) < 10:
    #     res = query_text(query,2)
    #     lst_relevant = []
    #     for s in res['hits']['hits']:
    #         lst_relevant.append(s['_source']['law_id']+","+s['_source']['article_id'])
    #     lst_relevant = list(set(lst_relevant))
    #     filtered_lst_relevant = []
    #     for s in lst_relevant:
    #         law_id , article_id = s.split(',')
    #         filtered_lst_relevant.append({"law_id" : law_id,
    #                             "article_id":article_id})
    #     submission.append({"question_id":question['question_id'],"relevant_articles":filtered_lst_relevant})
    # #     # break
    # else:
    lst_relevant_id = colbert_result[question['question_id']]
    lst_relevant = []
    for i in lst_relevant_id:
        qr = query_by_id(i)
        lst_relevant.append(qr['law_id']+","+qr['article_id'])
    lst_relevant = list(set(lst_relevant))
    filtered_lst_relevant = []
    for s in lst_relevant:
        law_id , article_id = s.split(',')
        filtered_lst_relevant.append({"law_id" : law_id,
                            "article_id":article_id})
    submission.append({"question_id":question['question_id'],"relevant_articles":filtered_lst_relevant})

print(q['_count_'])
print(len(submission))

with open('submission.json', 'w') as f:
    f.write(json.dumps(submission))

        

# print(submission)
# retrieve_rank('../ColBERT/experiments/dirty/test.py/2021-12-02_14.27.20/ranking.tsv')