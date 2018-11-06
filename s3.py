import json
import sys
import os


import boto3
import toml


kijiji_output_directory = os.environ["KIJIJI_OUTPUT_DIRECTORY"]
data_path = os.path.join(kijiji_output_directory, "latest", "out.json")


def download_latest():
    s3 = boto3.resource("s3", region_name="us-east-2")
    bucket_name = "kijiji-apartments"
    prefix = "v2/"

    bucket = s3.Bucket(bucket_name)

    objects = list(bucket.objects.filter(Prefix=prefix).all())
    newest_obj = sorted(objects, key=lambda o: o.key)[-1]

    print(f"Downloading {newest_obj.key}")

    os.makedirs(os.path.dirname(data_path), exist_ok=True)

    bucket.download_file(newest_obj.key, data_path)


def split():
    output_directory = os.path.join("site", "public")

    with open("scraper/scrape.toml") as f:
        start_data = toml.load(f)

    with open(data_path) as f:
        data = json.load(f)

    for city in start_data["cities"]:
        for ad_type in start_data["ad_types"]:
            city_id = city["id"]
            ad_id = ad_type["id"]

            offers = data["offers"][city_id][ad_id]

            to_export = {"city": city, "ad_type": ad_type, "offers": offers}

            json_name = f"{city_id}-{ad_id}.json"
            file_name = os.path.join(output_directory, json_name)

            with open(file_name, "w") as f:
                json.dump(to_export, f)


def main():
    if "--download" in sys.argv:
        download_latest()

    split()


if __name__ == "__main__":
    main()
