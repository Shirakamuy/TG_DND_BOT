

from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

HERO_CREATE = Command("hero_create")
CLASSES_INFO = Command("classes_info")
RACES_INFO = Command("races_info")
SPELS_INFO = Command("spels_info")
HANDBOOK_COMMAND = Command("handbook")
HELP_COMMAND = Command("help")
WEAPONS_INFO = Command("weapons_info")
PH_COMMAND = Command("PH")
MPMM_COMMAND = Command("MPMM")
DICE_ROLL_COMMAND = Command("diceroll")

HERO_CREATE_COMMAND = BotCommand(command= "hero_create", description="Допомога в створенні твого героя")
HANDBOOK_BOT_COMMAND = BotCommand(command="handbook", description="Довідник, вибери те, що тебе цікавить")
START_BOT_COMMAND = BotCommand(command="start", description="Start")
HELP_BOT_COMMAND = BotCommand(command="help", description="Як користуватись ботом і зворотній зв'язок")
ROLL_DICE = BotCommand(command="diceroll", description="Кинути гральну кість")
