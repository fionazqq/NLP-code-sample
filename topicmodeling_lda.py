# -*- coding: utf-8 -*-
"""TopicModeling - LDA

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iwkj_xvRjH35vuEUmsaf3rs7zQjANz9R
"""

# Commented out IPython magic to ensure Python compatibility.
## import packages
import pandas as pd
import numpy as np 
from nltk.corpus import stopwords;
import matplotlib.pyplot as plt

import csv
import io
import string
import pickle

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess

!pip install pyLDAvis
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
# %matplotlib inline

# Remove punctuation
def remove_punctuation(text):
    no_punct=[words for words in text if words not in string.punctuation]
    words_wo_punct=''.join(no_punct)
    words_wo_punct = words_wo_punct.rstrip(words_wo_punct[-1])
    return words_wo_punct

case['customercomments']=case['customercomments'].apply(lambda x: remove_punctuation(x))



# Remove digit 
def remove_digit(text):
  no_digit=[words for words in text if not words.isdigit()]
  words_wo_digit = ''.join(no_digit).strip().replace('  ',' ')
  return words_wo_digit

case['customercomments']=case['customercomments'].apply(lambda x: remove_digit(x))


# Tokenize for topic modeling
import re
def tokenize(text):
    words_split=re.split("\W+",text) 
    return words_split
case['clned_comments']=case['customercomments'].apply(lambda x: tokenize(x.lower()))


# Remove stopwords (words that are unnecessary) for topic modeling

nltk.download('stopwords')
stop_words = stopwords.words('english')
stop_words.extend(['customer', 'mcdonalds','mcdonald','n','said', 'get', 'told', 'didnt','wrote','go', 'please', 'got',
                   'im','ive','global','advised','yes','refer','wont'])

def remove_stopwords(text):
  words_wo_stopwords = [words for words in text if words not in stop_words]
  return words_wo_stopwords

case['clned_comments'] = case['clned_comments'].apply(lambda x: remove_stopwords(x))

sample = case['clned_comments'].values.tolist()
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

words = list(sent_to_words(sample))

# Create Dictionary
id2word = corpora.Dictionary(words)
# Create Corpus
texts = words
# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]

#%% run the lda model 
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=7, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

from pprint import pprint
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

pyLDAvis.enable_notebook()
vis = gensimvis.prepare(lda_model, corpus, id2word)
vis

corpus_lda = lda_model[corpus]
all_topics = lda_model.get_document_topics(corpus_lda, minimum_probability=0.0)
all_topics_csr = gensim.matutils.corpus2csc(all_topics)
all_topics_numpy = all_topics_csr.T.toarray()
all_topics_df = pd.DataFrame(all_topics_numpy)