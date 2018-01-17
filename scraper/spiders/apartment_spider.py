import scrapy
from scraper.items import Apartment
from scrapy.loader import ItemLoader


class ApartmentSpider(scrapy.Spider):
    base_url = 'https://www.kijiji.ca'
    name = "apartments"

    def start_requests(self):
        urls = ['https://www.kijiji.ca/b-appartement-condo/ville-de-quebec/c37l1700124?ad=offering']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.results_page)

    def results_page(self, response):
        apartment_paths = response.css('.info-container a.title::attr(href)').extract()

        for path in apartment_paths:
            full_url = ApartmentSpider.base_url + path
            yield scrapy.Request(url=full_url, callback=self.apartment_page)

        next_path = response.css('a[title~="Suivante"]::attr(href)').extract_first()

        if next_path:
            next_url = ApartmentSpider.base_url + next_path
            yield scrapy.Request(url=next_url, callback=self.results_page)

    def apartment_page(self, response):
        l = ItemLoader(item=Apartment(), response=response)
        l.default_output_processor = scrapy.loader.processors.TakeFirst()

        l.add_value('url', response.url)
        l.add_css('main_image_url', 'meta[property~="og:image"]::attr(content)')
        l.add_css('headline', "h1[class^='title']::text")
        l.add_css('description', 'div[class^="descriptionContainer"] > div')
        l.add_css('title', 'title::text')

        l.add_css('raw_id', 'li[class^="currentCrumb"] > span::text')
        l.add_css('raw_date', 'div[class^="datePosted"] > time::attr(datetime)')
        l.add_css('raw_address', "span[class^='address']::text")
        l.add_css('raw_price', 'span[class^="currentPrice"] > span::text')
        l.add_css('raw_bathrooms', '#AttributeList li:nth-of-type(1) dd::text')
        l.add_css('raw_furnished', '#AttributeList li:nth-of-type(2) dd::text')
        l.add_css('raw_animals', '#AttributeList li:nth-of-type(3) dd::text')

        return l.load_item()
