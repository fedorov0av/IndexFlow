import re
import httpx
import requests

SEARCH_ENGINES = {
    "IndexNow": "https://api.indexnow.org/indexnow",
    "Bing": "https://www.bing.com/indexnow",
    "Yandex": "https://yandex.com/indexnow",
    "Naver": "https://searchadvisor.naver.com/indexnow",
    "Seznam": "https://search.seznam.cz/indexnow",
    "Yep": "https://indexnow.yep.com/indexnow",
}

class IndexNow:
    def __init__(self, key: str, host: str, all_search_engines: bool = False) -> None:
        self.key: str = key
        self.host: str = host
        self.search_engines: dict = SEARCH_ENGINES
        self.all_search_engines: bool = all_search_engines

    def get_json(self, url: str) -> dict:
        host = self.get_host_name(self.host)
        return {
                'host': host,
                'key': self.key,
                'keyLocation': f'{self.host}/{self.key}.txt',
                'urlList':[
                    url
                ]
                }

    async def async_add_to_index(self, url: str) -> list[httpx.Response]:
        """
        HTTP Response Codes for IndexNow API:

        - 200 OK:
            URL submitted successfully.
        
        - 202 Accepted:
            URL received. IndexNow key validation pending.
        
        - 400 Bad Request:
            Invalid format in the request.
        
        - 403 Forbidden:
            The key is not valid (e.g. key not found, file found but key not in the file).
        
        - 422 Unprocessable Entity:
            URLs that don’t belong to the host or the key does not match the schema in the protocol.
        
        - 429 Too Many Requests:
            Too many requests, potential spam detected.
        """
        json = self.get_json(url)
        async_client = httpx.AsyncClient()
        responses = []
        for search_engine_key in self.search_engines:
            search_engine_url = self.search_engines[search_engine_key]
            search_engine_host = self.get_host_name(search_engine_url)
            response = await async_client.post(
                self.search_engines[search_engine_key],
                headers={'Content-Type': 'application/json', 'charset': 'utf-8', 'Host': search_engine_host},
                json=json
            )
            responses.append(response)
            if not self.all_search_engines:
                break
        return responses
        
    def add_to_index(self, url: str) -> list[requests.Response]:
        """
        HTTP Response Codes for IndexNow API: See the docstring for the method async_add_to_index.
        """
        json = self.get_json(url)
        session = requests.Session()
        responses = []
        for search_engine_key in self.search_engines:
            search_engine_url = self.search_engines[search_engine_key]
            search_engine_host = self.get_host_name(search_engine_url)
            response = session.post(
                self.search_engines[search_engine_key], 
                headers={'Content-Type': 'application/json', 'charset': 'utf-8', 'Host': search_engine_host},
                json=json
            )
            responses.append(response)
            if not self.all_search_engines:
                break
        return responses
    
    @staticmethod
    def get_host_name(url: str, need_http: bool=False) -> str:
        pattern = r"https?://([a-zA-Z0-9.-]+)"
        match = re.match(pattern, url)
        if need_http:
            return match.group(0)
        else:
            return match.group(1)