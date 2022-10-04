## Installation (Linux)

```bash
cd <project-root-directory>
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Usage

In the root directory of the project, create a `settings.py` file as per the
following example:

```python
HTTPBIN_URL = 'http://0.0.0.0:80/' # e.g. if deploying locally
OUTPUT_FILE_PATH = "ten_tallest.csv"
SWAPI_API_URL = "https://swapi.dev/api/"
```

From the root directory of the project, run:

```bash
. venv/bin/activate
export PYTHONPATH=$(pwd)
# Requires docker to be installed and port 80 to be available on the host
docker run -p 80:80 kennethreitz/httpbin
python src/swapi_etl.py
```

## Tests

```bash
. venv/bin/activate
export PYTHONPATH=$(pwd)
python -m pytest
```

## Notes

I decided to build my own classes / functions to interact with the API, rather
than using https://github.com/phalt/swapi-python, because:

* `swapi-python` seems to no longer be maintained:
    - e.g. still uses the url https://swapi.co instead of https://swapi.dev
* My own code ran faster in a quick test using `timeit` module (Ubuntu, 8 core
  / 3.8 GHz processor, 800MB/s internet connection):
    - `swapi.get_all("people")`: 2.5s
    - My `SWAPIRequest().get_all("people")` method: 0.24s
* I found `swapi-python` had some other limitations, like no built in
  functionality to sort in descending order

## Assumptions made

* Unknown heights are ignored
* Empty fields returned by API are left blank in output CSV file
* We are deploying httpbin locally on Docker

## Improvements for roadmap

* Account for the scenario where there are two or more heights in 10= position
* Was wary of introducing scope creep, so models are quite specific to what
  was required for the challenge, but would be good to extend swapi_models to
  include more resources
* Parameterise the resource type, number of resources listed, sorting order,
  and attributes written to the CSV file
* Test coverage focussed on happy paths. Add coverage for invalid function
  inputs, invalid API data, (e.g. unexpected types), API failure, httpbin being
  down, filesystem full etc.
* This application could sit behind an API which could accept the
  previously-mentioned parameters (resource type etc.)