from abc import ABC, abstractmethod

import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer


class TokenScorer(ABC):
    @abstractmethod
    def __init__(self, tokenized_texts):
        pass

    @abstractmethod
    def score_tokens(self):
        """Returns a dictionary containing tokens and their respective scores"""
        pass


class BM25Scorer(TokenScorer):
    def __init__(self, tokenized_texts):
        self.bm25 = BM25Okapi(tokenized_texts)
        return None

    def score_tokens(self):
        token_score = self.bm25.idf
        return token_score


class TFIDFScorer(TokenScorer):
    def __init__(self, tokenized_texts):
        self.tfidf_vectorizer = TfidfVectorizer(
            use_idf=True,
            max_df=0.5,
            tokenizer=lambda x: x,
            preprocessor=lambda x: x,
        )
        self.tf_idf_score = self.tfidf_vectorizer.fit_transform(
            tokenized_texts
        )
        return None

    def score_tokens(self):
        tfidf_feature_names = np.array(
            self.tfidf_vectorizer.get_feature_names_out()
        )
        tfidf_token_score = np.asarray(self.tf_idf_score.sum(axis=0)).ravel()
        token_score = dict(zip(tfidf_feature_names, tfidf_token_score))
        return token_score
