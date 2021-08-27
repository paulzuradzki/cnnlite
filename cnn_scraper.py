# cnn_scraper.py

import requests
from bs4 import BeautifulSoup
import concurrent.futures
from typing import Dict
import json
from datetime import datetime

def main():
    """Export today's news to json."""
    
    print('START')
    # collect all of the article docs into a dict
    docs = get_todays_news()
    
    # convert to json string
    docs_str = json.dumps(docs, indent=2)
    
    # export with timestamp
    dt_str = datetime.now().strftime('%Y%m%d%H%M')
    with open(f'cnn_lite_{dt_str}.json', 'w') as f:
        f.write(docs_str)

    print('END')

def get_todays_news(threaded=True) -> Dict[str, Dict]:
    """Build a dictionary of article/doc dictionaries."""
    urls = get_todays_urls()
    docs = {}
    
    # ex: 3.5 vs 18.5 seconds for threaded vs non-threaded
    if threaded:
        
        def _add_doc_to_dict(url, docs=docs):
            doc = get_article_document(url)
            docs[doc['headline']] = doc
    
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(_add_doc_to_dict, urls)
    
    else:
        for url in urls:
            doc = get_article_document(url)
            docs[doc['headline']] = doc
            
    return docs
    
def get_todays_urls():
    """Returns list of URLS from main CNN page, so we can scrape each URL.
    
    Usage
    -----
    urls = get_todays_urls()
    """
    
    base_url = 'https://lite.cnn.com'
    resp = requests.get(base_url)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    header_data = [(tag.getText(), tag['href']) 
                   for tag in soup.select('a')
                   if 'article' in tag['href']]

    headlines, urls = zip(*header_data)
    urls = [base_url + url for url in urls]
    
    return urls

def get_article_document(url) -> Dict:
    """For one URL, return a dictionary article content (meta info + text)."""
    
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

if __name__ == '__main__':
    main()