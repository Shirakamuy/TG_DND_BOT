from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class WikiCallback(CallbackData, prefix="class", sep=";"):
    id: int
    name: str


def wiki_pages_markup(wiki_list: list[dict], offset: int | None = None, skip: int | None = None):
    builder = InlineKeyboardBuilder()
    for index, wiki_data in enumerate(wiki_list):
        name = wiki_data.get('name_class')
        if name is None:
            raise ValueError(f"Missing 'name_class' in wiki_data: {wiki_data}")
        callback_data = WikiCallback(id=index, name=name)
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    builder.adjust(1, repeat=True)
    return builder.as_markup()


class PDFCallback(CallbackData, prefix="pdf_file", sep=";"):
    id: int
    name: str
    file: str


def pdf_pages_markup(pdf_data: list[dict], offset: int | None = None, skip: int | None = None):
    builder = InlineKeyboardBuilder()

    for index, pdf_list in enumerate(pdf_data):
        link = pdf_list.get('file_path')
        if link is None:
            raise ValueError(f"Missing 'file_path' in pdf_list: {pdf_list}")

        name = "PDF файл"

        callback_data = PDFCallback(id=index, name=name, file=link)
        builder.button(
            text=name,
            callback_data=callback_data.pack()
        )
    builder.adjust(1, repeat=True)
    return builder.as_markup()


class RaceCallback(CallbackData, prefix="race"):
    id: int
    name: str

def races_pages_markup(race_list: list[dict], offset: int | None = None, skip: int | None = None):
    builder = InlineKeyboardBuilder()
    for index, race_data in enumerate(race_list):
        name = race_data.get('name_race')
        if name is None:
            raise ValueError(f"Missing 'name_race' in race_data: {race_data}")
        callback_data = RaceCallback(id=index, name=name)
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    builder.adjust(1, repeat=True)
    return builder.as_markup()

class RaceCallback2(CallbackData, prefix="race_mpmm"):
    id: int
    name: str

def races_pages_markup_mpmm(race_list: list[dict], offset: int | None = None, skip: int | None = None):
    builder = InlineKeyboardBuilder()
    for index, race_data in enumerate(race_list):
        name = race_data.get('name_race')
        if name is None:
            raise ValueError(f"Missing 'name_race' in race_data: {race_data}")
        callback_data = RaceCallback2(id=index, name=name)
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    builder.adjust(1, repeat=True)
    return builder.as_markup()


class SpellsCallback(CallbackData, prefix="spells"):
    id: int
    name: str

def spells_pages_markup(spell_list: list[dict], offset: int | None = None, skip: int | None = None):  # Исправлено название функции
    builder = InlineKeyboardBuilder()
    for index, spell_data in enumerate(spell_list):
        name = spell_data.get('name_spell')
        if name is None:
            raise ValueError(f"Missing 'name_spell' in spell_data: {spell_data}")
        callback_data = SpellsCallback(id=index, name=name)
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    builder.adjust(2, repeat=True)
    return builder.as_markup()


class WeaponsCallback(CallbackData, prefix="weapons"):
    id: int
    name: str

def weapons_pages_markup(weapon_list: list[dict], offset: int | None = None, skip: int | None = None):
    builder = InlineKeyboardBuilder()
    for index, weapon_data in enumerate(weapon_list):
        name = weapon_data.get('name_weapon')
        if name is None:
            raise ValueError(f"Missing 'name_weapon' in weapon_data: {weapon_data}")
        callback_data = WeaponsCallback(id=index, name=name)
        builder.button(
            text=f"{callback_data.name}",
            callback_data=callback_data.pack()
        )
    builder.adjust(2, repeat=True)
    return builder.as_markup()


def hero_create_markup():
    builder = InlineKeyboardBuilder()
    description = """Як заповнити аркуш персонажа: Ім'я персонажа — це ім'я вашого персонажа, вписуйте все, що ви обрали. ...
    Щоб дізнатися більше про раси, класи, заклинання та зброю, скористайтесь командами:
    /races_info
    /classes_info
    /spells_info
    /weapons_info"""

    builder.button(
        text="Дізнатись більше про створення персонажа",
        callback_data="character_creation_info"
    )

    builder.adjust(1)
    return builder.as_markup(), description

