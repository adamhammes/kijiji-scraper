import csv
from datetime import date, datetime, timezone
import io
import json
import os

import boto3

from scraper.items import Apartment
from .makes_the_cut import makes_the_cut, RETAINED_KEYS


FIELD_NAMES = list(Apartment.fields.keys())
OUTPUT_DIRECTORY = os.environ['KIJIJI_OUTPUT_DIRECTORY']
LATEST_DIRECTORY = os.path.join(OUTPUT_DIRECTORY, 'latest')

BUCKET_NAME = 'kijiji-apartments'
S3_BACKUP_PATH = 'csv-backups'


class ItemCollector:
    def open_spider(self, spider):
        self.full_scrape = spider.full_scrape
        self.items = []

        self.exporters = [
            (full_csv, 'all_items.csv'),
            (trimmed_json, 'trimmed_values.json')
        ]

    def process_item(self, item, _):
        self.items.append(item)
        return item

    def close_spider(self, _):
        if self.full_scrape:
            s3_init()

        date_string = datetime_slug()

        for exporter, name in self.exporters:
            value = exporter(self.items)

            latest_path = os.path.join(LATEST_DIRECTORY, name)
            os.makedirs(os.path.dirname(latest_path), exist_ok=True)
            with io.open(latest_path, 'w', encoding='utf-8') as f:
                f.write(value)

            time_path = os.path.join(date_string, name)

            if self.full_scrape:
                latest_path = os.path.join('latest', name)
                upload_to_s3(latest_path, value)
                upload_to_s3(time_path, value)

            file_time_path = os.path.join(OUTPUT_DIRECTORY, time_path)
            os.makedirs(os.path.dirname(file_time_path), exist_ok=True)
            with io.open(file_time_path, 'w', encoding='utf-8') as f:
                f.write(value)


def datetime_slug():
    now = datetime.now(timezone.utc)
    return now.strftime('%Y%m%dT%H%M%SZ')


def s3_init():
    s3 = boto3.resource('s3', region_name='us-east-2')
    bucket = s3.Bucket(BUCKET_NAME)

    latest_path = os.path.join(S3_BACKUP_PATH, 'latest/')
    for key in bucket.list(latest_path):
        key.delete()


def upload_to_s3(file_path, string):
    # For the following line of code to work, the following environment
    # variables need to be set:
    #
    # os.environ['AWS_ACCESS_KEY_ID']
    # os.environ['AWS_SECRET_ACCESS_KEY']
    s3 = boto3.resource('s3', region_name='us-east-2')
    bucket = s3.Bucket(BUCKET_NAME)

    full_path = os.path.join(S3_BACKUP_PATH, file_path)
    bucket.put_object(Key=full_path, Body=string.encode('utf-8'))


def full_csv(items):
    file_like = io.StringIO()
    csv_writer = csv.DictWriter(file_like, fieldnames=FIELD_NAMES)

    csv_writer.writeheader()
    for item in items:
        csv_writer.writerow(item)

    return file_like.getvalue()


def trimmed_json(items):
    items_to_save = filter(makes_the_cut, items)

    trimmed_items = []
    for item in items_to_save:
        trimmed_items.append({key: item[key] for key in RETAINED_KEYS})

    return json.dumps(trimmed_items, default=_json_serial)


def _json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type {} is not serializable".format(type(obj)))
