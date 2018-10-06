from collections import defaultdict
import csv
from datetime import date, datetime, timezone
import io
import json
import logging
import os

import boto3

from scraper.items import Apartment
from ..cities import load_start_config, AdType, City, StartingPoint
from .makes_the_cut import makes_the_cut, RETAINED_KEYS


EXPORT_TIME = None
FIELD_NAMES = list(Apartment.fields.keys())
OUTPUT_DIRECTORY = os.environ["KIJIJI_OUTPUT_DIRECTORY"]
LATEST_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, "latest")


class ItemCollector:
    def open_spider(self, spider):
        self.version = spider.version
        self.full_scrape = spider.full_scrape

        config = load_start_config()

        self.cities = config["cities"]
        self.ad_types = config["ad_types"]

        self.export_data = {
            "cities": self.cities,
            "ad_types": self.ad_types,
            "date_collected": datetime_slug(),
            "data_version": self.version,
            "offers": {},
        }

        for city in self.cities:
            self.export_data["offers"][city.id] = {}

            for ad_type in self.ad_types:
                self.export_data["offers"][city.id][ad_type.id] = []

        logging.debug(self.export_data)

    def process_item(self, item, _):
        city = item["origin"].city
        ad_type = item["origin"].ad_type

        item["origin"] = item["origin"].normalized()

        self.export_data["offers"][city.id][ad_type.id].append(item)
        return item

    def close_spider(self, _):
        data = to_json(self.export_data)
        export(data, "out.json", self.full_scrape, self.version)


def export(value, exporter_name, full_scrape, version):
    latest_path = os.path.join(LATEST_DIRECTORY, exporter_name)
    os.makedirs(os.path.dirname(latest_path), exist_ok=True)
    with io.open(latest_path, "w", encoding="utf-8") as f:
        f.write(value)

    time_path = os.path.join(datetime_slug(), exporter_name)

    # if full_scrape:
    #     upload_to_s3(time_path, value, version)
    upload_to_s3(time_path, value, version)

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


def normalize_origin(item):
    origin = item["origin"]

    normalized_origin = {
        "url": origin.url,
        "city_id": origin.city.id,
        "ad_type_id": origin.ad_type.id,
    }

    item["origin"] = normalized_origin

    return item


def upload_to_s3(dir, string, version):
    # For the following line of code to work, the following environment
    # variables need to be set:
    #
    # os.environ['AWS_ACCESS_KEY_ID']
    # os.environ['AWS_SECRET_ACCESS_KEY']
    s3 = boto3.resource("s3", region_name="us-east-2")
    bucket = s3.Bucket("kijiji-apartments")

    base_path = "v" + str(version)
    path = "{}/{}".format(base_path, dir)

    logging.debug("s3path")
    logging.debug(path)
    logging.debug(version)

    bucket.put_object(Key=path, Body=string.encode("utf-8"))


def full_csv(_, items):
    file_like = io.StringIO()
    csv_writer = csv.DictWriter(file_like, fieldnames=FIELD_NAMES)

    csv_writer.writeheader()
    for item in items:
        csv_writer.writerow(item)

    return file_like.getvalue()


def to_json(data):
    return json.dumps(data, default=_json_serial)


def _json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    if isinstance(obj, (Apartment)):
        return dict(obj)

    if isinstance(obj, (City, AdType, StartingPoint)):
        return obj._asdict()

    import pdb

    pdb.set_trace()

    raise TypeError("Type {} is not serializable".format(type(obj)))
