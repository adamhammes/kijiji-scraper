import datetime
import logging

import scrapy
from scraper.items import Apartment
from scrapy.loader import ItemLoader
from .origins import QUEBEC_COLOC, QUEBEC_APARTMENTS


class ApartmentSpider(scrapy.Spider):
    base_url = 'https://www.kijiji.ca'
    name = 'apartments'

    origins = [QUEBEC_COLOC, QUEBEC_APARTMENTS]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            if self.full_scrape:
                logging.debug('Running full scrape')
            else:
                logging.debug('Only scraping first page of results')
        except AttributeError:
            logging.debug(
                'Command-line arg "full_scrape" not found\n'
                'defaulting to only using first page of results'
            )
            self.full_scrape = False

    def start_requests(self):
        for origin in self.origins:
            meta = {'origin': origin}
            yield scrapy.Request(
                url=meta.origin,
                callback=self.results_page,
                meta=meta
            )

    def results_page(self, response):
        apartment_paths = response.css(
            '.info-container a.title::attr(href)').extract()

        for path in apartment_paths:
            full_url = ApartmentSpider.base_url + path
            yield scrapy.Request(
                url=full_url,
                callback=self.apartment_page,
                meta=response.meta
            )

        next_path = response.css(
            'a[title~="Suivante"]::attr(href)').extract_first()

        if next_path and self.full_scrape:
            next_url = ApartmentSpider.base_url + next_path
            yield scrapy.Request(
                url=next_url,
                callback=self.results_page,
                meta=response.meta
            )

    def apartment_page(self, response):
        l = ItemLoader(item=Apartment(), response=response)
        l.default_output_processor = scrapy.loader.processors.TakeFirst()

        l.add_value('origin', response.meta['origin'])
        l.add_value('url', response.url)
        l.add_css('main_image_url',
                  'meta[property~="og:image"]::attr(content)')
        l.add_css('headline', "h1[class^='title']::text")
        l.add_css('description', 'div[class^="descriptionContainer"] > div')
        l.add_css('title', 'title::text')
        l.add_value('date_accessed', datetime.datetime.now())

        l.add_css('raw_id', 'li[class^="currentCrumb"] > span::text')
        l.add_css(
            'raw_date', 'div[class^="datePosted"] > time::attr(datetime)')
        l.add_css('raw_address', "span[class^='address']::text")
        l.add_css('raw_price', 'span[class^="currentPrice"] > span::text')
        l.add_css('raw_bathrooms', '#AttributeList li:nth-of-type(1) dd::text')
        l.add_css('raw_furnished', '#AttributeList li:nth-of-type(2) dd::text')
        l.add_css('raw_animals', '#AttributeList li:nth-of-type(3) dd::text')

        return l.load_item()
