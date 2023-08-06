from dataclasses import dataclass, field

from typing import List

from kinopoisk_api_client.contract.response import Response
from kinopoisk_api_client.model.filter_country import FilterCountry
from kinopoisk_api_client.model.filter_genre import FilterGenre


@dataclass(frozen=True)
class FiltersResponse(Response):
    genres: List[FilterGenre] = field(default_factory=list)
    countries: List[FilterCountry] = field(default_factory=list)
