from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
import string
import math
from nltk.stem import PorterStemmer

stop_words=stopwords.words('english')
def get_wordnet_pos(tag_parameter):

    tag = tag_parameter[0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)
def data_proccesing(file,csv_reader):
    stop_words=stopwords.words('english')
    document_of_terms = [],
    texts_list=[]
    for row in csv_reader:
        text_id=row[0]
        text=row[1]
        text = text.lower()
        new_tokens = []
        for token in text.split():
            new_tokens.append(token.translate(str.maketrans('', '', string.punctuation)))
        tokenized_documents = word_tokenize(text)
        pos_tags = pos_tag(tokenized_documents)
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) for word, tag in pos_tags]
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in lemmatized_words]
        terms=[]
        for word in stemmed_words:
            if word not in stop_words:
                terms.append(word)
        texts_list.append(terms)
    return texts_list;
