import scrapy


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
        yield {
            'id': response.css('li[class^="currentCrumb"] > span::text').extract_first(),
            'date': response.css('div[class^="datePosted"] > time::attr(datetime)').extract_first(),
            'title': response.css("h1[class^='title']::text").extract_first(),
            'address': response.css("span[class^='address']::text").extract_first(),
            'price': response.css('span[class^="currentPrice"] > span::text').extract_first(),
            'description': response.css('div[class^="descriptionContainer"] > div').extract_first(),
            'bathrooms':  response.css('#AttributeList li:nth-of-type(1) dd::text').extract_first(),
            'furnished':  response.css('#AttributeList li:nth-of-type(2) dd::text').extract_first(),
            'main_image_url': response.css('meta[property~="og:image"]::attr(content)').extract_first(),
        }
