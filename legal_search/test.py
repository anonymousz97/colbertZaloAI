from utils.search import query_title,query_text
from underthesea import word_tokenize
import os
from tqdm import tqdm
import json

# with open('./data/train_question_answer.json','r') as f:
#     q = json.load(f)
# #print(q.keys())


# eps = 1e-6
# # for n_docs in [3,5,10,15,20,25]:
# #     avg_f2 = 0.0
# #     for question in tqdm(q['items']):
# #         query = question['question']
# #         query = word_tokenize(query,format='text')
# #         res = query_title(query,n_docs,"legal_search_2")
# #         lst_relevant = []
# #         for s in res['hits']['hits']:
# #             lst_relevant.append(s['_source']['law_id']+","+s['_source']['article_id'])
# #         lst_relevant = list(set(lst_relevant))
# #         groundtruth = [x['law_id']+","+x['article_id'] for x in question['relevant_articles']]
# #         count = 0
# #         for i in lst_relevant:
# #             if i in groundtruth:
# #                 count += 1
# #         precision = 1.0*count/len(lst_relevant)
# #         recall = 1.0*count/len(groundtruth)
# #         f2_score = (5 * precision * recall) / (4* precision + recall+eps)
# #         avg_f2 += f2_score

# #     print("Elasticsearch query by title {} docs : {}".format(n_docs,avg_f2/q['_count_']))

# # for n_docs in [3,5,10,15,20,25]:
# #     avg_f2 = 0.0
# #     for question in tqdm(q['items']):
# #         query = question['question']
# #         query = word_tokenize(query,format='text')
# #         res = query_text(query,n_docs,"legal_search_2")
# #         lst_relevant = []
# #         for s in res['hits']['hits']:
# #             lst_relevant.append(s['_source']['law_id']+","+s['_source']['article_id'])
# #         lst_relevant = list(set(lst_relevant))
# #         groundtruth = [x['law_id']+","+x['article_id'] for x in question['relevant_articles']]
# #         count = 0
# #         for i in lst_relevant:
# #             if i in groundtruth:
# #                 count += 1
# #         precision = 1.0*count/len(lst_relevant)
# #         recall = 1.0*count/len(groundtruth)
# #         f2_score = (5 * precision * recall) / (4* precision + recall+eps)
# #         avg_f2 += f2_score

# #     print("Elasticsearch query by text {} docs : {}".format(n_docs,avg_f2/q['_count_']))

# def retrieve_rank(result_file,n_docs=5):
#     with open(result_file,'r') as f:
#         rerank = f.read().split('\n')
#     lst_top10 = {}
#     for item in rerank:
#         try:
#             qid , pid , rank = item.split('\t')
#             if qid not in lst_top10.keys():
#                 lst_top10[qid] = []
#             if int(rank) <= n_docs: # number of docs we take to submit
#                 lst_top10[qid].append(pid)
#         except:
#             continue
#     return lst_top10


# for n_docs in [3,5,10,15,20,25]:
#     colbert_result = retrieve_rank('../ColBERT/experiments/dirty/test.py/2021-12-03_00.39.00/ranking.tsv',n_docs)
#     avg_f2 = 0.0
#     for question in tqdm(q['items']):
#         query = question['question']
#         lst_relevant_id = colbert_result[question['question_id']]
#         lst_relevant = []
#         for i in lst_relevant_id:
#             qr = query_by_id(i,'legal_search_2')
#             lst_relevant.append(qr['law_id']+","+qr['article_id'])
#         lst_relevant = list(set(lst_relevant))
#         groundtruth = [x['law_id']+","+x['article_id'] for x in question['relevant_articles']]
#         count = 0
#         for i in lst_relevant:
#             if i in groundtruth:
#                 count += 1
#         precision = 1.0*count/len(lst_relevant)
#         recall = 1.0*count/len(groundtruth)
#         f2_score = (5 * precision * recall) / (4* precision + recall+eps)
#         avg_f2 += f2_score
#     print("Elasticsearch query by text {} docs : {}".format(n_docs,avg_f2/q['_count_']))


# ------------------------------------------------
from transformers import AutoTokenizer,AutoModel
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
model = AutoModel.from_pretrained("vinai/phobert-base")
tokenizer.save_pretrained('./local_model_directory/')
model.save_pretrained('./local_model_directory/')