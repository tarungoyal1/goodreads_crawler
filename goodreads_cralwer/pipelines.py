# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient


class GoodreadsCralwerPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['books']
        self.col_bookinfo = self.db['book_urls']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print('GoodreadsCralwerPipeline')
        return item
        # if not self.col_bookinfo.find_one({'book_url': item['book_url']}):
        #     if self.col_bookinfo.insert_one(item):
        #         return True
        # else:
        #     # print('Duplicate book url, skipped.')
        #     return False

class BookUrlPipeline:
    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['books']
        self.col_bookurls = self.db['book_urls']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # print('BookUrlPipeline')
        # print(item)
        if not self.col_bookurls.find_one({'url': item['url']}):
            if self.col_bookurls.insert_one(item):
                print('New book url inserted, url ={}'.format(item['url']))
                return True
        else:
            print('Duplicate book url, skipped.')
        return False