# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

#This pipelines is bound with spider = GetBookDetailsSpider in get_book_details.py
class GoodreadsCralwerPipeline:

    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['books']
        self.col_bookinfo = self.db['book_info']
        self.col_allbookurls = self.db['gr_book_urls']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print('GoodreadsCralwerPipeline')
        if not self.col_bookinfo.find_one({'book_url': item['book_url']}):
            if self.col_bookinfo.insert_one(item):
                if self.col_allbookurls.update_one({'url': item['book_url']}, {'$set': {'status': 'done'}},upsert=False).modified_count == 1:
                    # print('New book inserted and status updated, url  = {}'.format(item['book_url']))
                    return True
        else:
            # print('Book already scraped having url = {}'.format(item['book_url']))
            return False
        return item



#This pipelines is bound with spider = GrlistcrawlSpider in grlistcrawl.py
class BookUrlPipeline:
    def open_spider(self, spider):
        self.client = MongoClient()
        self.db = self.client['books']
        self.col_nfbookurls = self.db['book_urls'] # Old collection having book urls of non-fiction
        self.col_allbookurls = self.db['gr_book_urls'] # New collection having all book urls except non-fiction
        self.col_bookinfo = self.db['book_info']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not self.col_nfbookurls.find_one({'url': item['url']}):
            if  self.col_allbookurls.update_one(item,{'$set':item},upsert=True):
                # print('New book url inserted, url ={}'.format(item['url']))
                return True
        else:
            return False
        return item
