import json


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


POKEMON_DATA = load_json("data/generated/pokemon_data.json")
MOVE_DATA = load_json("data/generated/move_data.json")
ABILITY_DATA = load_json("data/generated/ability_data.json")