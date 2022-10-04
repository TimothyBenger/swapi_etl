import pytest
import json

@pytest.fixture()
def mock_api_data():
    with open('tests/mock_data/mock_api_data.json') as f:
        mock_api_data = json.load(f)
        return mock_api_data

@pytest.fixture()
def mock_top_ten():
    with open('tests/mock_data/mock_top_ten.json') as f:
        mock_top_ten = json.load(f)
        return mock_top_ten

@pytest.fixture()
def mock_output_file_content():
    return open('tests/mock_data/mock_output_file.csv').read()

@pytest.fixture()
def mock_species_data():
    with open('tests/mock_data/mock_species_data.json') as f:
        mock_species_data = json.load(f)
        return mock_species_data
