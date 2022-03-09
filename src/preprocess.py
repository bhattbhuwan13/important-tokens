from spacy.lang.ja.stop_words import STOP_WORDS as ja_stop
from spacy.lang.en.stop_words import STOP_WORDS as en_stop
# from sudachipy import SplitMode
from src.requests_es import ElasticSearch

# import tinysegmenter
import json
from typing import Dict, List


class PreprocessData:
    def __init__(self, crl):
        self.crl = crl

    def read_json(self, file_path):

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        return data

    def extract_data(self, raw_data: Dict) -> List:
        """Extract the news content.

        Args:
            raw_data (Dict): Input data.

        Returns:
            List: News content.
        """
        # breakpoint()
        content = [item["_source"]["content"] for item in raw_data]
        urls = [item["_source"]["url"] for item in raw_data]
        ids = [item["_id"] for item in raw_data]
        return content, urls, ids

    def get_stopwords(self):
        """Makes a list of stopwords.

        Args:
            stopwords_list (List): List of stopwords

        Returns:
            list: list of english and japanese stopwords
        """
        stopwords_list = list(ja_stop) + list(en_stop)
        return stopwords_list

    # def read_punc_file(self, file_path="./data/punc_file.txt"):

    #     my_file = open(file_path, "r")
    #     content = my_file.read()
    #     return content

    def clean_list(self, raw_news, new_stopwords=[]):
        """cleans the list of document

        Returns:
            List: List of cleaned document
        """

        stopwords_list = self.get_stopwords() + new_stopwords
        # punctuation = self.read_punc_file()
        # punctuation_list = punctuation.split("\n")
        punc = [
            "\u3000",
            "!",
            "(",
            "２",
            ")",
            "-",
            "[",
            "]",
            "{",
            "}",
            ";",
            ":",
            "'",
            '"',
            "\\",
            ",",
            " ",
            "<",
            ">",
            ".",
            "/",
            "?",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "_",
            "~",
            '"',
            "-",
            "-",
            ", ",
            "。",
            "・",
            "」",
            "、",
            "\n",
            "？",
            "「",
            "！",
        ]

        cleaned_list = [
            "".join(
                word
                for word in item
                if word not in punc and word not in stopwords_list and word.isalpha()
            )
            for item in raw_news
        ]
        return cleaned_list

    # def tokenize_text(self, text, tokenizer):

    #     tokenized_doc = [
    #         [article.surface() for article in tokenizer.tokenize(word, SplitMode.A)]
    #         for word in text
    #     ]

    #     return tokenized_doc[0]

    def tokenize_content(self, cleaned_news):

        """Tokenize the news using default analyzer of Elastic Search.

        Args:
            cleaned_news (List): Corpus containing news.

        Returns:
            List: Token list for each news in the corpus.
        """

        tokenized_news = [
            self.crl.get_tokens_from_es(value[:150000]) for value in cleaned_news
        ]

        return tokenized_news
