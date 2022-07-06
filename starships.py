import requests
from pprint import pprint
import pymongo

url = "https://swapi.dev/api/starships"

client = pymongo.MongoClient()
db = client['starwars']


def get_api_json(url: str):

    # Get information from the API in the URL in json format

    response = requests.get(url)
    return response.json()


def go_to_next_page(next_page: str):

    # Checks if a next page exists. If so, return the data in json format. If not, throw an exception

    try:
        data = get_api_json(next_page)
        return data

    except requests.exceptions.MissingSchema:
        print("There is no valid next page. the program will now stop scraping.")
        return False


def store_starships(data: list):

    # Stores dictionaries (containing info about starships) into one list.

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


def find_pilot_id(name: str):

    # Using the pilot's name, finds the pilot's ID from the local MongoDB star wars characters database.

    print(f"Finding {name} ID")
    pilot = db.characters.find({"name": name})

    for p in pilot:
        print(p["_id"])
        return p["_id"]


def check_for_pilots(pilots: list):

    # Checks if the starship has any pilots

    if len(pilots) == 0:
        return False
    return True


def replace_pilots(starships: list):

    # For each starship, replaces urls in the list of pilots with the pilot IDs.

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


def upload_data_to_mongodb(data):

    # Upload all the starship data to the local MangoDB Database

    collection = db["starships"]

    for d in data:

        inserted = collection.insert_one(d)


def drop_collection():

    # Drops the starships collection

    collection = db["starships"]

    collection.drop()


starship_api_info = get_api_json(url)  # Pass in the url of the page that we wish to scrape from

all_starships = store_starships(starship_api_info)  # Create a list containing all starships and their metadata

data_to_insert = replace_pilots(all_starships)  # Replace pilots with their IDs

drop_collection()
upload_data_to_mongodb(data_to_insert)






