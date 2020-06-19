# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class GoodreadsCralwerPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['books_crawled']
        self.col_bookinfo = self.db['book_info']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not self.col_bookinfo.find_one({'book_url': item['book_url']}):
            if self.col_bookinfo.insert_one(item):
                return True
        else:
            # print('Duplicate book url, skipped.')
            return False