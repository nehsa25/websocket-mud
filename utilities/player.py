import random
import time


class PlayerUtility:
    common_names = [
        "William",
        "Olga",
        "Omar",
        "Jill",
        "Jack",
        "John",
        "Jane",
        "Stefan",
        "Sven",
        "Svetlana",
        "Sergei",
        "Serge",
        "Isabella",
        "Isaac",
        "Ivan",
        "Igor",
        "Vlad",
        "Vladimir",
        "Dimi",
        "Dimitri",
        "Dimitrius",
        "Ali",
        "Alyssa",
        "Alicia",
        "Giles",
        "Gerald",
        "Geraldine",
        "Geoffrey",
        "Tom",
        "Thomas",
    ]

    common_sirnames = [
        "Smith",
        "Johnson",
        "Williams",
        "Jones",
        "Brown",
        "Davis",
        "Draper",
        "Chandler",
    ]

    common_identifiers = [
        "the Brave",
        "the Cowardly",
        "the Fool",
        "the greedy",
        "the Prideful",
        "the Wise",
        "the Strong",
        "Quickfoot",
        "the Swift",
    ]

    @staticmethod
    def generate_name(include_identifier=True, include_sirname=False):
        name_choice = random.choice(PlayerUtility.common_names)
        identifier = ""
        sirname_choice = ""

        # sirname list
        if include_sirname:
            sirname_choice = random.choice(PlayerUtility.common_sirnames)

        # title list
        if include_identifier:
            identifier = random.choice(PlayerUtility.common_identifiers)

        # combine name and title
        name = f"{sirname_choice.strip()} {name_choice.strip()} {identifier.strip()}".strip()
        return name

    @staticmethod
    def create_unique_name(self, original_name):
        name = f"{original_name}_{int(time.time())}".lower()
        return name
