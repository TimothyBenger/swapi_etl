import requests
from src.swapi_etl import post_to_httpbin
from settings import HTTPBIN_URL

def test_connection_to_api(mock_species_data):
    """
    Test that actual SWAPI returns expected response to a simple request
    """
    species_response = requests.get("https://swapi.dev/api/species/2/")
    assert species_response.json() == mock_species_data

def test_post_to_httpbin():
    """
    Test that posting a test file to httpbin receives OK status response
    """
    response = post_to_httpbin(
        'tests/mock_data/mock_output_file.csv',
        HTTPBIN_URL
    )
    assert response.status_code == 200