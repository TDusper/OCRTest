from whoosh.fields import Schema, TEXT
from whoosh import index
from whoosh import scoring
import os.path
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
schema = Schema(content=TEXT(stored=True))
ix = index.create_in("indexdir", schema)

with open("recognized.txt", "r", encoding='utf-8') as input:
    input = input.read().split("\n\n\n\n\n")
print(len(input))

writer = ix.writer()
for doc in input:
    writer.add_document(content=u"{}".format(doc))
writer.commit()

from whoosh.qparser import QueryParser
with ix.searcher(weighting=scoring.BM25F) as searcher:
    query = QueryParser("content", ix.schema).parse("He")
    results = searcher.search(query, terms=True, limit=15 )
    print(len(results))
    for r in results:
        print(r, r.score)