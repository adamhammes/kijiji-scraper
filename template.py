import os

import toml
from jinja2 import Environment, FileSystemLoader, Template

from scraper.cities import City, AdType


template_directory = os.path.abspath("site_templates")
output_directory = "site/public"


def out_path(relative_path):
    return os.path.join(output_directory, relative_path)


def write_template(template, path, data):
    rendered = template.render(data)
    destination = out_path(path)

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    with open(out_path(path), "w") as f:
        f.write(rendered)


def load_start_config():
    data = toml.load("scraper/scrape.toml")

    return {
        "cities": [City(**d) for d in data["cities"]],
        "ad_types": [AdType(**d) for d in data["ad_types"]],
    }


def main():
    start_data = load_start_config()
    jinja_env = Environment(loader=FileSystemLoader(template_directory))

    index_template = jinja_env.get_template("home.html")
    city_template = jinja_env.get_template("city.html")
    listing_template = jinja_env.get_template("listing.html")

    write_template(index_template, "index.html", start_data)

    for city in start_data["cities"]:
        city_path = f"{city.id}/index.html"
        write_template(
            city_template, city_path, {"city": city, "ad_types": start_data["ad_types"]}
        )

        for ad_type in start_data["ad_types"]:
            listing_path = f"{city.id}/{ad_type.id}/index.html"
            write_template(
                listing_template, listing_path, {"city": city, "ad_type": ad_type}
            )


if __name__ == "__main__":
    main()
