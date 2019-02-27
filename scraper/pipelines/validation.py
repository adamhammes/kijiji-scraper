from datetime import datetime
import fractions
import re

from scrapy.exceptions import DropItem
from scraper.items import Apartment


FIELD_NAMES = Apartment.fields.keys()


class ValidationPipeline(object):
    def open_spider(self, spider):
        self.cache = set()

    def process_item(self, item, spider):
        if item["raw_id"] in self.cache:
            raise DropItem("Already seen item (link: {})".format(item["url"]))

        self.cache.add(item["raw_id"])

        # Set all missing fields to None
        for key in FIELD_NAMES:
            item.setdefault(key, None)

        item["id"] = int(item["raw_id"])
        item["date"] = _read_date(item["raw_date"])
        item["price"] = _read_price(item["raw_price"])

        item["num_bathrooms"] = _read_bathrooms(item["raw_bathrooms"])
        item["is_furnished"] = _read_furnished(item["raw_furnished"])
        item["allows_animals"] = _read_animals(item["raw_animals"])
        item["num_rooms"] = _read_num_rooms(item["raw_rooms"])

        return item


def nullable(func, *args, **kw):
    def wrapped(*args, **kw):
        if args[0] is None:
            return None

        return func(*args, **kw)

    return wrapped


@nullable
def _read_date(raw_date):
    date_format = "%Y-%m-%dT%H:%M:%S"

    relevant = raw_date.split(".")[0]
    return datetime.strptime(relevant, date_format)


@nullable
def _read_price(raw_price):
    valid_chars = "0123456789,"
    valid_price = "".join(c for c in raw_price if c in valid_chars)

    price_re = re.compile(r"(\d+),(\d+)")
    match = price_re.search(valid_price)

    if not match:
        raise DropItem('Couldn\'t read price "{}"'.format(raw_price))

    dollars = int(match.group(1))
    cents = int(match.group(2))

    return dollars * 100 + cents


@nullable
def _read_bathrooms(raw_bathrooms):
    bathroom_re = re.compile(r"(\d+)(,5)?")
    match = bathroom_re.search(raw_bathrooms)

    if not match:
        raise DropItem('Couldn\'t read bathrooms "{}"'.format(raw_bathrooms))

    val = float(match.group(1))
    if match.group(2) == ",5":
        val += .5

    return val


@nullable
def _read_furnished(raw_furnished):
    return "Oui" in raw_furnished


@nullable
def _read_animals(raw_animals):
    return "Oui" in raw_animals


@nullable
def _read_num_rooms(raw_fraction):
    parts = raw_fraction.split(" ")[:2]

    return float(sum(fractions.Fraction(part) for part in parts))

