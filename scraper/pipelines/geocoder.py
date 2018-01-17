import geocoder
import os

from scrapy.exceptions import DropItem


class GeocoderPipeline(object):
    def open_spider(self, spider):
        self.api_key = os.environ['GOOGLE_GEOCODER_KEY']

    def process_item(self, item, spider):
        geocode = self._geocode(item['raw_address'])

        if not geocode.ok:
            raise DropItem('Bad response from geocode API')

        item['address_confidence'] = geocode.confidence
        item['address_accuracy'] = geocode.accuracy

        item['address'] = geocode.address
        item['postal'] = geocode.postal

        item['latitude'], item['longitude'] = geocode.latlng
        item['city'] = geocode.city

        return item

    def _geocode(self, address):
        return geocoder.google(address, key=self.api_key)
