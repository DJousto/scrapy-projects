import scrapy
import re
from ..items import PromeplaItem as Product

class GenericSpider(scrapy.Spider):
    name = 'elcam-medical'
    allowed_domains = ["www.elcam-medical.com"]
    start_urls = ['https://www.elcam-medical.com/sitemap_index.xml']
    custom_settings = {
        'FEEDS': {
            'scraped_data/elcam-medical.json': {
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
        #'CLOSESPIDER_ITEMCOUNT':1,
    }

    # first level
    def parse(self, response):
        url_list = re.findall(r'>(https://www\.elcam-medical\.com/product-sitemap[^<]*)',response.text)
        for url in url_list:
            yield scrapy.Request(url = url,callback = self.parse_sitemap_2)

    # 2nd level
    def parse_sitemap_2(self, response):
        url_list = re.findall(r'>(https://www\.elcam-medical\.com/product/[^<]*)',response.text)
        for url in url_list:
            yield scrapy.Request(url = url,callback = self.parse_product)

    # product
    def parse_product(self, response):
        item = Product()
        item['url'] = response.url
        metadata = dict()

        data_table = response.xpath('//div[@class="table-single-product"]')[0]
        rows = data_table.xpath('.//tr')
        for row in rows:
            key = row.xpath('.//th/text()').get()
            value = row.xpath('.//td//text()[normalize-space()]').get().strip()
            if key=="Name":
                item['title'] = value
            elif key=="Product Code":
                item['id'] = value
            else:
                metadata[key] = value

        item['img'] = response.xpath('//meta[@property="og:image"]/@content').get()

        metadata['documentation'] = response.xpath('//div[@class="catalogue-links"]/a/@href').get()

        item['metadata'] = metadata

        yield item
