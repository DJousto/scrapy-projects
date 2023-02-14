import scrapy
import re
from ..items import PromeplaItem as Product
import logging

# urls
start_urls = ["https://www.nordsonmedical.com/Shop/Fluid-Management","https://www.nordsonmedical.com/Shop/Quick-Connect-Fittings"]

class GenericSpider(scrapy.Spider):
    name = 'nordsonmedical'
    allowed_domains = ["nordsonmedical.com"]
    custom_settings = {
        'FEEDS': {
            'scraped_data/nordsonmedical.json': {
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
            yield scrapy.Request(url = url,callback = self.parse_categories)

    # first level
    def parse_categories(self, response):
        url_list = response.xpath('//h4/a/@href').getall()
        url_list = ["https://www.nordsonmedical.com"+x.replace(' ','%20')+"?start=0&itemsPer=1000" for x in url_list]
        logging.log(logging.INFO, f'{len(url_list)} subcategories in url {response.url}')
        for url in url_list:
            yield scrapy.Request(url = url,callback = self.parse_sub_categories)



    # 2nd level
    def parse_sub_categories(self, response):
        url_list = response.xpath('//div[@class="product-front"]//h4/a/@href').getall()
        logging.log(logging.INFO, f'{len(url_list)} products in category {response.url}')
        for url in url_list:
            url = "https://www.nordsonmedical.com" + url
            yield scrapy.Request(url = url,callback = self.parse_product)


    # product
    def parse_product(self, response):
        item = Product()
        metadata = dict()

        price = response.xpath('//h4[@class="text-orange-sm"]/text()').get()
        if price is not None:
            metadata['price'] = price.strip()

        pic = response.xpath('//img[contains(@class,"product-img-shop")]/@src').get()
        if pic is not None:
            item['img'] = "https://www.nordsonmedical.com"+pic

        pdf = response.xpath('//div[@id="drawing"]//a/@href').get()
        if pdf is not None:
            pdf = "https://www.nordsonmedical.com"+pdf
        metadata['drawing'] = pdf

        item['id'] = response.url.split('/')[-1]
        item['url'] = response.url
        item['title'] = response.xpath('//p[@class="text-grey"]/text()').get()

        metadata['colors'] = re.findall(r'Clear|Natural|White|Black|Blue|Red|Yellow|Green|Orange', item['title'])
        metadata['family'] = response.xpath('//label[@id="hfFamily"]/text()').get()
        metadata['category'] = response.xpath('//label[@id="hfCategory"]/text()').get()
        metadata['style'] = response.xpath('//label[@id="hfStyle"]/text()').get()
        metadata['material'] = response.xpath('//label[@id="hfMaterial"]/text()').get()

        item['metadata'] = metadata

        yield item