# -*- coding: utf-8 -*-
import scrapy


class SinglelistcrawlSpider(scrapy.Spider):
    name = 'singlelistcrawl'
    allowed_domains = ['www.goodreads.com']
    start_urls = ['https://www.goodreads.com/list/show/10762.Best_Book_Boyfriends']

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

