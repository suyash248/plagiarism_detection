__author__ = "Suyash Soni"
__email__ = "suyash.soni248@gmail.com"

from model import Document
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from util.injector import inject
from service.base import BaseService
from service.plag_dao import PlagiarismDAO
from typing import List, Dict

class PlagiarismDetector(BaseService):

    plag_dao: PlagiarismDAO = inject(PlagiarismDAO)
    vectorizer = None

    @staticmethod
    def tokenize_and_stem(doc):
        punctuation_remover = dict((ord(char), None) for char in string.punctuation)
        tokens = nltk.word_tokenize(doc.lower().translate(punctuation_remover))
        return PlagiarismDetector.stem_tokens(tokens)

    @staticmethod
    def stem_tokens(tokens):
        stemmer = nltk.stem.porter.PorterStemmer()
        stemmed_tokens = [stemmer.stem(item) for item in tokens]
        return stemmed_tokens

    def cosine_similarity(self, source_doc, input_doc):
        vectorizer = self.vectorizer or TfidfVectorizer(tokenizer=PlagiarismDetector.tokenize_and_stem, stop_words='english')
        tfidf = vectorizer.fit_transform([source_doc, input_doc])
        return ((tfidf * tfidf.T).A)[0, 1]

    def compute_similarity(self, input_doc) -> Dict:
        most_similar_so_far = dict(similarity_score=-1, doc=None)

        for doc_info in self.plag_dao.yield_docs():
            docs: List[Document] = doc_info['data']

            for doc in docs:
                similarity_score = self.cosine_similarity(doc.content, input_doc)
                if similarity_score > most_similar_so_far['similarity_score']:
                    most_similar_so_far['similarity_score'] = similarity_score
                    most_similar_so_far['doc'] = doc
        return most_similar_so_far