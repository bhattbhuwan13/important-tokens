from typing import List


class PreprocessData:
    @staticmethod
    def clean_documents(documents: List[str]) -> List[str]:
        """Removes unwanted newline and empty characters from a string

        Args:
            documents (List[str]): documents

        Returns:
            List[str]:
        """

        documents = [item.replace("\n", "").strip() for item in documents]
        return documents

    @staticmethod
    def tokenize_documents(documents: List[str]) -> List[List[str]]:
        """Tokenizes a given string by splitting them using space character

        Args:
            documents (List[List[str]]): documents

        Returns:
            List[List[str]]:
        """

        return [document.split() for document in documents]
