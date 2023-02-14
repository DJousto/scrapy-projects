import scrapy
import json
from ..items import PromeplaItem as Product

class GenericSpider(scrapy.Spider):
    name = 'haemotronic'
    allowed_domains = ["www.haemotronic.it"]
    custom_settings = {
        'FEEDS': {
            'scraped_data/haemotronic.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True,
                'store_empty': False,
                'indent': 2,
            },
        },
        'LOG_LEVEL': 'INFO',
        #'DOWNLOAD_DELAY':3,
        'CONCURRENT_REQUESTS':16,
        'CONCURRENT_REQUESTS_PER_DOMAIN':16,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        },
    }



    # first level: there is only one request to get all products in a json structure
    # json is parsed in parse() function
    def start_requests(self):
        data = {
            'cat_id': '0',
            'subcat_id': '0',
            'filters': '{}',
            'freetext': '',
        }
        yield scrapy.Request( 'https://www.haemotronic.it/catalogue/ux/get_articles',
                              method='POST',
                              body=json.dumps(data),
                              headers={'Content-Type': 'application/json; charset=UTF-8'},
                              callback=self.parse)

    def parse(self,response):
        data = json.loads(response.text)
        for row in data['art_rows']:
            item = Product()
            description = dict()
            if row.get('img','') and len(row.get('img','')):
                item['img'] = 'https://www.haemotronic.it/catalogue/static/images/' + row['img']
            item['id'] = row['code']
            item['title'] = row['description']
            item['url'] = "https://www.haemotronic.it/catalogue/#"
            description['Color'] = row['Color']
            description['Packaging'] = row['Packaging']
            description['Sterilization'] = row['Sterilization']
            description['step'] = row['Packaging']
            description['Materials'] = row['Materials']
            description['sub_cat'] = row['sub_cat']
            item['metadata'] = description
            yield item
