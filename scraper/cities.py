from typing import NamedTuple
from types import SimpleNamespace

import toml


class City(NamedTuple):
    id: str
    name_french: str
    name_english: str
    kijiji_id: str
    kijiji_name: str
    longitude: float
    latitude: float
    radius: float


class AdType(NamedTuple):
    id: str
    kijiji_id: str
    kijiji_name: str


class StartingPoint(NamedTuple):
    url: str
    city: City
    ad_type: AdType

    def normalized(self):
        return {"url": self.url, "city_id": self.city.id, "ad_type_id": self.ad_type.id}


def load_start_config():
    data = toml.load("scraper/scrape.toml")

    return {
        "cities": [City(**d) for d in data["cities"]],
        "ad_types": [AdType(**d) for d in data["ad_types"]],
    }


def generate_starting_points(start_config):
    for city in start_config["cities"]:
        for ad_type in start_config["ad_types"]:
            url = "https://kijiji.ca"
            url += f"/{ad_type.kijiji_name}/{city.kijiji_name}"
            url += f"/{ad_type.kijiji_id}{city.kijiji_id}"
            url += "?ad=offering"

            yield StartingPoint(url=url, city=city, ad_type=ad_type)


def starting_cities(start_config):
    return start_config["citites"]


def ad_types(start_config):
    return start_config["ad_types"]


if __name__ == "__main__":
    config = load_start_config()
    for s in generate_starting_points(config):
        print(s.url)
