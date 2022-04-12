from typing import Dict, List, Tuple

from src.preprocess import PreprocessData
from src.token_scorer import BM25Scorer, TFIDFScorer, TokenScorer


def sort_tokens_by_score(tokens_with_score: Dict) -> List[str]:
    """Given a dictionary containing tokens and their score,

    Args:
        tokens_with_score (Dict): Dictionary containing tokens as key
        and scores as value.

    Returns:
        List[str]:
    """

    sorted_token_score = sorted(
        tokens_with_score.items(), key=lambda item: item[1]
    )
    return [token for token, score in sorted_token_score]


def compute_number_of_special_words(fraction: float, total_tokens: int) -> int:
    """Given a percentage as fraction, computes the number of special and stop words.

    Args:
        fraction (float): fraction
        total_tokens (int): total_tokens
    """
    return round(fraction * total_tokens)


def get_special_and_stop_words(
    scorer: TokenScorer,
) -> Tuple[List[str], List[str]]:
    """Computes the most and least significant words.

    Args:
        scorer (TokenScorer): The algorithm used for scoring the tokens.

    Returns:
        Tuple[List[str], List[str]]: List of most and least important words
    """

    token_scores = scorer.score_tokens()
    sorted_tokens = sort_tokens_by_score(token_scores)
    NUMBER_OF_SPECIAL_WORDS = compute_number_of_special_words(
        0.05, len(sorted_tokens)
    )
    important_words = sorted_tokens[-NUMBER_OF_SPECIAL_WORDS:]
    stop_words = sorted_tokens[:NUMBER_OF_SPECIAL_WORDS]
    return important_words, stop_words


def main(tokenized_texts: List[List[str]]):
    """Finds and prints the most and least significant words.

    Args:
        tokenized_texts (List[List[str]]): List containing list of tokens from each document
    """

    ## Okapi Implementation
    okapi_scorer = BM25Scorer(tokenized_texts)
    okapi_important_words, okapi_stop_words = get_special_and_stop_words(
        okapi_scorer
    )

    print("Okapi important words", okapi_important_words)
    print("Okapi stopwords", okapi_stop_words)

    ## TFIDF implementation

    tfidf_scorer = TFIDFScorer(tokenized_texts)
    tfidf_important_words, tfidf_stopwords = get_special_and_stop_words(
        tfidf_scorer
    )
    print("TFIDF important words", tfidf_important_words)
    print("TFIDF stop words", tfidf_stopwords)


if __name__ == "__main__":
    all_content = [
        """
            Media experts and journalists of South Asia have called for a systematic structural change in the media outlets of the region to break the bias and to accelerate women's equal participation in leadership roles.
            """,
        """
            Priya (name changed) a single mother, returned home to Nepal with a child she had given birth to in United Arab Emirates, with the hopes of providing identity to her offspring who had been denied birth registration in the country of her child's birth.
            """,
        """ 
            Two weeks into its war in Ukraine, Russia has achieved less and struggled more than anticipated at the outset of the biggest land conflict in Europe since World War II. But the invading force of more than 150,000 troops retains large and possibly decisive advantages in firepower as they bear down on key cities.
            """,
    ]

    data_preprocessor = PreprocessData()
    cleaned_contents = data_preprocessor.clean_documents(all_content)

    tokenized_contents = data_preprocessor.tokenize_documents(cleaned_contents)

    main(tokenized_contents)
