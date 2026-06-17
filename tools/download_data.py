import json
import os
import time
import requests


BASE_URL = "https://pokeapi.co/api/v2"
OUTPUT_DIR = "data/generated"

POKEMON_NAMES = list(range(1, 151))


def get_json(url):
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()


def get_text_by_language(entries, key= "effect", language= "es"):
    for entry in entries:
        if entry["language"]["name"] == language:
            return entry[key]

    for entry in entries:
        if entry["language"]["name"] == "en":
            return entry[key]

    return "No description found."

def get_name_by_language(names, language="es"):
    for name_entry in names:
        if name_entry["language"]["name"] == language:
            return name_entry["name"]

    for name_entry in names:
        if name_entry["language"]["name"] == "en":
            return name_entry["name"]

    return None


def format_name(api_name):
    return api_name.replace("-", " ").title()


def download_ability(ability_name):
    data = get_json(f"{BASE_URL}/ability/{ability_name}")

    spanish_name = get_name_by_language(data["names"], "es")

    if spanish_name is None:
        spanish_name = format_name(data["name"])

    description = get_text_by_language(
        data["flavor_text_entries"],
        "flavor_text",
        "es"
    )

    description = description.replace("\n", " ").replace("\f", " ")

    return {
        "name": spanish_name,
        "internal_name": format_name(data["name"]),
        "description": description
    }


def download_move(move_name):
    data = get_json(f"{BASE_URL}/move/{move_name}")

    spanish_name = get_name_by_language(data["names"], "es")

    if spanish_name is None:
        spanish_name = format_name(data["name"])

    description = get_text_by_language(
        data["flavor_text_entries"],
        "flavor_text",
        "es"
    )

    description = description.replace("\n", " ").replace("\f", " ")

    return {
        "name": spanish_name,
        "internal_name": format_name(data["name"]),
        "type": format_name(data["type"]["name"]),
        "category": format_name(data["damage_class"]["name"]),
        "power": str(data["power"]) if data["power"] is not None else "-",
        "accuracy": str(data["accuracy"]) if data["accuracy"] is not None else "-",
        "pp": str(data["pp"]) if data["pp"] is not None else "-",
        "priority": str(data["priority"]) if data["priority"] is not None else "0",
        "description": description
        
    }


def download_pokemon(pokemon_name):
    data = get_json(f"{BASE_URL}/pokemon/{pokemon_name}")
    species_data = get_json(data["species"]["url"])
    category = "Unknown Pokemon"

    for genus in species_data["genera"]:
        if genus["language"]["name"] == "es":
            category = genus["genus"]
            break

    description = "No description found."

    for entry in species_data["flavor_text_entries"]:
        if entry["language"]["name"] == "es":
            description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            break

    abilities = []
    for ability_slot in data["abilities"]:
        abilities.append(ability_slot["ability"]["name"])

    moves = [
        move_slot["move"]["name"]
        for move_slot in data["moves"]
    ]

    pokemon = {
        "number": str(data["id"]).zfill(3),
        "name": format_name(data["name"]),
        "type": " / ".join([
            format_name(type_slot["type"]["name"])
            for type_slot in data["types"]
        ]),
        "category": category,
        "height": str(data["height"] / 10) + " m",
        "weight": str(data["weight"] / 10) + " kg",
        "description": description,
        "stats": {
            format_name(stat_slot["stat"]["name"]): stat_slot["base_stat"]
            for stat_slot in data["stats"]
        },
        "moves": [
            format_name(move_name)
            for move_name in moves
        ],
        "abilities": [
            format_name(ability_name)
            for ability_name in abilities
        ],
        "sprite_url": data["sprites"]["front_default"]
    }

    return pokemon, moves, abilities

def download_sprite(sprite_url, pokemon_name):
    if sprite_url is None:
        return None

    sprites_dir = "assets/sprites"
    os.makedirs(sprites_dir, exist_ok=True)

    file_name = pokemon_name.lower().replace(" ", "-") + ".png"
    file_path = os.path.join(sprites_dir, file_name)

    if os.path.exists(file_path):
        return file_path

    response = requests.get(sprite_url, timeout=20)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    pokemon_data = {}
    move_data = {}
    ability_data = {}

    for pokemon_name in POKEMON_NAMES:
        print("Downloading Pokemon:", pokemon_name)

        pokemon, move_names, ability_names = download_pokemon(pokemon_name)

        sprite_path = download_sprite(
            pokemon["sprite_url"],
            pokemon["name"]
        )

        pokemon["sprite_path"] = sprite_path

        pokemon_data[pokemon["name"]] = pokemon

        for move_name in move_names:
            formatted_move_name = format_name(move_name)

            if formatted_move_name not in move_data:
                print("  Downloading Move:", move_name)
                move_data[formatted_move_name] = download_move(move_name)
                time.sleep(0.1)

        for ability_name in ability_names:
            formatted_ability_name = format_name(ability_name)

            if formatted_ability_name not in ability_data:
                print("  Downloading Ability:", ability_name)
                ability_data[formatted_ability_name] = download_ability(ability_name)
                time.sleep(0.1)

        time.sleep(0.1)

    with open(f"{OUTPUT_DIR}/pokemon_data.json", "w", encoding="utf-8") as file:
        json.dump(pokemon_data, file, indent=4, ensure_ascii=False)

    with open(f"{OUTPUT_DIR}/move_data.json", "w", encoding="utf-8") as file:
        json.dump(move_data, file, indent=4, ensure_ascii=False)

    with open(f"{OUTPUT_DIR}/ability_data.json", "w", encoding="utf-8") as file:
        json.dump(ability_data, file, indent=4, ensure_ascii=False)

    print("Done.")


if __name__ == "__main__":
    main()