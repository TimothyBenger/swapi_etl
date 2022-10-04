import requests
from urllib.parse import urljoin

class SWAPIRequest():
    """Represents a request for resources from SWAPI"""

    def __init__(self, swapi_api_url):
        self.swapi_api_url = swapi_api_url

    def get_all(self, sw_resource_type, next="start"):
        """
        Given a SWAPI resource type, return all instances of it in SWAPI.
        Choose from 'films', 'people', 'planets', 'species', 'starships' and
        'vehicles' per https://swapi.dev/documentation
        """

        # first API call
        if next == "start":
            next = urljoin(self.swapi_api_url, sw_resource_type)
        
        response = requests.get(next).json()
        results = response.get('results')
        next = response.get('next')

        # base case -> all pages scraped
        if not next:
            return results
        # recursive case -> more pages to scrape
        else:
            return(results + self.get_all(sw_resource_type, next=next))

class Person():
    """
    Pared down version of the 'person' resource available from
    SWAPI
    """

    def __init__(self, name, species_url, height, films):
        self.name = name
        self.species_name = self._get_species_name(species_url)
        self.height = height
        self.no_films = len(films)

    def _get_species_name(self, species_url):
        """Given a 'person' resource, return the name of their species"""
        if not species_url:
            return ""
        species_info = requests.get(species_url).json()
        return species_info.get('name')