# cnnlite.py

# standard lib
import concurrent.futures
from datetime import datetime
import json
import logging
from typing import Dict, List

# third-party
from bs4 import BeautifulSoup
import requests

class CNNLite:
    """Web scraper for CNN Lite @ https://lite.cnn.com
    
    Example
    -------

    # instantiate scraper
    >>> import cnnlite
    >>> scraper = cnnlite.CNNLite()

    # export all articles to a json file
    >>> scraper.to_json_file()

    # show article-level attributes
    >>> scraper.headlines
    >>> scraper.urls

    # large collection / nest dict containing each article for the day
    >>> docs = scraper.all_articles
    """

    def __init__(self):
        self.urls = self._get_todays_urls()
        self.all_articles = self.to_dict()
        self.headlines = list(self.all_articles.keys())

    def to_dict(self):
        return self._get_todays_news()

    def to_json_file(self, out_filepath=None):

        docs = self.to_dict()

        # convert to json string    
        docs_str = json.dumps(docs, indent=2)
        
        if out_filepath is None:
            # export with timestamp
            dt_str = datetime.now().strftime('%Y%m%d%H%M')
            out_filepath = f'cnn_lite_{dt_str}.json'

        with open(out_filepath, 'w') as f:
            f.write(docs_str)

        logging.info(f'Created file: {out_filepath}')

    def get_article_from_url(self, url) -> Dict:
        """For one article URL, return a dictionary with the article content including meta data."""
        
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        document = {}

        # get headline
        document['headline'] = soup.find_all('h2').pop().getText()    
        document['url'] = url

        # get other meta info using `id` label
        for meta_info_category in ['byline', 'published datetime', 'source', 'editorsNote']:
            document[meta_info_category] = soup.find_all(id=meta_info_category).pop().getText()

        # get article text from `p` tags
        article_text = '\n\n'.join([tag.getText() for tag in soup.select('p')])    
        document['article_text'] = article_text
        
        return document

    def __repr__(self):
        return "CNNLiteScraper(urls, headlines)"

    def _get_todays_news(self, threaded=True) -> Dict[str, Dict]:
        """Build a dictionary of article/doc dictionaries."""

        logging.info('Collecting articles...')

        # The structure of `docs` nested dict is one key per headline
        # and within each headline collection is metadata and the article text. Ex:
        # {headline_1: 
            # {'byline': '', 
            #  'published datetime': '',
            #  'source': '', 
            #  'editorsNote': '',
            #  'article_text': ''
        # ... and so on through headline_<N>
        docs = {}
        
        # ex: 3.5 vs 18.5 seconds for threaded vs non-threaded
        if threaded:
            
            # threads will be writing to shared docs variable
            # function defined here, so we can access docs in this scope
            def _add_doc_to_dict(url, docs=docs):
                doc = self.get_article_from_url(url)
                docs[doc['headline']] = doc
        
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(_add_doc_to_dict, self.urls)
        
        elif not threaded:

            # sequential processing alternative (slower)
            for url in self.urls:
                doc = self.get_article_from_url(url)
                docs[doc['headline']] = doc
                
        return docs
    
    def _get_todays_urls(self) -> List:
        """Returns list of URLS from main CNN page, so we can scrape each URL."""
        
        base_url = 'https://lite.cnn.com'
        resp = requests.get(base_url)
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')

        # for each 'a' tag with 'article' in the URL
        # get the text (headline) and URL
        header_data = [(tag.getText(), tag['href']) 
                    for tag in soup.select('a')
                    if 'article' in tag['href']]

        # headlines is not accessed anywhere for now
        headlines, urls = zip(*header_data)
        urls = [base_url + url for url in urls]
        
        return urls
