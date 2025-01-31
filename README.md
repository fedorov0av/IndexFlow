# IndexFlow
A straightforward solution for quick content indexing using the IndexNow protocol.

## Installation

Install the package using pip:

```bash
poetry add git+https://github.com/fedorov0av/IndexFlow.git
```

## Usage

### Variables:

- `INDEXNOW_KEY`: Your unique API key for interacting with the IndexNow API. This key is used for authentication when adding URLs to the index.
- `page_url`: The URL of the page you want to submit to the search engine index. This should be a valid URL that is publicly accessible.

async:
```python
index_now = IndexNow(key=INDEXNOW_KEY, host=page_url)
responses = await index_now.async_add_to_index(page_url)
```
sync:
```python
index_now = IndexNow(key=INDEXNOW_KEY, host=page_url)
responses = await index_now.add_to_index(page_url)
```
