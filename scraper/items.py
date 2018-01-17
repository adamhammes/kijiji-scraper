import scrapy


class Apartment(scrapy.Item):
    # Fields that don't need processing
    url = scrapy.Field()
    main_image_url = scrapy.Field()
    headline = scrapy.Field()
    description = scrapy.Field()

    # Unvalidated/unprocessed
    raw_id = scrapy.Field()
    raw_date = scrapy.Field()
    raw_title = scrapy.Field()
    raw_address = scrapy.Field()
    raw_price = scrapy.Field()
    raw_bathrooms = scrapy.Field()
    raw_furnished = scrapy.Field()
    raw_animals = scrapy.Field()

    # Validated fields
    id = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    num_bathrooms = scrapy.Field()
    is_furnished = scrapy.Field()
    allows_animals = scrapy.Field()

    # Synthesized fields
    has_exact_address = scrapy.Field()
    address_confidence = scrapy.Field()
    address_accuracy = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    postal = scrapy.Field()
    city = scrapy.Field()

    num_rooms = scrapy.Field()
