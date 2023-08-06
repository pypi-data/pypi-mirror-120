from dataclasses import dataclass

from kinopoisk_api_client.model.dictonary.fact_type import FactType


@dataclass
class Fact:
    text: str
    type: FactType
    spoiler: bool
