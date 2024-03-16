from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.prof_keyboards import make_row_keyboard

router = Router()

available_prob_names = ["С компьютером", "С принтером", "С интернетом"]
available_prob_grades = ["Простая", "Средняя", "Сложная"]


class ChoiceProbNames(StatesGroup):
    choice_prob_names = State()
    choice_prob_grades = State()


#Хэндлер на команду /prob
@router.message(Command('prob'))
async def cmd_prob(message: types.Message, state: FSMContext):
    name = message.chat.first_name
    await message.answer(
        f'Привет, {name}, какая у Вас проблема?',
        reply_markup=make_row_keyboard(available_prob_names)
    )
    await state.set_state(ChoiceProbNames.choice_prob_names)


@router.message(ChoiceProbNames.choice_prob_names, F.text.in_(available_prob_names))
async def prob_chosen(message: types.Message, state: FSMContext):
    await state.update_data(chosen_prob=message.text.lower())
    await message.answer(
        text='Спасибо, теперь выберите уровень проблемы',
        reply_markup=make_row_keyboard(available_prob_grades)
    )
    await state.set_state(ChoiceProbNames.choice_prob_grades)


@router.message(ChoiceProbNames.choice_prob_names)
async def prob_chosen_incorrectly(message: types.Message):
    await message.answer(
        'Я не знаю такой проблемы',
        reply_markup=make_row_keyboard(available_prob_names)
    )


@router.message(ChoiceProbNames.choice_prob_grades, F.text.in_(available_prob_grades))
async def grade_chosen(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        f'Вы выбрали уровень проблемы: {message.text.lower()}. Ваша проблема: {user_data.get("chosen_prob")}. Сейчас подключится специалист из этого отдела.',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(ChoiceProbNames.choice_prob_grades)
async def grade_chosen_incorrectly(message: types.Message):
    await message.answer(
        'Я не знаю такой проблемы',
        reply_markup=make_row_keyboard(available_prob_grades)
    )
