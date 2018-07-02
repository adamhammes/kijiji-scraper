from collections import namedtuple

City = namedtuple("City", ["name", "slug", "start_url", "latitude", "longitude"])

montreal = City(
    name="Montréal",
    slug="montreal",
    start_url="https://www.kijiji.ca/b-appartement-condo/grand-montreal/c37l80002?ad=offering",
    latitude=45.508840,
    longitude=-73.587810,
)

quebec = City(
    name="Québec City",
    slug="quebec",
    start_url="https://www.kijiji.ca/b-appartement-condo/ville-de-quebec/c37l1700124?ad=offering",
    latitude=46.8139,
    longitude=-71.2080,
)

starting_cities = [montreal, quebec]
