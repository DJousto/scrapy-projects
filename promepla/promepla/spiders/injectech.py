import scrapy
import json
from ..items import PromeplaItem as Product

# urls
start_urls = ["https://www.injectech.net/Products/"]

class GenericSpider(scrapy.Spider):
    name = 'injectech'
    allowed_domains = ["injectech.net"]
    custom_settings = {
        'FEEDS': {
            'scraped_data/injectech.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'overwrite': True,
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
    def start_requests(self):
        for url in start_urls:
            yield scrapy.Request(url = url,callback = self.parse)

    # first level
    def parse(self, response):
        url_list = response.xpath('//div[@class="col-sm-4 column"]/div/a/@href').getall()
        url_list = ["https://www.injectech.net"+x for x in url_list]
        for url in url_list:
            yield scrapy.Request(url = url,callback = self.parse_categories)

    # 2nd level
    def parse_categories(self, response):
        url_list = response.xpath('//div[contains(@class,"category-item")]/a[contains(@class,"category-link")]/@href').getall()
        url_list = ["https://www.injectech.net"+x for x in url_list]
        for url in url_list:
            yield scrapy.Request(url = url,callback = self.parse_sub_categories)

    # 2nd level
    def parse_sub_categories(self, response):
        url_list = response.xpath('//a[contains(@class,"view-details")]/@href').getall()
        url_list = ["https://www.injectech.net"+x for x in url_list]
        for url in url_list:
            yield scrapy.Request(url = url,callback = self.parse_product)

    # product
    def parse_product(self, response):
        item = Product()
        metadata = dict()

        x = response.xpath('//script[contains(text(),".productDetails({")]/text()').get().split('{"Product":')[1][:-7]
        data = json.loads(x)

        if len(data['Variations']):
            products = data['Variations']
        else:
            products = list()
            products.append(data)

        for product in products:
            for key,value in product['Attributes'].items():
                if len(value):
                    if key == "LeadTimeMessage":
                        continue
                    if "download" in key.lower():
                        value = "https://www.injectech.net/downloads/" + value
                    metadata[key] = value
            metadata['stock'] = product['BundleStockCheck']['ActualStockLevel']
            if type(metadata['stock']) == int:
                metadata['stock'] = max(0,metadata['stock'])

            item['img'] = "https://www.injectech.net" + product['ProductImages']['DEFAULT']['Images'][0]['Sizes']['LARGE']['ImagePath']
            item['id'] = product['ProductCode']
            item['title'] = product['ProductName']
            metadata['price'] = product['ProductPrice']['Price']
            metadata['MinimumOrderQuantity'] = product['MinimumOrderQuantity']
            metadata['category'] = product['Navigation_ProductCategory']
            item['url'] = response.url
            item['metadata'] = metadata

            yield item
