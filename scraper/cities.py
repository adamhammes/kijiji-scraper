from enum import Enum
from collections import namedtuple


class HousingType(Enum):
    Colocation = "colocation"
    Apartment = "apartment"


City = namedtuple(
    "City", ["name", "slug", "apartment_url", "colocation_url", "latitude", "longitude"]
)

montreal = City(
    name="Montréal",
    slug="montreal",
    apartment_url="https://www.kijiji.ca/b-appartement-condo/grand-montreal/c37l80002?ad=offering",
    colocation_url="https://www.kijiji.ca/b-chambres-a-louer-colocataire/grand-montreal/c36l80002?ad=offering",
    latitude=45.508840,
    longitude=-73.587810,
)

quebec = City(
    name="Québec City",
    slug="quebec",
    apartment_url="https://www.kijiji.ca/b-appartement-condo/ville-de-quebec/c37l1700124?ad=offering",
    colocation_url="https://www.kijiji.ca/b-chambres-a-louer-colocataire/ville-de-quebec/c36l1700124?ad=offering",
    latitude=46.8139,
    longitude=-71.2080,
)

starting_cities = [montreal, quebec]

slug_to_city = {city.slug: city for city in starting_cities}
