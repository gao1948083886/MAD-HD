# split a text string into sentences

from nltk.tokenize import sent_tokenize
import nltk


class SentenceSplitter:
    def __init__(self):
        pass

    # use NLTK to split a text string into sentences for now
    def split_into_sentences(self, text):
        return sent_tokenize(text)
