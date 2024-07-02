
from enum import Enum

class He:
    pronoun = "he"
    possessive_pronoun = "his"
    possessive_pronoun2 = "him"
    
    sex = "male"
    
class She:
    pronoun = "she"
    possessive_pronoun = "her"
    possessive_pronoun2 = "her"
    sex = "female"

class It:
    pronoun = "it"
    possessive_pronoun = "its"
    possessive_pronoun2 = "her"
    sex = ""
    
class Pronouns(Enum):
    HE = He()
    SHE = She()
    IT = It()
    