from aiogram import F, types, Router
from aiogram.filters import CommandStart, StateFilter, or_f, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from common.scripts_for_track import get_trips
from kbds.reply import get_keyboard
from common.scripts_for_weather import get_weather

user_private_router = Router()

MAIN_KBDS = get_keyboard(
    'Узнать погоду ☀️',
    'Узнать ближайшую электричку 🚝',
    placeholder='Выберите действие',
    sizes=(2,),
)


TRACKS_KBDS = get_keyboard(
    'Заветы-Ильича--Ярославский Вокзал',
    'Ярославский Вокзал--Заветы-Ильича',
    'Заветы-Ильича--Пушкино',
    'Пушкино--Заветы-Ильича',
    placeholder='Выберите действие',
    sizes=(2,),
)


class GiveWeather(StatesGroup):
    weather = State()


class GiveTracks(StatesGroup):
    track = State()



# Высылай клаву при вводе '/start'
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('[+] Что хотите сделать? 💪', reply_markup=MAIN_KBDS)


@user_private_router.message(StateFilter(None), F.text == 'Узнать погоду ☀️')
async def get_city(message: types.Message, state: FSMContext):
    await message.answer("[+] Введите название города🏙", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(GiveWeather.weather)


@user_private_router.message(StateFilter("*"), Command("отмена"))
@user_private_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("[+] Действия отменены 🙅", reply_markup=MAIN_KBDS)


@user_private_router.message(GiveWeather.weather, F.text)
async def return_weather(message: types.Message, state: FSMContext):
    try:
        await message.answer(get_weather(message.text), reply_markup=MAIN_KBDS)
        await state.clear()
    except Exception as ex:
        await message.answer(f'[-] Произошла такая белебурда {ex}.\n[-] Скорее всего, вы неверно написали город.☹️\n[-] Впишите заново город или напишите: "отмена"🙅')


@user_private_router.message(StateFilter(None), F.text == 'Узнать ближайшую электричку 🚝')
async def get_city(message: types.Message, state: FSMContext):
    await message.answer("[+] Выберите направление 🔛", reply_markup=TRACKS_KBDS)
    await state.set_state(GiveTracks.track)


@user_private_router.message(GiveTracks.track, F.text)
async def return_weather(message: types.Message, state: FSMContext):
    await message.answer(get_trips(message.text), reply_markup=MAIN_KBDS)
    await state.clear()




