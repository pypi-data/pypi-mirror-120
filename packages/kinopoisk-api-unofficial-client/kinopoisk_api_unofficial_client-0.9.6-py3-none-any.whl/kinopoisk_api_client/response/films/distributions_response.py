from dataclasses import dataclass, field

from typing import List

from kinopoisk_api_client.contract.response import Response
from kinopoisk_api_client.model.distribution import Distribution


@dataclass(frozen=True)
class DistributionsResponse(Response):
    total: int
    items: List[Distribution] = field(default_factory=list)
