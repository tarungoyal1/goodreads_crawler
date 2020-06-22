# -*- coding: utf-8 -*-
import scrapy
from .geturls import get_listurl, updateListStatus


class SinglelistcrawlSpider(scrapy.Spider):
    name = 'singlelistcrawl'
    allowed_domains = ['www.goodreads.com']

    # Bind this spider with it's own separate pipeline (BookUrlPipeline)
    custom_settings = {
        'ITEM_PIPELINES': {
            'goodreads_cralwer.pipelines.BookUrlPipeline': 400
        }
    }
    list_url = ''

    def start_requests(self):
        list_url = get_listurl()
        self.list_url = list_url
        yield scrapy.Request(list_url)


    def parse(self, response):
        book_url = {
            'url': '',
            'status': 'pending'
        }

        for url in response.xpath("//table[contains(@class, 'tableList')]//tr"):
            book_url['url'] = response.urljoin(url.xpath(".//a[@class='bookTitle']/@href").get())
            yield book_url

        next_page = response.xpath("//a[@class='next_page']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            # means reached the last page in pagination
            if updateListStatus(self.list_url):
                print("List fully scraped and status changed to 'done'")



