# colbertZaloAI
Zalo AI Challenge Legal search using Colbert (around 0.65 F2)
<br>Modified ColBERT version for this task

This need elasticsearch for saving all the legal rules and docs (file legal_search/utils/elasticsearch_demo.py)
And create hard pairs using top-n results from elasticsearch by cosin-similarity.
