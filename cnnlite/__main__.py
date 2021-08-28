import logging
import cnn_scraper

def main():
    # Export today's news to json in local directory
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info('Starting main.')

    scraper = cnn_scraper.CNNLite()
    scraper.to_json_file()
    logging.info('Completed main.')

if __name__ == '__main__':
    main()