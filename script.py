from cnnlite import cnnlite

scraper = cnnlite.CNNLiteScraper()
all_articles = scraper.to_dict()
scraper.to_json_file(out='test.json')

all_articles.keys()
scraper.urls
scraper.headlines

