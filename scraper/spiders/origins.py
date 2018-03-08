from enum import Enum
from typing import *

from dataclasses import dataclass, field


class LodgingType(Enum):
    COLOCATION = 'colocation'
    APARTMENT = 'apartment'


@dataclass
class ScraperOrigin:
    city: str
    lodging_type: LodgingType
    coords: Tuple[float, float]
    url: str


QC_COORDS = (46.83, -71.25)


QUEBEC_APARTMENTS = ScraperOrigin(
    'Québec',
    LodgingType.APARTMENT,
    QC_COORDS,
    'https://www.kijiji.ca/b-appartement-condo/ville-de-quebec/c37l1700124?ad=offering'
)


QUEBEC_COLOCS  = ScraperOrigin(
    'Québec',
    LodgingType.COLOCATION,
    QC_COORDS,
    'https://www.kijiji.ca/b-chambres-a-louer-colocataire/ville-de-quebec/c36l1700124?ad=offering'
)

