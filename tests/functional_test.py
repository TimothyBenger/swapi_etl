import os
import subprocess
from settings import OUTPUT_FILE_PATH
import csv


def test_finds_sorts_and_outputs():
    """
    Tests that application correctly calls the actual SWAPI and produces a CSV
    with characters in descending height order, which includes their name,
    species, height and # appearances
    """
    
    # Remove any existing output file
    if os.path.exists(OUTPUT_FILE_PATH):
        os.remove(OUTPUT_FILE_PATH) 

    # Execute the program
    subprocess.run(["python", "src/swapi_etl.py"])

    # Assert that CSV file exists
    assert os.path.exists(OUTPUT_FILE_PATH)

    with open(OUTPUT_FILE_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        list_of_output = list(reader)

        # Assert correct headings used
        assert list_of_output[0] == [
            'name',
            'species',
            'height',
            'appearances'
        ]

        # Assert heights (index 2) are in descending order
        height_tracker = 0
        for row in reversed(list_of_output[1:]):
            height = int(row[2])
            assert height >= height_tracker
            height_tracker = height

