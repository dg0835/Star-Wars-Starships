import requests
from pprint import pprint
import pymongo

url = "https://swapi.dev/api/starships"

client = pymongo.MongoClient()
db = client['starwars']

def get_api_json(url):

    # Get information from the API in the URL in json format

    response = requests.get(url)
    return response.json()

def go_to_next_page(next_page):

    # Checks if a next page exists. If so, return the data in json format. If not, throw an exception

    try:
        data = get_api_json(next_page)
        return data

    except requests.exceptions.MissingSchema:
        print("There is no valid next page. the program will now stop scraping.")
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

        if not current_data:
            break

    return starships


def find_pilot_id(name):
    print(f"Finding {name} ID")
    pilot = db.characters.find({"name": name})

    for p in pilot:
        print(p["_id"])
        return p["_id"]


def check_for_pilots(pilots):
    if len(pilots) == 0:
        return False
    return True


def replace_pilots(starships):
    for ship in starships:
        pilots = ship["pilots"]
        are_there_pilots = check_for_pilots(pilots)

        if are_there_pilots:
            new_pilot_list = []

            for p in pilots:

                p_info = get_api_json(p)
                p_name = p_info["name"]
                p_id = find_pilot_id(p_name)

                new_pilot_list.append(p_id)

            ship["pilots"] = new_pilot_list

    return starships


starship_api_info = get_api_json(url)

all_starships = store_starships(starship_api_info)

pprint(replace_pilots(all_starships))






