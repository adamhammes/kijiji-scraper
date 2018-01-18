import csv
import datetime
import io

import boto3


class AmazonS3Pipeline:
    def open_spider(self, spider):
        self.items = []
    
    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        file_like = io.StringIO()
        field_names = self.items[0].fields

        csv_writer = csv.DictWriter(file_like, fieldnames=field_names)
        csv_writer.writeheader()
        for item in self.items:
            csv_writer.writerow(item)

        current_date = datetime.datetime.now()
        date_format = '%Y-%m-%d %H%M%S.csv'
        file_name = current_date.strftime(date_format)

        # For the boto3.resource('s3') call to work, the following environment variables need to be
        # set (or passed directly).
        #
        # os.environ['AWS_ACCESS_KEY_ID']
        # os.environ['AWS_SECRET_ACCESS_KEY']
        # os.environ['AWS_SESSION_TOKEN'] <- only needed if using temporary credentials
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('kijiji-apartments')

        backup_path = 'csv_backups/{}'.format(file_name)
        bucket.put_object(Key=backup_path, Body=file_like.getvalue().encode('utf-8'))
