import scrapy
from scrapy.crawler import CrawlerProcess
from goodreads_cralwer.spiders.grlistcrawl import GrlistcrawlSpider
from goodreads_cralwer.spiders.get_book_details import GetBookDetailsSpider

process = CrawlerProcess()
process.crawl(GrlistcrawlSpider)
process.crawl(GetBookDetailsSpider)
process.start()