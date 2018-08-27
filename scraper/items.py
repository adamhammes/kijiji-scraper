import scrapy


class Apartment(scrapy.Item):
    # Fields that don't need processing
    starting_city = scrapy.Field()
    city_slug = scrapy.Field()
    housing_type = scrapy.Field()
    url = scrapy.Field()
    main_image_url = scrapy.Field()
    headline = scrapy.Field()
    description = scrapy.Field()
    title = scrapy.Field()
    date_accessed = scrapy.Field()  # datetime

    # Unvalidated/unprocessed
    raw_id = scrapy.Field()
    raw_date = scrapy.Field()  # nullable
    raw_address = scrapy.Field()
    raw_price = scrapy.Field()
    raw_bathrooms = scrapy.Field()
    raw_furnished = scrapy.Field()
    raw_animals = scrapy.Field()  # nullable

    # Validated fields
    id = scrapy.Field()  # int
    date = scrapy.Field()  # datetime, nullable
    price = scrapy.Field()  # integer (in cents) - nullable in the case of "on demand"
    num_bathrooms = scrapy.Field()
    is_furnished = scrapy.Field()
    allows_animals = scrapy.Field()  # nullable

    # Synthesized fields
    address_confidence = scrapy.Field()  # int
    address_accuracy = scrapy.Field()  # string
    address = scrapy.Field()
    latitude = scrapy.Field()  # float
    longitude = scrapy.Field()  # float
    postal = scrapy.Field()  # string
    city = scrapy.Field()

    num_rooms = scrapy.Field()  # float (e.g. 4.5)
