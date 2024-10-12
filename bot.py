import asyncio
import json
import logging
import sys
import d20

from models import Class_info, PDF_READER, Races_info_ph, Spells_info, Weapons_info, Races_info_mpmm
from config import BOT_TOKEN as TOKEN
from commands import (
    CLASSES_INFO,
    HANDBOOK_COMMAND,
    HANDBOOK_BOT_COMMAND,
    RACES_INFO,
    HERO_CREATE,
    HERO_CREATE_COMMAND,
    SPELS_INFO,
    START_BOT_COMMAND,
    HELP_COMMAND,
    HELP_BOT_COMMAND,
    WEAPONS_INFO,
    PH_COMMAND,
    MPMM_COMMAND,
    DICE_ROLL_COMMAND,
    ROLL_DICE

)
from keyboards import (
    wiki_pages_markup,
    WikiCallback,
    pdf_pages_markup,
    PDFCallback,
    races_pages_markup,
    RaceCallback,
    spells_pages_markup,
    SpellsCallback,
    WeaponsCallback,
    weapons_pages_markup,
    hero_create_markup,
    RaceCallback2,
    races_pages_markup_mpmm,

)
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, URLInputFile
from aiogram.fsm.context import FSMContext


dp = Dispatcher()

session = AiohttpSession(proxy='http://proxy.server:3128')


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"""Привіт, це бот-помічник для гри Dungeon & Dragons. 
Що він вміє, і для чого він?:
— Довідник (Класи, спелси, раси і т.д) /handbook
— Як користуватись ботом, і зворотня допомога /help
— Помічник в створенні героя /hero_create
— /diceroll - Команда для кидання кістки (Наприклад /diceroll 1d1)
""")


@dp.message(DICE_ROLL_COMMAND)
async def dice_command(message: Message) -> None:
    try:
        dice_expression = message.text.split(' ', 1)[1]
        result = d20.roll(dice_expression)
        await message.answer(f"Результат: {result}")
    except IndexError:
        await message.answer("Будь ласка, введіть коректну команду. Наприклад: /diceroll 3d6")


@dp.message(HANDBOOK_COMMAND)
async def handbook(message: Message) -> None:
    await message.answer(f"""Вибери що тебе цікавить
— Інформація о класах /classes_info
— Інформація о расах /races_info
— Інформація о спелсах /spels_info
— Інформація о зброї /weapons_info""")


@dp.message(HELP_COMMAND)
async def help_handler(message: Message) -> None:
    await message.answer(f"""Цей бот є своєобразною енциклопедією по грі D&D
• Основні команди знаходяться в закладці "Menu"
• Якщо знайшли якісь помилки, сконтактуйтеся з розробником @kamujx""")


@dp.message(HERO_CREATE)
async def hero_creator(message: Message) -> None:
    data = get_pdf()
    markup = pdf_pages_markup(pdf_data=data)

    await message.answer(
        f"""Я допоможу створити тобі свого героя.
Натисни кнопку, щоб отримати лист для створення персонажа.""",
        reply_markup=markup,
    )


@dp.message(CLASSES_INFO)
async def classes_info(message: Message) -> None:
    data = get_classes()
    markup = wiki_pages_markup(wiki_list=data)
    await message.answer(
        "Вибери один з класів",
        reply_markup=markup
    )


@dp.message(RACES_INFO)
async def oneshot_wiki(message: Message) -> None:
    await message.answer("""Вибери з рекомендованих кампаній:
/PH - Players Handbook
/MPMM -  Mordenkainen Presents: Monsters of the Multiverse""")


@dp.message(PH_COMMAND)
async def handle_ph(message: Message) -> None:
    races = get_races_ph()
    markup = races_pages_markup(race_list=races)
    await message.answer(
        "Вибери расу:",
        reply_markup=markup
    )


@dp.message(MPMM_COMMAND)
async def handle_mpmm(message: Message) -> None:
    races = get_races_mpmm()
    markup = races_pages_markup_mpmm(race_list=races)
    await message.answer(
        "Вибери расу:",
        reply_markup=markup
    )


@dp.message(SPELS_INFO)
async def spells_info(message: Message) -> None:
    spell = get_spell()
    markup = spells_pages_markup(spell_list=spell)
    await message.answer(
        """Вибери заклинання:
Примітка: заклинання та змови даються не всім, класи які можуть використовувати магію це - Бард, Чарівник, Друїд, Жрець,  Винахідника, Чаклун, Паладін, Слідопит і Чарівник.
Також у слідопита з'являються заклинання лише з другого рівня""",
        reply_markup=markup
    )


@dp.message(WEAPONS_INFO)
async def weapons_info(message: Message) -> None:
    weapon = get_weapon()
    markup = weapons_pages_markup(weapon_list=weapon)
    await message.answer(
        "Вибери зброю:",
        reply_markup=markup)


@dp.callback_query(WikiCallback.filter())
async def wikicallback(callback: CallbackQuery, callback_data: WikiCallback) -> None:
    class_id = int(callback_data.id)
    class_data = get_classes(class_id=class_id)
    data = Class_info(**class_data)
    text = f"Kлас: {data.name_class}\n" \
           f"Інформація о класі: {data.description}\n" \
           f"Швидке створення персонажа: {data.creation}\n"

    photo = URLInputFile(data.picture, filename=f"{data.name_class}_picture.{data.picture.split('.')[-1]}")
    await callback.message.answer_photo(photo=photo, caption=text)


