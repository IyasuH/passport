from enum import Enum
from typing import List

class Location(Enum):
    Addis_Ababa = "Addis Ababa"
    Bahir_Dar = "Bahirdar"
    Hawassa = "Hawassa"
    Hosanna = "Hosanna"
    Dire_Dawa = "Dire Dawa"
    Adama = "Adama"

class Gender(Enum):
    Male = "Male"
    Female = "Female"

class NameType(Enum):
    Name = "name"
    Father_Name = "father_name"
    Grand_Father_Name = "grand_father_name"
