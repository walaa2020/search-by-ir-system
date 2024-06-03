import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import string
from nltk.stem import PorterStemmer

from data_processing import get_wordnet_pos
def clean_query(text):
    stop_words=stopwords.words('english')
    document_of_terms = [],
    texts_list=[]
    text = text.lower()
    new_tokens = []
    for token in text.split():
        new_tokens.append(token.translate(str.maketrans('', '', string.punctuation)))
    tokenized_documents = word_tokenize(text)
    pos_tags = pos_tag(tokenized_documents)
        # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in pos_tags]
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in lemmatized_words]


    terms=[]
    for word in stemmed_words:
        if word not in stop_words:
            terms.append(word)
    texts_list.append(terms)
    return terms;
def join_strings(string_list): 
    string_list = [str(item) for item in string_list]
    return ' '.join(string_list)
def get_w_tf(x):
    try:
        return math.log10(x)+1
    except:
        return 0