@dp.callback_query(PDFCallback.filter())
async def pdfcallback(callback: CallbackQuery, callback_data: PDFCallback) -> None:
    pdf_id = int(callback_data.id)
    pdf_data = get_pdf(pdf_id=pdf_id)
    data_pdf = PDF_READER(**pdf_data)
    await callback.message.answer_document(
        document=URLInputFile(data_pdf.file_path, filename=f"{data_pdf.file_name}_document.pdf"),
        caption=f"""{data_pdf.file_name}"""
    )
    await callback.message.answer(f"""Як заповнити аркуш персонажа: Ім'я персонажа — це ім'я вашого персонжа,як заповнити аркуш персонажа,праворуч є клас раса і т.д. вписуйте все що ви обрали і на світогляд вам треба вибрати щось із цього - "добро", "зло", "нейтрал", "хаос", також впишіть собі "досвід" 0
    
Сила спритність і т.д. ви заповнювали коли вибирали клас і расу, тому в віконці знизу вставляйте свої характеристики, у великому вікні ви підставляєте модифікатор який дорівнюватиме такій таблиці: 16-17 = +3, 15-14 = +2, 13-12 = +1, 11 -10 = 0, 9-8 = -1 бонус майстерності ставте +2, у натхнення залишайте порожнім, у ряткидки та навички вписуйте модифікатори які були ліворуч від них.

У ряткидках і навичках є порожні кружечки, натисніть і він стане повним, ви робите для класу у якого буде здібності до навичок і ряткидкив додавайте свій бонус майстерності, щоб дізнатися які навички та скидки у вас тут поки що допоможе https://longstoryshort.app/srd/

Клас обладунку це ваша броня за якою вороги повинні викинути те ж число або більше щоб завдати вам шкоди, швидкість, хіти та кістку хітів ви знову знайдете на сайті. вікно праворуч, а саме риси характеру, прихильності, ідеали характеру та слабкості ви знайдете на сайті за своєю передісторією.

Інше можна знайти в цьому боті:
/races_info
/classes_info
/spels_info
/weapons_info""")


@dp.callback_query(SpellsCallback.filter())
async def spellcallback(callback: CallbackQuery, callback_data: SpellsCallback) -> None:
    spell_id = int(callback_data.id)
    spell_data = get_spell(spell_id=spell_id)
    data = Spells_info(**spell_data)
    text = f"Заклинання: {data.name_spell}\n" \
           f"Рівень:{data.level}\n" \
           f"Тип: {data.type}\n" \
           f"Час дії:{data.time}\n" \
           f"Інформація о класі: {data.description}\n"
    await callback.message.edit_text(text)


@dp.callback_query(WeaponsCallback.filter())
async def weaponcallback(callback: CallbackQuery, callback_data: WeaponsCallback) -> None:
    weapon_id = int(callback_data.id)
    weapon_data = get_weapon(weapon_id=weapon_id)
    data = Weapons_info(**weapon_data)
    text = f"Назва зброї: {data.name_weapon}\n" \
           f"Урон: {data.damage}\n" \
           f"Вага: {data.weight}\n" \
           f"Тип:{data.type}\n"
    await callback.message.edit_text(text)


@dp.callback_query(RaceCallback.filter())
async def handle_race(callback_query: CallbackQuery, callback_data: RaceCallback) -> None:
    race_id = int(callback_data.id)
    race_data = get_races_ph(race_id=race_id)
    data = Races_info_ph(**race_data)
    text = f"Раса: {race_data['name_race']}\n" \
           f"Інформація о расі: {race_data['description']}\n"

    photo = URLInputFile(race_data['picture'],
                         filename=f"{race_data['name_race']}_picture.{race_data['picture'].split('.')[-1]}")
    await callback_query.message.answer_photo(photo=photo, caption=text)


@dp.callback_query(RaceCallback2.filter())
async def handle_race_mpmm(callback_query: CallbackQuery, callback_data: RaceCallback2) -> None:
    race_id = int(callback_data.id)
    race_data = get_races_mpmm(race_id=race_id)
    data = Races_info_mpmm(**race_data)
    text = f"Раса: {race_data['name_race']}\n" \
           f"Інформація о расі: {race_data['description']}\n"

    photo = URLInputFile(race_data['picture'],
                         filename=f"{race_data['name_race']}_picture.{race_data['picture'].split('.')[-1]}")
    await callback_query.message.answer_photo(photo=photo, caption=text)


def get_races_ph(file_path: str = "races_ph.json", race_id: int | None = None) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as fp:
        file = json.load(fp)
        if race_id != None and race_id < len(file):
            return file[race_id]
        return file


def get_races_mpmm(file_path: str = "races_mpmm.json", race_id: int | None = None) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as fp:
        file = json.load(fp)
        if race_id != None and race_id < len(file):
            return file[race_id]
        return file


def get_classes(file_path: str = "classes.json", class_id: int | None = None) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as fp:
        file = json.load(fp)
        if class_id != None and class_id < len(file):
            return file[class_id]
        return file


def get_pdf(file_path: str = "dnd_list.json", pdf_id: int | None = None) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as fp:
        file = json.load(fp)
        if pdf_id != None and pdf_id < len(file):
            return file[pdf_id]
        return file


def get_spell(file_path: str = "spels.json", spell_id: int | None = None) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as fp:
        file = json.load(fp)
        if spell_id != None and spell_id < len(file):
            return file[spell_id]
        return file


def get_weapon(file_path: str = "weapons.json", weapon_id: int | None = None) -> list[dict] | dict:
    with open(file_path, "r", encoding="utf-8") as fp:
        file = json.load(fp)
        if weapon_id != None and weapon_id < len(file):
            return file[weapon_id]
        return file


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands([
        START_BOT_COMMAND,
        HELP_BOT_COMMAND,
        HANDBOOK_BOT_COMMAND,
        HERO_CREATE_COMMAND,
        ROLL_DICE
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
