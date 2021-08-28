# cnnlite

## Description
`cnnlite` is a web scraper for CNN Lite. This package collects CNN Lite articles at https://lite.cnn.com.

## Installation
```bash
>>> pip install cnnlite
```

## Usage
```python

# instantiate scraper
import cnnlite
from pprint import pprint

# start up scraper
scraper = cnnlite.CNNLite()

# export all articles to a json file
# default name: 'cnn_lite_<timestamp>.json'
scraper.to_json_file()

# show sample of headlines and URL list
print(scraper.headlines[:5])
print(scraper.urls[:5])

# large collection / nest dict containing each article for the day
docs = scraper.all_articles

# articles can be access one at a time too
article_name = scraper.headlines[0]
pprint(docs[article_name])

```

## Sample CNN Lite Home Page and Output JSON
<img src="./imgs/sample_cnn_lite.png" width="50%" alttext="Sample CNN Lite home page">
<img src="./imgs/sample_json.png" width="65%" altext="Sample JSON output">

## Bot Etiquetee
[Be a good bot and comply with the publisher's `robots.txt` guidelines.](https://edition.cnn.com/robots.txt)