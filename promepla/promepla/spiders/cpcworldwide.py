from scrapy.spiders import SitemapSpider
import scrapy
import json
from ..items import PromeplaItem as Product

# urls

headers = {
    'Accept': '*/*',
    'Referer': 'https://www.google.com',
    'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

class GenericSpider(SitemapSpider):
    name = 'cpcworldwide'
    custom_settings = {
        'FEEDS': {
            'scraped_data/cpcworldwide.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'overwrite': True,
                'indent': 2,
            },
        },
        # if you need proxies, enable this following settings
        'HTTPPROXY_ENABLED': True,
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_TIMEOUT':30,
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS':32,
        'DEFAULT_REQUEST_HEADERS':headers,
        'CONCURRENT_REQUESTS_PER_DOMAIN':32,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 405,
        },
    }


    sitemap_urls = ['https://products.cpcworldwide.com/en_US/sitemap-product-sitemap-0']

    sitemap_rules = [
        (r'ProductsCat', 'parse_product'),
    ]


    # product
    def parse_product(self, response):
        product = Product()
        product['metadata'] = dict()
        product['url'] = response.url
        product['title'] = response.css('h1 span::text').get()
        img = response.css('div.product-img-main img::attr(src)').get()
        if img:
            product['img'] = 'https://products.cpcworldwide.com' + img

        infos = response.xpath('//meta[@name]')
        for info in infos[4:]:
            if 'twitter' in info.attrib['name']:
                continue

            if info.attrib['name']=="Product Category":
                product['metadata']['category'] = info.attrib['content']
                continue

            if not info.attrib['content']:
                continue

            if info.attrib['name']=='Product ID':
                product['id'] = info.attrib['content']
                continue

            if info.attrib['name']=="Product Description":
                product['title'] = info.attrib['content']
                continue

            # for all other cases :
            product['metadata'][info.attrib['name']] = info.attrib['content']


        yield product
