def all_word_list(texts_list):
    all_words=[]
    for doc in texts_list:
        for word in doc:
            all_words.append(word)
    return all_words
def get_term_freq(doc,all_words):
    words_found=dict.fromkeys(all_words,0)
    for word in doc:
        words_found[word]+=1
    return words_found
