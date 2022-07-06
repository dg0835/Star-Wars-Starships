import requests
from pprint import pprint
import pymongo

url = "https://swapi.dev/api/starships"

def get_api_json(url):

    # Get information from the API in the URL in json format

    response = requests.get(url)
    return response.json()

def go_to_next_page(next_page):

    try:
        data = get_api_json(next_page)
        return data

    except requests.exceptions.MissingSchema:
        print("There is no valid next page. the program will now stop scraping from the webpage.")
        return False

def store_starships(data):
    current_data = data
    starships = []

    while True:

        next_page = current_data["next"]
        starship_dicts = current_data["results"]

        for starship in starship_dicts:
            starships.append(starship)


        current_data = go_to_next_page(next_page)
        print(current_data) #prints the json of the page

        if not current_data:
            break

    pprint(starships)


starship_api_info = get_api_json(url)

store_starships(starship_api_info)


