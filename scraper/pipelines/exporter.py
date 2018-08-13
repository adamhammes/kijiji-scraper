import csv
from datetime import date, datetime, timezone
import io
import json
import logging
import os

import boto3

from scraper.items import Apartment
from .makes_the_cut import makes_the_cut, RETAINED_KEYS
from ..cities import slug_to_city, starting_cities


EXPORT_TIME = None
FIELD_NAMES = list(Apartment.fields.keys())
OUTPUT_DIRECTORY = os.environ["KIJIJI_OUTPUT_DIRECTORY"]
LATEST_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "latest")


class ItemCollector:
    def open_spider(self, spider):
        self.full_scrape = spider.full_scrape
        self.cities = {city.slug: [] for city in starting_cities}
        logging.debug(self.cities)

        self.exporters = [
            (full_csv, "all_items.csv"),
            (trimmed_json, "trimmed_values.json"),
        ]

    def process_item(self, item, _):
        logging.debug("process city " + str(item["starting_city"]))
        self.cities[item["starting_city"].slug].append(item)
        return item

    def close_spider(self, _):
        for slug, items in self.cities.items():
            for exporter, exporter_name in self.exporters:
                value = exporter(slug_to_city[slug], items)
                export(slug, value, exporter, exporter_name, self.full_scrape)


def export(city_slug, value, exporter, exporter_name, full_scrape):
    latest_path = os.path.join(LATEST_DIRECTORY, city_slug, exporter_name)
    os.makedirs(os.path.dirname(latest_path), exist_ok=True)
    with io.open(latest_path, "w", encoding="utf-8") as f:
        f.write(value)

    time_path = os.path.join(datetime_slug(), city_slug, exporter_name)

    if full_scrape:
        upload_to_s3(time_path, value)

    file_time_path = os.path.join(OUTPUT_DIRECTORY, time_path)
    os.makedirs(os.path.dirname(file_time_path), exist_ok=True)
    with io.open(file_time_path, "w", encoding="utf-8") as f:
        f.write(value)


def datetime_slug():
    global EXPORT_TIME

    if EXPORT_TIME is None:
        now = datetime.now(timezone.utc)
        EXPORT_TIME = now.strftime("%Y%m%dT%H%M%SZ")

    return EXPORT_TIME


def upload_to_s3(dir, string):
    # For the following line of code to work, the following environment
    # variables need to be set:
    #
    # os.environ['AWS_ACCESS_KEY_ID']
    # os.environ['AWS_SECRET_ACCESS_KEY']
    s3 = boto3.resource("s3", region_name="us-east-2")
    bucket = s3.Bucket("kijiji-apartments")

    path = "csv_backups/{}".format(dir)
    bucket.put_object(Key=path, Body=string.encode("utf-8"))


def full_csv(_, items):
    file_like = io.StringIO()
    csv_writer = csv.DictWriter(file_like, fieldnames=FIELD_NAMES)

    csv_writer.writeheader()
    for item in items:
        csv_writer.writerow(item)

    return file_like.getvalue()


def trimmed_json(city, items):
    items_to_save = filter(makes_the_cut, items)

    trimmed_items = []
    for item in items_to_save:
        trimmed_items.append({key: item[key] for key in RETAINED_KEYS})

    to_export = {"city": city._asdict(), "apartments": trimmed_items}

    return json.dumps(to_export, default=_json_serial)


def _json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type {} is not serializable".format(type(obj)))
