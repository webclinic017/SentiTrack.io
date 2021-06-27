import emoji
import re
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

def cleanText(text):
    """
    Applies pre-processing to text comment

    Steps:
        1. emoji to text
        2. remove html tags
        3. lowercase
        4. remove punctuation 
    """
    #demojize emojis
    text = emoji.demojize(text, delimiters=("", ""))

    # remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # convert text to lowercase
    text = text.strip().lower()
    
    # remove the characters [\], ['] and ["]
    text = re.sub(r"\\", "", text)    
    text = re.sub(r"\'", "", text)    
    text = re.sub(r"\"", "", text)   
    
    # replace punctuation characters with spaces
    filters ='!"\'#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n'
    translate_dict = dict((c, " ") for c in filters)
    translate_map = str.maketrans(translate_dict)
    text = text.translate(translate_map)

    return text

class TextCleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y = None):
        return self

    def transform(self, X):
        return pd.Series(X).apply(cleanText).values