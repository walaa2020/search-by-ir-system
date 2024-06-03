import math

import numpy as np
import pandas as pd

from data_represntation import get_term_freq


def update_term_freq(texts_list,term_freq,all_words):
    for i in range(1,len(texts_list)):
        term_freq[i]=get_term_freq(texts_list[i],all_words).values()
    term_freq.columns=['doc'+str(i) for i in range(1,(len(texts_list)+1))]
    return term_freq

def get_weighted_term_freq(x):
    if x>0:
        return math.log(x)+1
    return 0
def ftdf(term_freq):  
    tfd=pd.DataFrame(columns=['freq','idf'])
    for i in range(len(term_freq)):
        frequency=term_freq.iloc[i].values.sum()
        tfd.loc[i,'freq']=frequency
        tfd.loc[i,'idf']=math.log(10/(float(frequency)))
    tfd.index=term_freq.index
    return tfd

def get_docs_legth(col,trem_freq_inve_doc_freq):
    return np.sqrt(trem_freq_inve_doc_freq[col].apply(lambda x: x**2).sum())
def f_document_length(trem_freq_inve_doc_freq):
    document_length=pd.DataFrame()
    for column in trem_freq_inve_doc_freq.columns:
        document_length.loc[0,column+'_len']=get_docs_legth(column,trem_freq_inve_doc_freq)
    return document_length 

def get_norm_tf_idf(col, x,document_length):
    try:
        return x / document_length[col+'_len'].values[0]
    except:
        return 0
def f_normlized_term_freq_idf(trem_freq_inve_doc_freq,document_length):
    normlized_term_freq_idf = pd.DataFrame()
    for col in trem_freq_inve_doc_freq.columns:
        normlized_term_freq_idf[col] = trem_freq_inve_doc_freq[col].apply(lambda x : get_norm_tf_idf(col, x,document_length))
    return normlized_term_freq_idf