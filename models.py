from pydantic import BaseModel

class Class_info(BaseModel):
    name_class: str
    description: str
    creation: str
    picture: str

class PDF_READER(BaseModel):
    file_path: str
    file_name: str

class Races_info_ph(BaseModel):
    name_race: str
    description: str
    picture: str

class Races_info_mpmm(BaseModel):
    name_race: str
    description: str
    picture: str

class Spells_info(BaseModel):
    name_spell: str
    level: int
    type: str
    time: str
    description: str

class Weapons_info(BaseModel):
    name_weapon: str
    damage: str
    weight: str
    type: str

