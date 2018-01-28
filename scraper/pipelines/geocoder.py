import json
import logging
import os

import geocoder
import requests
from scrapy.exceptions import DropItem


ITEMS_GEOCODED = 'num_items_geocoded'
GEOCODE_HIT = 'geocode_cache_hits'
GEOCODE_MISS = 'geocode_cache_misses'


class GeocoderPipeline(object):
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)

    def open_spider(self, spider):
        self.api_key = os.environ['GOOGLE_GEOCODER_KEY']
        output_dir = os.environ['KIJIJI_OUTPUT_DIRECTORY']

        self.cache_location = os.path.join(output_dir, 'geocoder_cache.json')

        try:
            with open(self.cache_location) as f:
                self.cache = json.loads(f.read())
        except FileNotFoundError:
            self.cache = {}
        except json.JSONDecodeError as err:
            logging.error('Couldn\'t decode geocoder cache:\n{}'.format(err))
            self.cache = {}

        self.session = requests.session()

        self.stats.set_value(ITEMS_GEOCODED , 0)
        self.stats.set_value(GEOCODE_HIT , 0)
        self.stats.set_value(GEOCODE_MISS , 0)

    def process_item(self, item, spider):
        self.stats.inc_value(ITEMS_GEOCODED)
        raw_address = item['raw_address']

        if raw_address in self.cache:
            self.stats.inc_value(GEOCODE_HIT)
            item.update(self.cache[raw_address])
            return item

        self.stats.inc_value(GEOCODE_MISS)
        geocode = geocoder.google(
            raw_address,
            key=self.api_key,
            session=self.session,
        )

        if not geocode.ok:
            raise DropItem('Bad response from geocode API: {}'
                .format(geocode.status))

        new_fields = {
            'address_confidence': int(geocode.confidence),
            'address_accuracy': geocode.accuracy,
            'address': geocode.address,
            'postal': geocode.postal,
            'latitude': float(geocode.latlng[0]),
            'longitude': float(geocode.latlng[1]),
            'city': geocode.city,
        }

        self.cache[raw_address] = new_fields

        item.update(new_fields)
        return item

    def close_spider(self, _):
        with open(self.cache_location, 'w') as f:
            f.write(json.dumps(self.cache))

