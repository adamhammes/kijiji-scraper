from math import sin, cos, sqrt, atan2, radians

from scraper.items import Apartment

FIELD_NAMES = list(Apartment.fields.keys())


def makes_the_cut(item):
    filters = [
        required_fields_present,
        sufficient_accuracy,
        values_not_none,
        within_distance,
    ]

    return all(func(item) for func in filters)


RETAINED_KEYS = {
    "origin",
    "housing_type",
    "address",
    "url",
    "headline",
    "description",
    "id",
    "date",
    "price",
    "is_furnished",
    "allows_animals",
    "latitude",
    "longitude",
    "num_rooms",
}


def required_fields_present(item):
    return all(key in item for key in RETAINED_KEYS)


CAN_BE_NONE = {"is_furnished", "allows_animals"}
NON_NONE_KEYS = RETAINED_KEYS - CAN_BE_NONE


def values_not_none(item):
    return all(item[key] is not None for key in NON_NONE_KEYS)


def sufficient_accuracy(item):
    confidence = int(item["address_confidence"])
    accuracy = item["address_accuracy"]

    return confidence >= 9 and accuracy == "ROOFTOP"


def within_distance(item):
    city = item["origin"].city
    city_latlon = city.latitude, city.longitude

    apartment_latlon = item["latitude"], item["latitude"]
    return distance_between_km(apartment_latlon, city_latlon) <= city.radius


RADIUS_OF_EARTH_KM = 6371


def distance_between_km(p1, p2):
    lat1, lon1 = radians(p1[0]), radians(p1[1])
    lat2, lon2 = radians(p2[0]), radians(p2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return c * RADIUS_OF_EARTH_KM
