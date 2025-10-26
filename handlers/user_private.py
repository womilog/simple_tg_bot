from aiogram import F, types, Router
from aiogram.filters import CommandStart, StateFilter, or_f, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile

from common.scripts_for_track import get_trips
from kbds.reply import get_reply_keyboard
from common.scripts_for_weather import get_weather
from common.database import SchedulerDatabase, AudioDatabase

user_private_router = Router()

MAIN_KBDS = get_reply_keyboard(
    'Узнать погоду ☀️',
    'Узнать ближайшую электричку 🚝',
    'Аудио 🎵',
    'Планировщик 📋',
    placeholder='Выберите действие',
    sizes=(2,),
)


TRACKS_KBDS = get_reply_keyboard(
    'Заветы Ильича > Ярославский Вокзал',
    'Ярославский Вокзал > Заветы Ильича',
    'Заветы Ильича > Пушкино',
    'Пушкино > Заветы Ильича',
    'Заветы Ильича > Ростокино',
    'Ростокино > Заветы Ильича',
    placeholder='Выберите действие',
    sizes=(2,),
)

PLANS_KBDS = get_reply_keyboard(
    'Запись плана',
    'Чтение последнего',
    placeholder = 'Выберите действие',
    sizes = (2,),
)

AUDIOS_KBDS = get_reply_keyboard(
    'Получить аудио',
    'Получить все названия',
    'Получить названия автора',
    placeholder="Выберите действие",
    sizes=(2,),
)


class GiveWeather(StatesGroup):
    weather = State()


class GiveTracks(StatesGroup):
    track = State()


class GiveAudio(StatesGroup):
    choice = State()
    audio = State()
    author = State()


class GivePlans(StatesGroup):
    choice = State()
    write = State()


# Высылай клаву при вводе '/start'
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('[+] Что хотите сделать? 💪', reply_markup=MAIN_KBDS)


@user_private_router.message(StateFilter("*"), Command("отмена"))
@user_private_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("[+] Действия отменены 🙅", reply_markup=MAIN_KBDS)


@user_private_router.message(StateFilter(None), F.text == 'Аудио 🎵')
async def get_audio_choice(message: types.Message, state: FSMContext):
    await message.answer('[+] Выберите действие', reply_markup=AUDIOS_KBDS)
    await state.set_state(GiveAudio.choice)


@user_private_router.message(GiveAudio.choice)
async def set_audio_choice(message: types.Message, state: FSMContext):
    if message.text == 'Получить все названия':
        cl = AudioDatabase()
        res = cl.all_audios_name()
        await message.answer(res, reply_markup=MAIN_KBDS)
        await state.clear()
    elif message.text == 'Получить аудио':
        await message.answer("[+] Введите название аудио", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(GiveAudio.audio)
    else:
        await message.answer(f"[+] Введите название автора", reply_markup=MAIN_KBDS)
        await state.set_state(GiveAudio.author)


@user_private_router.message(GiveAudio.audio, F.text)
async def return_audio(message: types.Message, state: FSMContext):
    cl = AudioDatabase()
    try:
        binary_audio = cl.read_audio(message.text)
        await message.answer_audio(BufferedInputFile(binary_audio, message.text), reply_markup=MAIN_KBDS)
        await state.clear()
    except Exception as ex:
        await message.answer(f'[-] Произошла такая белебурда {ex}.\n[-] Скорее всего, вы неверно написали название.☹️\n[-] Впишите заново или напишите: "отмена"🙅')


@user_private_router.message(GiveAudio.author, F.text)
async def return_author_lst(message: types.Message, state: FSMContext):
    cl = AudioDatabase()
    try:
        author_list = cl.author_audios_name(message.text)
        print(author_list)
        await message.answer(author_list, reply_markup=MAIN_KBDS)
        await state.clear()
    except Exception as ex:
        await message.answer(f'[-] Произошла такая белебурда {ex}.\n[-] Скорее всего, вы неверно написали название.☹️\n[-] Впишите заново или напишите: "отмена"🙅')


@user_private_router.message(StateFilter(None), F.text == 'Узнать погоду ☀️')
async def get_city(message: types.Message, state: FSMContext):
    await message.answer("[+] Введите название города🏙", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(GiveWeather.weather)


@user_private_router.message(GiveWeather.weather, F.text)
async def return_weather(message: types.Message, state: FSMContext):
    try:
        await message.answer(get_weather(message.text), reply_markup=MAIN_KBDS)
        await state.clear()
    except Exception as ex:
        await message.answer(f'[-] Произошла такая белебурда {ex}.\n[-] Скорее всего, вы неверно написали город.☹️\n[-] Впишите заново город или напишите: "отмена"🙅')


@user_private_router.message(StateFilter(None), F.text == 'Узнать ближайшую электричку 🚝')
async def get_train(message: types.Message, state: FSMContext):
    await message.answer("[+] Выберите направление 🔛", reply_markup=TRACKS_KBDS)
    await state.set_state(GiveTracks.track)


@user_private_router.message(GiveTracks.track, F.text)
async def return_train(message: types.Message, state: FSMContext):
    await message.answer(get_trips(message.text), reply_markup=MAIN_KBDS)
    await state.clear()


@user_private_router.message(StateFilter(None), F.text == "Планировщик 📋")
async def get_type_schdl(messsage: types.Message, state: FSMContext):
    await messsage.answer("[+] Выберите действие", reply_markup=PLANS_KBDS)
    await state.set_state(GivePlans.choice)


@user_private_router.message(GivePlans.choice, F.text)
async def return_answr_kbrd(message: types.Message, state: FSMContext):
    if message.text == 'Запись плана':
        await message.answer("[+] Прописывай план через ', '")
        await state.set_state(GivePlans.write)
    else:
        scheduler_db = SchedulerDatabase()
        text = scheduler_db.read_last_schedule()
        text = ''.join(['-' + x + '\n' for x in text.split(', ')])
        await message.answer(text, reply_markup=MAIN_KBDS)
        await state.clear()


@user_private_router.message(GivePlans.write, F.text)
async def write_plan(message: types.Message, state: FSMContext):
    scheduler_db = SchedulerDatabase()
    data = str(message.text)
    flag = scheduler_db.write_schedule(data)
    if flag:
        await message.answer("[+] Планы записаны в бд!", reply_markup=MAIN_KBDS)
    else:
        await message.answer("[+] Планы не записаны в бд(", reply_markup=MAIN_KBDS)
    await state.clear()



