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


class ItemCollector:
    def open_spider(self, _):
        self.items = []

        self.exporters = [
            (full_csv, 'all_items.csv'),
            (trimmed_json, 'trimmed_values.json')
        ]

    def process_item(self, item, _):
        self.items.append(item)
        return item

    def close_spider(self, _):
        date_string = datetime_slug()

        for exporter, name in self.exporters:
            value = exporter(self.items)

            latest_path = os.path.join(LATEST_DIRECTORY, name)
            os.makedirs(os.path.dirname(latest_path), exist_ok=True)
            with io.open(latest_path, 'w', encoding='utf-8') as f:
                f.write(value)

            time_path = os.path.join(date_string, name)
            upload_to_s3(time_path, value)

            file_time_path = os.path.join(OUTPUT_DIRECTORY, time_path)
            os.makedirs(os.path.dirname(file_time_path), exist_ok=True)
            with io.open(file_time_path, 'w', encoding='utf-8') as f:
                f.write(value)


def datetime_slug():
    now = datetime.now(timezone.utc)
    return now.strftime('%Y%m%dT%H%M%SZ')


def upload_to_s3(dir, string):
    # For the following line of code to work, the following environment
    # variables need to be set:
    #
    # os.environ['AWS_ACCESS_KEY_ID']
    # os.environ['AWS_SECRET_ACCESS_KEY']
    s3 = boto3.resource('s3', region_name='us-east-2')
    bucket = s3.Bucket('kijiji-apartments')

    path = 'csv_backups/{}'.format(dir)
    bucket.put_object(Key=path, Body=string.encode('utf-8'))


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
