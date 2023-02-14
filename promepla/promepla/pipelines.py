# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time
from scrapy import signals
from pydispatch import dispatcher
from slack import WebClient
from slack.errors import SlackApiError
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from scrapy.utils.project import get_project_settings
import logging
from scrapy.exceptions import DropItem

settings = get_project_settings()

class PromeplaPipeline:
    def __init__(self):
         self.ids_seen = set()
         dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def process_item(self, item, spider):
        item.setdefault('scraping_date', time.strftime("%Y-%m-%d %H:%M:%S"))
        if item['id'] in self.ids_seen:
            raise DropItem()
        else:
            self.ids_seen.add(item['id'])
            return item


    def spider_closed(self, spider):
        if settings['SLACK']:
            try:
                message = spider.settings['BOT_NAME'] + "/" + spider.name + ' : terminated\nItems : ' + str(spider.crawler.stats._stats.get("item_scraped_count",0))
                message = message + f"\nFile  : http://scrapy-srv.graphee.io:6800/logs/items/{list(spider.settings['FEEDS'].keys())[0].split('/')[-1]}"
            except:
                message = spider.name + ' scraping finished | Error, see logs '

            slack_client = WebClient(token=settings['SLACK_TOKEN'])
            try:
                slack_client.chat_postMessage(
                    channel=settings['SLACK_CHANNEL'],
                    text=message
                )
            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                logging.error(e.response["error"])




