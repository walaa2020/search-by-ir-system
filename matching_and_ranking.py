import csv
import math
import pandas as pd
from data_processing import data_proccesing
from data_represntation import all_word_list, get_term_freq
from indexin import f_document_length, f_normlized_term_freq_idf, ftdf, get_weighted_term_freq, update_term_freq
from query_processing import clean_query, get_w_tf, join_strings

def f_product2(q,normlized_term_freq_idf,tfd):  
    query= pd.DataFrame(index=normlized_term_freq_idf.index)
    s=[]
    for x in normlized_term_freq_idf.index:
        if x in q.split() :
            s.append(1)
        else:
            s.append(0)
    query['tf']=s
    query['w_tf']=query['tf'].apply(lambda x:get_w_tf(x))
    product = normlized_term_freq_idf.multiply(query['w_tf'], axis=0)
    query['idf'] = tfd['idf'] * query['w_tf']
    query['tf_idf'] = query['w_tf'] * query['idf']
    query['normalized'] = 0
    for i in range(len(query)):
        if math.sqrt(sum(query['idf'].values**2))==0:
#             print("not found")
            pass
        else:
            query['normalized'].iloc[i] = float(query['idf'].iloc[i]) / math.sqrt(sum(query['idf'].values**2))
    # print('Query Details')
    #     print(query.loc[new_q])
    product2 = product.multiply(query['normalized'], axis=0)
    return product2

def Matching_and_ranking(query,file):
    rr=clean_query(query)
    query = join_strings(rr)
    if file and file.filename.endswith('.csv'):
        csv_data = file.read().decode('utf-8')
        reader = csv.reader(csv_data.splitlines())
        texts_list=data_proccesing(file,reader)
        print(texts_list)
        all_words=all_word_list(texts_list)
        term_freq=pd.DataFrame(get_term_freq(texts_list[0],all_words).values(),index=get_term_freq(texts_list[0],all_words).keys())
        term_freq=update_term_freq(texts_list,term_freq,all_words)
        for i in range(1,len(texts_list)+1):
            term_freq['doc'+str(i)]= term_freq['doc'+str(i)].apply(get_weighted_term_freq)
        tfd=ftdf(term_freq)
        trem_freq_inve_doc_freq=term_freq.multiply(tfd['idf'],axis=0)
        document_length=f_document_length(trem_freq_inve_doc_freq)
        normlized_term_freq_idf=f_normlized_term_freq_idf(trem_freq_inve_doc_freq,document_length)
        product2=f_product2(query,normlized_term_freq_idf,tfd)
        scores = {}
        # قم بتحويل النص q إلى قائمة من الكلمات (افترض أن q هو نص)
        q_list = query.split()
        # تحقق من وجود الصفوف التي تتطابق مع الكلمات في q_list في DataFrame
        # for i, col in enumerate(product2.columns):
        #     if i < len(product2.columns) - 1:  # تأكد من عدم التجاوز للعمود الأخير
        #         next_col = product2.columns[i + 1]
        #         if not (0 in product2[col].loc[q_list].values and 0 in product2[next_col].loc[q_list].values):
        #             scores[col] = product2[col].sum()
        for col in product2.columns:
            col_values = product2[col].loc[q_list].values if q_list[0] in product2.index else []
            if any(value != 0 for value in col_values):  # التحقق من وجود قيم غير صفرية
                scores[col] = product2[col].sum()       
            
        prod_res=product2[list(scores.keys())].loc[query.split()]
        prod_res.sum()
        final_scores=sorted(scores.items(),key=lambda x:x[1],reverse=True)
        c=[]
        for doc in final_scores:
            c.append(doc[0])
        result=[int(item.replace('doc', '')) for item in c]
        return result
          