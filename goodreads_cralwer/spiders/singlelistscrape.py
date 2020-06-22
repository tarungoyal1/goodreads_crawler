# -*- coding: utf-8 -*-
import scrapy
from .geturls import get_listurl, updateListStatus
import logging


class SinglelistcrawlSpider(scrapy.Spider):
    name = 'singlelistcrawl'
    allowed_domains = ['www.goodreads.com']

    # Bind this spider with it's own separate pipeline (BookUrlPipeline)
    custom_settings = {
        'ITEM_PIPELINES': {
            'goodreads_cralwer.pipelines.BookUrlPipeline': 400
        }
    }

    def start_requests(self):
        #batch size of list_urls = 2
        list_url_batch = get_listurl()
        urls = next(list_url_batch)
        for i in range(2):
            list_url = urls.pop(0)
            yield scrapy.Request(list_url)


    def parse(self, response):
        book_url = {
            'url': '',
            'status': 'pending'
        }

        for url in response.xpath("//table[contains(@class, 'tableList')]//tr"):
            book_url['url'] = response.urljoin(url.xpath(".//a[@class='bookTitle']/@href").get())
            yield book_url

        next_page = response.xpath("//div[@class='pagination']//a[@class='next_page']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            # means reached the last page in pagination
            last_url = response.request.url.partition('?')[0]
            if updateListStatus(last_url):
                print("List fully scraped and status changed to 'done', list_url = {}".format(last_url))



