# cse.py
Asyncio API wrapper for the [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/overview).
# Installation

#### PIP
`pip install -U cse.py`
#### GIT
`pip3 install -U git+https://github.com/Hype3808/cse.py`
# Usage
```python
import cse

client = cse.Engine("Your API Key") # create the Search client (uses Google by default!)

results = await client.search("Python", safesearch=False) # returns a list of cse.Result objects

print(results[0].title, results[0].description, results[0].url, results[0].image_url) # Title, snippet, URL, and Image URL

await client.close() # Run this when cleaning up.
```
# Getting image results
```python
import cse

client = cse.Engine("Your API Key") # create the Search client (uses Google by default!)

results = await client.search("Python", safesearch=False, image_search=True) # returns a list of cse.Result objects

print(results[0].title, results[0].description, results[0].url, results[0].image_url) # Title, snippet, URL, and Image URL

await client.close() # Run this when cleaning up.
```
To use Search objects with a custom search engine, provide the ID of the search engine.
```python
cse.Engine("Your API Key", engine_id="015786823554162166929:mywctwj8es4")
```
SafeSearch can also be turned off by setting `safesearch=False` when using the `search()` method.
# Getting an API key
You can get an API key by going [here](https://developers.google.com/custom-search/v1/overview#api_key) and scrolling down to the **API key** section.

<a href=https://developers.google.com/custom-search/v1/overview#api_key target=_blank>![Get API key](https://i.imgur.com/pHXFiI8.png)</a>
