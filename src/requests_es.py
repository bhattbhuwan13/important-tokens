import json
import os
import sys
from typing import Dict, List
from urllib import response

import requests

proxies = {"http": "", "https": ""}
ES_URL = sys.argv[2]
SIZE_LIMIT = 2245


class ElasticSearch:
    def __init__(self, index_name) -> None:
        self.index_name = index_name
        self.headers = {"content-type": "application/json"}

    @staticmethod
    def get_formatted_data(raw_data: json, hits=False) -> Dict:
        result = json.loads(raw_data.text)
        if hits:
            return result["hits"]["hits"]
        else:
            return result

    def get_required_data(self) -> List:
        URL = f"{ES_URL}/{self.index_name}/_search?size={SIZE_LIMIT}"
        query = json.dumps(
            {
                "_source": ["devnet_folder_name_path", "content", "url"],
                "query": {"match": {"filetype": "word"},  "match": {"filetype": "pdf"}},
            }
        )
        try:
            response = requests.get(
                URL, data=query, headers=self.headers, proxies=proxies, verify=False
            )
            formatted_data = self.get_formatted_data(response, hits=True)

            print("The formatted data length is", len(formatted_data))
            filepath = [
                "開発コックピットサイト/開発CP/開発CP（NRI-協力会社共用）/50.保守/20_テスト環境作業エビデンス",
                "開発コックピットサイト/開発CP/開発CP（NRI-協力会社共用）/50.保守/10_本番環境作業エビデンス",
            ]
            formatted_data_cleaned = [
                data
                for data in formatted_data
                if filepath[0] not in data
                and filepath[1] not in data["_source"]["devnet_folder_name_path"]
                and len(data["_source"]["content"]) > 20
            ]

            print("The len of cleaned formatted data is", len(formatted_data_cleaned))

            return formatted_data_cleaned
        except:
            print("Inside exception")

    def tokenizer(self, text: str, analyzer_name: str) -> Dict:
        URL = f"{ES_URL}/{self.index_name}/_analyze"
        data = json.dumps({"analyzer": analyzer_name, "text": str(text)})
        response = requests.get(
            URL, data=data, headers=self.headers, proxies=proxies, verify=False
        )
        formatted_data = self.get_formatted_data(response)
        return formatted_data

    def get_doc_details_from_doc_id(self, ids: str) -> Dict:
        URL = f"{ES_URL}/{self.index_name}/_search?size={SIZE_LIMIT}"
        params = json.dumps(
            {
                "query": {"term": {"_id": {"value": ids}}},
            }
        )
        try:
            response = requests.get(
                URL, data=params, headers=self.headers, proxies=proxies, verify=False
            )
            formatted_data = self.get_formatted_data(response, hits=True)
            doc_details = {}
            doc_details["url"] = formatted_data[0]["_source"]["url"]
            doc_details["title"] = formatted_data[0]["_source"]["title"]
            doc_details["devnet_folder_name_path"] = formatted_data[0]["_source"][
                "devnet_folder_name_path"
            ]
            doc_details["content"] = formatted_data[0]["_source"]["content"]
            return doc_details
        except:
            print("Inside the exception block")

    def refresh_es(self) -> None:
        URL = f"{ES_URL}/{self.index_name}/_refresh"
        data = requests.get(URL, headers=self.headers, proxies=proxies, verify=False)
        print(f"Refreshed Elasticsearch...")

    def update_data(self, data: Dict, es_id: str) -> str:
        self.refresh_es()
        URL = f"{ES_URL}/{self.index_name}/_update/{es_id}"
        data = json.dumps(data)

        try:
            response = requests.post(
                URL, data=data, headers=self.headers, proxies=proxies, verify=False
            )
            return "Updated"

        except:
            return "Inside Exception block"


    def get_tokens_from_es(self, text: str):
        tokens = []
        response = self.tokenizer(text, "japanese_analyzer")
        for item in response["tokens"]:
            tokens.append(item["token"])

        return tokens
