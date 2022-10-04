import requests
import csv
from src.swapi_models import SWAPIRequest, Person
from urllib.parse import urljoin
from settings import HTTPBIN_URL, OUTPUT_FILE_PATH, SWAPI_API_URL

def main():
    people_list_request = SWAPIRequest(SWAPI_API_URL)
    people_list = people_list_request.get_all('people')
    ten_tallest = get_top_list('height', 10, people_list)
    write_people_to_csv(ten_tallest, OUTPUT_FILE_PATH)
    post_to_httpbin(OUTPUT_FILE_PATH, HTTPBIN_URL)

def get_top_list(attribute, top_n, full_list):
    """Return the top n people by attribute"""
    filtered_list = [d for d in full_list if d[attribute] != 'unknown'] 
    sorted_filtered_list = sorted(
        filtered_list, key=lambda x: int(x[attribute]), reverse=True)
    return sorted_filtered_list[:top_n]

def write_people_to_csv(people, filename):
    """
    Given a list of people, write to a CSV in the format:
    name, species, height, appearances
    """
    with open(filename, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['name', 'species', 'height', 'appearances'])
        for person in people:
            person_ = Person(
                name = person.get('name'),
                species_url = "".join(person.get('species')),
                height = person.get('height'),
                films = person.get('films')
            )
            writer.writerow([
                person_.name,
                person_.species_name,
                person_.height,
                person_.no_films])

def post_to_httpbin(output_filename, httpbin_url):
    with open(output_filename, 'rb') as f:
        return requests.post(
            urljoin(httpbin_url, "post"),
            files={output_filename: f}
        )

if __name__ == '__main__':
    main()
