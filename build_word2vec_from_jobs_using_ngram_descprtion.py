from datetime import datetime
from db import *
from gensim.models import Word2Vec

from gensim.models import Phrases
import gensim

l=student_resumes.distinct("preprocessed")
documents=[]
for i in l:
    documents.append(i.split())
l=student_resumes.distinct("ngram_descrption")

for i in l:
    documents.append(i.split())
print len(documents)

l=petroleum_jobs.find({})
for i in l:
    documents.append(i["preprocessed_data"].split())
    documents.append(i["ngram_descrption"].split())
#### build the word2vec using documents which has list of words
try:
    model = Word2Vec.load("resume_word2vec5.model")
    model.build_vocab(documents, update=True)

except:
    model = gensim.models.Word2Vec(documents, size=50, window=5, min_count=1, workers=250, max_vocab_size=None)
    # model.build_vocab(documents)


model.train(documents, total_examples=len(documents), epochs=500)
print("training is complete")
model.save("resume_word2vec5.model")
print("list:", list(model.wv.vocab))