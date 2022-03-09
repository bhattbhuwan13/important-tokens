import json
import os
import sys
from typing import Dict, List

import numpy as np
import tinysegmenter
from sudachipy import Dictionary

from src.okapi_scoring.tfidf import (
    compute_tfidf_score,
    compute_tfidf_vectorizer,
    get_tfidf_stopwords,
    get_top_tfidf_tokens,
)
from src.preprocess import PreprocessData
from src.requests_es import ElasticSearch

# from src.okapi_bm25 import BM25
from src.token_scorer import BM25Scorer, TFIDFScorer, TokenScorer


def sort_tokens_by_score(tokens_with_score: Dict):

    sorted_token_score = sorted(
        tokens_with_score.items(), key=lambda item: item[1]
    )
    sorted_tokens_list = [token for token, score in sorted_token_score]
    return sorted_tokens_list


def compute_number_of_special_words(fraction: float, total_tokens: int):
    return int(fraction * total_tokens)


def get_special_and_stop_words(Scorer: TokenScorer, tokenized_texts):
    scorer = Scorer(tokenized_texts=tokenized_texts)

    token_scores = scorer.score_tokens()
    sorted_tokens = sort_tokens_by_score(token_scores)
    NUMBER_OF_SPECIAL_WORDS = compute_number_of_special_words(
        0.01, len(sorted_tokens)
    )
    important_words = sorted_tokens[-NUMBER_OF_SPECIAL_WORDS:]
    stop_words = sorted_tokens[:NUMBER_OF_SPECIAL_WORDS]
    return important_words, stop_words


def main(content: List) -> List:
    """Initialize model and compute the similarities among the docs.

    Args:
        crl (PycurlHelper): Instance of PycurlHelper to access ElasticSearch.
        content (List): Contents of _content field in the ES database.
        ids (List): content of the _id field in ES database.

    Returns:
        List: Similarity score along with the Corpus ID.
    """
    cleaned_list = preprocess_data.clean_list(content)
    tokenized_texts = preprocess_data.tokenize_content(cleaned_list)
    ## Okapi Implementation
    # breakpoint()

    (
        nri_specific_important_words,
        nri_specific_stop_words,
    ) = get_special_and_stop_words(BM25Scorer, tokenized_texts=tokenized_texts)

    # tf_nri_specific_important_words, tf_nri_specific_stop_words = get_special_and_stop_words(
    #     TFIDFScorer, tokenized_texts=tokenized_texts
    # )

    print("Okapi important words", nri_specific_important_words)
    print("Okapi stopwords", nri_specific_stop_words)

    ## TFIDF implementation------------Needs refactoring
    tinysegmenter_tokenizer = tinysegmenter.TinySegmenter()
    stop_words = preprocess_data.get_stopwords()
    tfidf_vectorizer = compute_tfidf_vectorizer(
        stop_words, tinysegmenter_tokenizer
    )
    tfidf_score = compute_tfidf_score(tfidf_vectorizer, cleaned_list)
    tfidf_important_words = get_top_tfidf_tokens(tfidf_score, tfidf_vectorizer)
    tfidf_stopwords = get_tfidf_stopwords(tfidf_score, tfidf_vectorizer)
    print("TFIDF important words", tfidf_important_words)
    print("TFIDF stop words", tfidf_stopwords)


if __name__ == "__main__":
    INDEX_NAME = sys.argv[1]
    crl = ElasticSearch(INDEX_NAME)
    preprocess_data = PreprocessData(crl)

    print("Retreving all data ...")
    input_data = crl.get_required_data()
    print("Preprocessing.....")
    content, _, ids = preprocess_data.extract_data(input_data)
    main(content)
    # get_similar_docs(crl, content, ids)
