# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PromeplaItem(scrapy.Item):
    scraping_date = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    img = scrapy.Field()
    metadata = scrapy.Field()

