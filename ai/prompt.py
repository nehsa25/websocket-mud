class PromptSettings:

    room_tone = {
        "style": ["retro", "fantasy", "medieval", "sketch", "two-tone color"],
        "description": "<description of npc is here>"
    }

    player_tone = {
        "style": ["retro", "fantasy", "medieval", "sketch", "two-tone color"],
        "description": "<description of npc is here>"
    }

    npc_tone = {
        "style": ["retro", "fantasy", "medieval", "sketch", "two-tone color"],
        "description": "<description of npc is here>"
    }

    item_tone = {
        "style": ["retro", "fantasy", "medieval", "sketch", "two-tone color"],
        "description": "<description of item is here>"
    }

    monster_tone = {
        "style": ["retro", "fantasy", "medieval", "sketch", "two-tone color", "sinister"],
        "description": "<description of monster is here>"
    }

    @staticmethod
    def generate_prompt(tone, description):
        tone["description"] = description
        return tone
