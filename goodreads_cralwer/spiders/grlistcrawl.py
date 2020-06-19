# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup, NavigableString
import re


class GrlistcrawlSpider(CrawlSpider):
    name = 'grlistcrawl'
    allowed_domains = ['www.goodreads.com']
    start_urls = ['https://www.goodreads.com/list']

    rules = (
        # This rule will extract the links of all the book list (listopia on good) (except non-fiction as already done) including pagination
        Rule(LinkExtractor(restrict_xpaths=("//ul[@class='listTagsTwoColumn']//a", "//a[@class='next_page']"), deny=r'.*\/non-?fiction'),
             follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='listTitle']"),
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='bookTitle']", "//a[@class='next_page']")),
             callback='parse_item',
             follow=True)
    )

    def parse_item(self, response):
        book = {
            'book_title': '',
            'authors_names': '',
            'authors_data': '',
            'series_data': '',
            'description_fulltext': '',
            'description_fullhtml': '',
            'rating_value': '',
            'rating_count': '',
            'review_count': '',
            'genres': '',
            'bookcover_thumburl': '',
            'book_url': ''
        }

        current_book_url = response.request.url

        try:
            book['book_title'] = self.get_book_title(response)
            book['rating_value'] = self.get_rating_value(response)
            book['rating_count'] = self.get_rating_count(response)
            book['review_count'] = self.get_review_count(response)
            book['genres'] = self.get_genres_list(response)
            book['bookcover_thumburl'] = self.get_thumbnail_url(response)
            book['book_url'] = current_book_url
            book['authors_names'] = self.get_author_data(response)[0]
            book['authors_data'] = self.get_author_data(response)[1]
            book['series_data'] = self.get_book_series(response)
            desc_text, desc_html = self.get_book_description(response)
            book['description_fulltext'] = desc_text
            book['description_fullhtml'] = desc_html
        except Exception as e:
            print(str(e))

        yield book

    def get_book_title(self, response):
        return response.xpath("normalize-space(//h1[@id='bookTitle']/text())").get()

    def get_author_data(self, response):
        # This is should handle if multiple authors present for one book, then add all of them
        author_containers = response.xpath("//span[@itemprop='author']//a[@class ='authorName']")
        authors_names = []
        authors_data = []
        for author_html in author_containers:
            author = {}
            author_name = author_html.xpath(".//span[@itemprop='name']/text()").get()
            author['name'] = author_name
            author['link'] = author_html.xpath(".//@href").get()
            authors_names.append(author_name)
            authors_data.append(author)
        return (authors_names, authors_data)

    def get_book_series(self, response):
        series_info = {}
        series_info['series_name'] = response.xpath("normalize-space(//h2[@id='bookSeries']/a/text())").get()
        series_info['series_link'] = response.urljoin(response.xpath("//h2[@id='bookSeries']/a/@href").get())
        return series_info

    def get_book_description(self, response):
        pure_text = ''
        pure_html = ''
        soup = BeautifulSoup(response.body, 'lxml')
        des = soup.find("div", {"id": "description"}).find("span", {"style": "display:none"}).contents
        for content in des:
            stringified_content = str(content)
            if isinstance(content, NavigableString):
                pure_text += stringified_content
            pure_html += stringified_content
        return pure_text, pure_html

    def get_rating_value(self, response):
        return response.xpath("normalize-space(//div[@id='bookMeta']//span[@itemprop='ratingValue']/text())").get()

    def get_rating_count(self, response):
        rating_count = response.xpath(
            "normalize-space(//div[@id='bookMeta']//meta[@itemprop='ratingCount']/parent::a/text()[2])").get()
        return ''.join([x for x in re.findall(r'\d+', rating_count)])

    def get_review_count(self, response):
        review_count = response.xpath(
            "normalize-space(//div[@id='bookMeta']//meta[@itemprop='reviewCount']/parent::a/text()[2])").get()
        return ''.join([x for x in re.findall(r'\d+', review_count)])

    def get_genres_list(self, response):
        genres = response.xpath("//div[contains(@class, 'elementList')]//div[@class='left']")
        genres_list = []
        for genre in genres:
            genres_list.append(genre.xpath(".//a[contains(@class, 'actionLinkLite')]/text()").get())
        return genres_list

    def get_thumbnail_url(self, response):
        return response.xpath(".//div[contains(@class, 'bookCoverPrimary')]/a/img/@src").get()
