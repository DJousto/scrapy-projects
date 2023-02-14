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

class GenericSpider(scrapy.Spider):
    name = 'meritoem'
    custom_settings = {
        'FEEDS': {
            'scraped_data/meritoem.json': {
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
    start_urls = ["https://meritoem.com/product-category/syringes/medallion/","https://meritoem.com/product-category/syringes/vaclok-at/","https://meritoem.com/product-category/syringes/vaclok/","https://meritoem.com/product-category/syringes/coronary-control/","https://meritoem.com/product-category/syringes/inflation-devices/","https://meritoem.com/product-category/syringes/cop/","https://meritoem.com/product-category/syringes/x-change/","https://meritoem.com/product-category/syringes/polypropylene/","https://meritoem.com/product-category/syringes/medallion-handles/","https://meritoem.com/product-category/syringes/rapid-exchange-rxp/","https://meritoem.com/product-category/valves/hemostasis-valves/","https://meritoem.com/product-category/valves/stopcocks/","https://meritoem.com/product-category/valves/tuohy-borst/","https://meritoem.com/product-category/valves/hemostasis-valve-adapters/","https://meritoem.com/product-category/valves/high-pressure-flow-control-switch/","https://meritoem.com/product-category/valves/manifolds/","https://meritoem.com/product-category/valves/stopcocks-with-extension-tubing/","https://meritoem.com/product-category/valves/luer-activated-valves/","https://meritoem.com/product-category/valves/check-relief-valves/","https://meritoem.com/product-category/molded-parts-components/adapters-rotators/","https://meritoem.com/product-category/molded-parts-components/caps-covers/","https://meritoem.com/product-category/molded-parts-components/hubs/","https://meritoem.com/product-category/molded-parts-components/luers-connectors/","https://meritoem.com/product-category/molded-parts-components/neuraxial-components-iso-80369-6/","https://meritoem.com/product-category/percutaneous-access/needles/","https://meritoem.com/product-category/percutaneous-access/introducers/","https://meritoem.com/product-category/percutaneous-access/dilators/","https://meritoem.com/product-category/percutaneous-access/valve-crossing-tool/","https://meritoem.com/product-category/percutaneous-access/scalpels/","https://meritoem.com/product-category/percutaneous-access/obturators/","https://meritoem.com/product-category/percutaneous-access/over-the-needle-access/","https://meritoem.com/product-category/tubing/high-pressure/","https://meritoem.com/product-category/tubing/pressure-monitoring/","https://meritoem.com/product-category/waste-management-safety/fluid-waste-disposal-systems/","https://meritoem.com/product-category/waste-management-safety/drainage-bags/","https://meritoem.com/product-category/waste-management-safety/disposal-basins/","https://meritoem.com/product-category/waste-management-safety/sharps-holder/","https://meritoem.com/product-category/waste-management-safety/pen-labels/","https://meritoem.com/product-category/fluid-management/contrast-transfer-sets/","https://meritoem.com/product-category/fluid-management/drip-chambers/","https://meritoem.com/product-category/fluid-management/fluid-administration-sets/","https://meritoem.com/product-category/fluid-management/fluid-administration-roller-clamp/","https://meritoem.com/product-category/fluid-management/spikes/","https://meritoem.com/product-category/fluid-management/pressure-infusor-bag/","https://meritoem.com/product-category/catheters-extrusions/diagnostic-cardiology/","https://meritoem.com/product-category/catheters-extrusions/diagnostic-peripheral/","https://meritoem.com/product-category/catheters-extrusions/guiding-catheters/","https://meritoem.com/product-category/catheters-extrusions/microcatheters/","https://meritoem.com/product-category/catheters-extrusions/marker-bands/","https://meritoem.com/product-category/catheters-extrusions/shafts/","https://meritoem.com/product-category/catheters-extrusions/centesis-catheters/","https://meritoem.com/product-category/catheters-extrusions/drainage-catheters/","https://meritoem.com/product-category/guide-wires-accessories/torque-devices/","https://meritoem.com/product-category/guide-wires-accessories/curved/","https://meritoem.com/product-category/guide-wires-accessories/straight/","https://meritoem.com/product-category/guide-wires-accessories/hydrophilic/","https://meritoem.com/product-category/guide-wires-accessories/coaxial-introducer-guide-wires/","https://meritoem.com/product-category/guide-wires-accessories/sheath-introducers-guide-wires/","https://meritoem.com/product-category/guide-wires-accessories/accessories/","https://meritoem.com/product-category/specialty-devices/snares/","https://meritoem.com/product-category/specialty-devices/squirt-fluid-dispensing-system/","https://meritoem.com/product-category/specialty-devices/transducers/","https://meritoem.com/product-category/specialty-devices/fixation-device/","https://meritoem.com/product-category/specialty-devices/suture-retention/","https://meritoem.com/product-category/specialty-devices/cultura-collection-transport/","https://meritoem.com/product-category/specialty-devices/therapeutic-infusion-systems/"]

    # first level
    def parse(self, response):
        url_list = response.css('li.product a.woocommerce-loop-product__link::attr(href)').getall()
        for url in url_list:
            yield scrapy.Request(url = url,callback = self.parse_product)
        next = response.xpath('//link[@rel="next"]/@href').get()
        if next:
            yield scrapy.Request(url = next,callback = self.parse)


    # product
    def parse_product(self, response):
        product = Product()
        product['metadata'] = dict()
        product['url'] = response.url
        product['title'] = response.xpath('//meta[@property="og:title"]/@content').get()
        product['metadata']['description'] = response.xpath('//meta[@property="og:description"]/@content').get()
        product['id'] = response.url.split('/')[-2]
        product['img'] = response.xpath('//meta[@property="og:image"]/@content').get()
        for detail in response.css('div.attribute-container div.product-attributes'):
            if detail.xpath('./p[1]/text()').get():
                product['metadata'][detail.xpath('./p[1]/text()').get().strip(':')] = detail.xpath('./p[2]/text()').get()
        product['metadata']['documents'] = response.css('div.woo-doc-wrapper a::attr(href)').getall()
        product['metadata']['category'] = '/'.join(response.css('div.breadcrumb-trail a span::text').getall()[1:])

        yield product
