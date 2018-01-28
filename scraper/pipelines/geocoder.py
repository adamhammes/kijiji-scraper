import json
import logging
import os

import geocoder
import requests
from scrapy.exceptions import DropItem


class GeocoderPipeline(object):
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

    def process_item(self, item, spider):
        raw_address = item['raw_address']

        if raw_address in self.cache:
            item.update(self.cache[raw_address])
            return item

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
            'latitude': geocode.latlng[0],
            'longitude': geocode.latlng[1],
            'city': geocode.city,
        }

        self.cache[raw_address] = new_fields

        item.update(new_fields)
        return item

    def close_spider(self, _):
        with open(self.cache_location, 'w') as f:
            f.write(json.dumps(self.cache))

