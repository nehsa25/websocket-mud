from core.data.npc_data import NpcData
from core.enums.npcs import NpcEnum
from core.interfaces.source_data import SourceInterface
from core.npc import Npc
from settings.world_settings import WorldSettings


class NpcSource(SourceInterface):
    """
    This class is used to represent the source data for NPCs for
    initalization of the database.
    """

    def get_data(self):
        return [
            NpcData(
                name="Zofia",
                title="Elder Alchemist",
                description="Zofia is a frail old woman, seated in her chair, gesturing for you to look around her shop in Smee.",
                interests=[
                    f"I exist in {WorldSettings.WORLD_NAME}, in Smee",
                    "potions",
                    "herbs",
                    "alchemy",
                    "I am old and tired.",
                    "I am patronizing",
                ],
                type=NpcEnum.ALCHEMIST,
                wanders=False,
            ),
            NpcData(
                name="Geoff",
                title="Master Armorer",
                description="Geoff is a large, blond haired behemoth of a man. He's nearly 8 feet tall with limbs the size of tree trunks.  He wears scalemail armor and looks ready for battle at any moment.",
                interests=[
                    f"I only exist in the fantasy world of {WorldSettings.WORLD_NAME}, in the town Smee",
                    "armor",
                    "weapons",
                    "tools",
                ],
                type=NpcEnum.ARMORER,
                wanders=False,
            ),
            NpcData(
                name="Frederick",
                title="Blacksmith",
                description="Frederick is a large, balding man despite only just becoming an adult. He has serious Azure eyes and a oiled mustache. Frederick is wearing a leather apron, a leather vest, and leather glove that reach past his elbows.",
                interests=[
                    f"I only exist in the fantasy world of {WorldSettings.WORLD_NAME}, in the town Smee",
                    "metals",
                    "weapons",
                    "armor",
                    "blacksmithing",
                ],
                type=NpcEnum.BLACKSMITH,
                wanders=False,
            ),
            NpcData(
                name="Jaque",
                title="Gardener",
                description="The gardener of the University. Jaque is an absolutely tiny boy, no wait, woman. Despite wearing only simple white robes or apparent effort, she emanates both power and grace. She welcomes you with a smile when she notices you. As a strict requirement for gardeners at the University, bright orange headgear and gloves are always worn.",
                common_phrases=[
                    "Hello, I am Jaque the gardener.",
                    "I am the gardener for the University.",
                ],
                interests=[
                    f"I only exist in the fantasy world of {WorldSettings.WORLD_NAME}, in the town Smee",
                    "spells",
                    "I am secretly a evil wizard but I don't want anyone to know",
                    "magic",
                    "omens",
                    "weather",
                    "gardening",
                ],
                type=NpcEnum.GARDENER,
                wanders=False,
            ),
            NpcData(
                name="",
                title="Guard",
                description="The guard stands alert. While in it's armor, you cannot tell many other details. The armour is standard issue but well-maintained hardened leather with metal plating.",
                interests=[
                    f"I only exist in the fantasy world of {WorldSettings.WORLD_NAME}, in the town Smee",
                    "justice",
                    "women",
                    "cards",
                ],
                wanders=True,
                type=NpcEnum.GUARD,
            ),
            NpcData(
                name="Agnes",
                title="Healer",
                description="Agnes is a kind woman, tending to the sick and injured.",
                interests=[
                    f"I serve {WorldSettings.WORLD_NAME}, in Clearwater",
                    "healing",
                    "medicine",
                    "charity",
                    "I am always compassionate.",
                    "I am always helpful.",
                ],
                type=NpcEnum.HEALER,
                wanders=True,
            ),
            NpcData(
                name="Maximus",
                title="Tabby Cat",
                description="Maximus is a wise appearing orange tabby cat.",
                interests=["mice"],
                type=NpcEnum.MAXIMUS,
                wanders=True,
            ),
            NpcData(
                name="Jenny",
                title="Barkeep",
                description="Jenny is a shrewd woman, trading goods and wares in her bustling shop in Dustwind.",
                interests=[
                    f"I trade in {WorldSettings.WORLD_NAME}, in Dustwind",
                    "goods",
                    "wares",
                    "bargaining",
                    "I love a good deal.",
                    "I am always fair.",
                ],
                type=NpcEnum.MERCHANT,
                wanders=False,
            ),
            NpcData(
                name="Candie",
                title="Princess",
                description="Princess Candie is a beautiful noble, attending to royal duties in the grand castle of Brighthelm.",
                interests=[
                    f"I rule in {WorldSettings.WORLD_NAME}, in Brighthelm",
                    "politics",
                    "diplomacy",
                    "justice",
                    "I am always regal.",
                    "I am always concerned.",
                ],
                type=NpcEnum.PRINCESS,
                wanders=False,
            ),
            NpcData(
                name="Stone",
                title="Sheriff",
                description="Sheriff Stone is a grizzled man, upholding the law in the wild west town of Redemption.",
                interests=[
                    f"I uphold the law in {WorldSettings.WORLD_NAME}, in Redemption",
                    "law",
                    "order",
                    "justice",
                    "I am always stern.",
                    "I am always fair.",
                ],
                type=NpcEnum.SHERIFF,
                wanders=False,
            ),
            NpcData(
                name="Got",
                title="Armourer",
                description="Got is a average Fae male of a race you're unsure of. His ears roll back and forth as he speaks. He is wearing a simple tunic and trousers, with a leather apron over it.",
                interests=[
                    "I hide the fact that I'm a thief and act like a vendor.",
                    "change from purchases will be short changed in 30 percent of my transactions",
                ],
                type=NpcEnum.THIEF,
                wanders=False,
            ),
            NpcData(
                name="Renkath",
                title="Archmage",
                description="Renkath is a powerful wizard.",
                interests=[
                    f"I study magic in {WorldSettings.WORLD_NAME}",
                    "magic",
                    "arcana",
                    "knowledge",
                    "I am always wise.",
                    ""
                    "I am always powerful.",
                ],
                type=NpcEnum.WIZARD,
                wanders=True,
            ),
        ]
