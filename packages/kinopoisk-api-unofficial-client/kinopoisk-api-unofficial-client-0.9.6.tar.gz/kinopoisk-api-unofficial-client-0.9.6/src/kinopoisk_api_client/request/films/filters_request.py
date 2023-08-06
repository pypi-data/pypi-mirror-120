from kinopoisk_api_client.client.http_method import HttpMethod
from kinopoisk_api_client.contract.request import Request
from kinopoisk_api_client.response.films.filters_response import FiltersResponse


class FiltersRequest(Request):
    METHOD: HttpMethod = HttpMethod.GET
    PATH: str = '/api/v2.1/films/filters'
    RESPONSE: type = FiltersResponse
