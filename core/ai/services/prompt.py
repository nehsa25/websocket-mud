class PromptSettings:
    room_tone = {
        "style": [
            "Expressionist",
            "line art drawing",
            "fantasy",
            "early 6th century AD",
            "two-tone color",
        ],
        "description": "<description of room is here>",
        "negative_prompt": [
            "photo",
            "realisticbad anatomy",
            "bad proportions",
            "bad perspective",
            "bad lighting",
            "bad color",
            "bad composition",
        ],
    }

    player_tone = {
        "style": [
            "Expressionist",
            "line art drawing",
            "fantasy",
            "early 6th century AD",
            "two-tone color",
        ],
        "description": "<description of player is here>",
        "negative_prompt": [
            "photo",
            "realisticbad anatomy",
            "bad proportions",
            "bad perspective",
            "bad lighting",
            "bad color",
            "bad composition",
        ],
    }

    npc_tone = {
        "style": [
            "Expressionist",
            "line art drawing",
            "fantasy",
            "early 6th century AD",
            "two-tone color",
        ],
        "description": "<description of npc is here>",
        "negative_prompt": [
            "photo",
            "realisticbad anatomy",
            "bad proportions",
            "bad perspective",
            "bad lighting",
            "bad color",
            "bad composition",
        ],
    }

    item_tone = {
        "style": [
            "Expressionist",
            "line art drawing",
            "fantasy",
            "early 6th century AD",
            "two-tone color",
        ],
        "description": "<description of item is here>",
        "negative_prompt": [
            "photo",
            "realisticbad anatomy",
            "bad proportions",
            "bad perspective",
            "bad lighting",
            "bad color",
            "bad composition",
        ],
    }

    monster_tone = {
        "style": [
            "Expressionist",
            "line art drawing",
            "fantasy",
            "early 6th century AD",
            "two-tone color",
            "sinister",
        ],
        "description": "<description of monster is here>",
        "negative_prompt": [
            "photo",
            "realisticbad anatomy",
            "bad proportions",
            "bad perspective",
            "bad lighting",
            "bad color",
            "bad composition",
        ],
    }

    @staticmethod
    def generate_prompt(tone, description):
        prompt = f'the style of the image is {", ".join(tone["style"])} and the description is "{description}". Negative: {", ".join(tone["negative_prompt"])}'
        return prompt
