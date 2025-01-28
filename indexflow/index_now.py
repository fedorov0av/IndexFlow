import httpx

SEARCH_INGINES = {
    "IndexNow": "https://yandex.ru/search/?text=url-changed&key=your-key",
    "Bing": "https://www.bing.com/indexnow?url=url-changed&key=your-key",
    "Naver": "https://www.bing.com/indexnow?url=url-changed&key=your-key",
    "Seznam": "https://search.seznam.cz/indexnow?url=url-changed&key=your-key",
    "Yandex": "https://yandex.com/indexnow?url=url-changed&key=your-key",
    "Yep": "https://indexnow.yep.com/indexnow?url=url-changed&key=your-key",
}

class IndexNow:
    def __init__(self, token: str):
        self.token = token
        self.client = httpx.AsyncClient()
    