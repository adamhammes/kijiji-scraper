import csv
from datetime import date, datetime
import io
import json
import os

import boto3

from scraper.items import Apartment


FIELD_NAMES = list(Apartment.fields.keys())
OUTPUT_DIRECTORY = os.environ['KIJIJI_OUTPUT_DIRECTORY']


class ItemCollector:
    def open_spider(self, _):
        self.items = []

        self.exporters = [
            s3_upload,
            full_csv,
            trimmed_json
        ]

    def process_item(self, item, _):
        self.items.append(item)
        return item

    def close_spider(self, _):
        for exporter in self.exporters:
            exporter(self.items)


def s3_upload(items):
    file_like = io.StringIO()
    csv_writer = csv.DictWriter(file_like, fieldnames=FIELD_NAMES)
    
    csv_writer.writeheader()
    for item in items:
        csv_writer.writerow(item)

    current_date = datetime.now()
    date_format = '%Y-%m-%d %H%M%S.csv'
    file_name = current_date.strftime(date_format)

    # For the following line of code to work, the following environment 
    # variables need to be set:
    #
    # os.environ['AWS_ACCESS_KEY_ID']
    # os.environ['AWS_SECRET_ACCESS_KEY']
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('kijiji-apartments')

    backup_path = 'csv_backups/{}'.format(file_name)
    payload = file_like.getvalue().encode('utf-8')
    bucket.put_object(Key=backup_path, Body=payload)


def full_csv(items):
    file_name = os.path.join(OUTPUT_DIRECTORY, 'full_scrape.csv')

    with open(file_name, 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
         
        csv_writer.writeheader()
        for item in items:
            csv_writer.writerow(item)


def trimmed_json(items):
    retained_keys = [
        'url',
        'headline',
        'description',
        'id',
        'date',
        'price',
        'is_furnished',
        'allows_animals',
        'latitude',
        'longitude',
        'num_rooms',
    ]

    trimmed_items = []
    for item in items:
        assert [field in item for field in retained_keys]
        trimmed_items.append({key: item[key] for key in retained_keys})
    
    file_name = os.path.join(OUTPUT_DIRECTORY, 'trimmed_values.json')
    with open(file_name, 'w') as f:
        f.write(json.dumps(trimmed_items, default=json_serial)) 


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type {} is not serializable".format(type(obj)))

