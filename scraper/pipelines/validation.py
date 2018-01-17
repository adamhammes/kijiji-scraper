from datetime import datetime
import fractions
import re

from scrapy.exceptions import DropItem


class ValidationPipeline(object):
    def open_spider(self, spider):
        self.cache = set()
    
    def process_item(self, item, spider):
        if item['raw_id'] in self.cache:
            raise DropItem('Already seen item (link: {})'.format(item['url']))
        
        item['id'] = int(item['raw_id'])
        item['date'] = _read_date(item['raw_date'])
        
        if 'raw_price' in item:
            item['price'] = _read_price(item['raw_price'])
        else:
            item['raw_price'], item['price']  = None, None

        item['num_bathrooms'] = _read_bathrooms(item['raw_bathrooms'])
        item['is_furnished'] = _read_furnished(item['raw_furnished'])

        if 'raw_animals' in item:
            item['allows_animals'] = _read_animals(item['raw_animals'])
        else:
            item['raw_animals'], item['allows_animals'] = None, None

        item['num_rooms'] = _read_num_rooms(item['title'])

        return item


def _read_date(raw_date):
    date_format = '%Y-%m-%dT%H:%M:%S'

    relevant = raw_date.split('.')[0]
    return datetime.strptime(relevant, date_format)


def _read_price(raw_price):
    if not raw_price:
        return None

    valid_chars = '0123456789,'
    valid_price = ''.join(c for c in raw_price if c in valid_chars)

    price_re = re.compile(r'(\d+),(\d+)')
    match = price_re.search(valid_price)

    if not match:
        raise DropItem('Couldn\'t read price "{}"'.format(raw_price))
    
    dollars = int(match.group(1))
    cents = int(match.group(2))

    return dollars * 100 + cents

def _read_bathrooms(raw_bathrooms):
    bathroom_re = re.compile(r'(\d+)(,5)?')
    match = bathroom_re.search(raw_bathrooms)

    if not match:
        raise DropItem('Couldn\'t read bathrooms "{}"'.format(raw_bathrooms))
    
    val = float(match.group(1))
    if match.group(2) == ',5':
        val += .5

    return val


def _read_furnished(raw_furnished):
    return 'Oui' in raw_furnished


def _read_animals(raw_animals):
    if not raw_animals:
        return None

    return 'Oui' in raw_animals

def _read_num_rooms(title):
    raw = title.split(' | ')[-3]
    parts = raw.split(' ')[:2]

    return float(sum(fractions.Fraction(part) for part in parts))
