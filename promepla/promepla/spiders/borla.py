import scrapy
from ..items import PromeplaItem as Product

start_urls = ["https://www.borla.it/find.php"]

class GenericSpider(scrapy.Spider):
    name = 'borla'
    allowed_domains = ["borla.it"]
    custom_settings = {
        'FEEDS': {
            'scraped_data/borla.json': {
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

    def parse(self, response):
        items = response.xpath('//div[@class="rowresult" and @style]')
        for item in items:
            product = Product()

            # title
            product['title'] = ''.join(item.xpath('.//text()').extract()).strip()

            # url
            product['url'] = "https://www.borla.it/find.php"

            # image
            details = item.xpath('./following-sibling::div[@id="rowresult"][1]')
            if len(details):
                img = details[0].xpath('.//div[@id="imgthumb"]/img/@src').get()
                if (img is not None) and len(img)>0:
                    product['img'] = "https://www.borla.it/" + img

            # product ID
            cod = details.xpath('.//div[contains(@class,"cod-result")]/text()').getall()
            if len(cod):
                product['id'] = cod[-1]

            # all other data are stored in metadata dict
            metadata = dict()
            pf = details.xpath('.//div[contains(@class,"pf-result")]/text()').getall()
            if len(pf):
                metadata['pf'] = pf[-1]
            characteristics = details.xpath('.//div[contains(@class,"bgcol")]')
            for characteristic in characteristics:
                metadata[characteristic.xpath('.//div[@class="chr-title-C"]/text()').get()] = characteristic.xpath('.//div[@class="chr-C"]/text()').get()

            explode = item.xpath('./following-sibling::div[3]')
            if len(explode):
                explode = explode[0]
                if "explosion" in explode.attrib.get('id',''):
                    codes = explode.xpath('.//div[@class="explosion-cod-component"]/text()').getall()
                    codes = [x for x in codes if x.isnumeric()]
                    if len(codes):
                        metadata["components"] = codes

            product['metadata'] = metadata

            yield product



