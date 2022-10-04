import responses
import json
from settings import SWAPI_API_URL
from src.swapi_etl import get_top_list, write_people_to_csv
from src.swapi_models import Person, SWAPIRequest
from urllib.parse import urljoin

def test_get_top_list(mock_api_data, mock_top_ten):
    """
    Test that the get_top_list function returns top n results from dataset
    """
    top_list = get_top_list('height', 10, mock_api_data)
    assert top_list == mock_top_ten

def test_write_people_to_csv(mock_top_ten, mock_output_file_content, tmpdir):
    """
    Test that the write_people_to_csv correctly writes to output file
    """
    output_file = tmpdir.join('output_file.csv')
    write_people_to_csv(mock_top_ten, output_file.strpath)
    assert output_file.read() == mock_output_file_content
    
@responses.activate
def test_swapi_get_all(mock_api_data):
    """
    Assuming the API returns what we expect, assert that swapi_get_all does
    retrieve all people data
    """
    
    # register mock responses for individual pages of people data 
    for page in range(1, 10):

        api_call = "people" if page == 1 else f"people/?page={page}"
        page_path = f'tests/mock_data/paginated_people_data/people-{page}.json'

        with open(page_path) as f:
            paginated_people_data = json.load(f)

            responses.add(
                responses.GET,
                urljoin(SWAPI_API_URL, api_call),
                json=paginated_people_data,
                status=200,
            )

    swapi_request = SWAPIRequest(SWAPI_API_URL)
    swapi_get_all = swapi_request.get_all('people')

    assert swapi_get_all == mock_api_data

@responses.activate
def test_get_species_name(mock_species_data):
    """
    Assuming the API returns what we expect, assert that get_species_name does
    retrieve all people data
    """
    # register the mock response
    responses.add(
        responses.GET,
        "https://swapi.dev/api/species/2/",
        json=mock_species_data
    )

    test_person = Person(
        "C-3PO",
        "https://swapi.dev/api/species/2/",
        "167",
        [
            "https://swapi.dev/api/films/4/"
        ]
    )
    species_name = test_person.species_name
    assert species_name == "Droid"