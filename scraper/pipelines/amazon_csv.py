import csv
import datetime
import logging
import io
import os

import boto3
from scrapy.exporters import CsvItemExporter


class AmazonS3Pipeline(object):
    def open_spider(self, spider):
        current_date = datetime.datetime.now()
        date_format = '%Y-%m-%d %H%M%S.csv'

        file_name = current_date.strftime(date_format)

        self.exporter = AmazonCsv(file_name)
    
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        with open('itemdump.txt', 'w') as f:
            f.write(item['url'])
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()


class AmazonCsv:
    def __init__(self, file_name):
        self.file_name = file_name
        self.items = []

    def export_item(self, item):
        self.items.append(item)

    def finish_exporting(self):
        file_like = io.StringIO()
        field_names = self.items[0].fields

        csv_writer = csv.DictWriter(file_like, fieldnames=field_names)
        csv_writer.writeheader()
        for item in self.items:
            csv_writer.writerow(item)

        # os.environ['AWS_ACCESS_KEY_ID']
        # os.environ['AWS_SECRET_ACCESS_KEY']
        # os.environ['AWS_SESSION_TOKEN'] <- only needed if using temporary credentials
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('kijiji-apartments')

        backup_path = 'csv_backups/{}'.format(self.file_name)
        bucket.put_object(Key=backup_path, Body=file_like.getvalue().encode('utf-8'))
