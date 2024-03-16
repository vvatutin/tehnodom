from aiogram import types, F, Router
from aiogram.filters.command import Command
import logging
import random
from keyboards.keyboards import kb1, kb2


router = Router()

#Хэндлер на команду /start
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    name = message.chat.first_name
    await message.answer(f'Привет, {name}', reply_markup=kb1)

# Хэндлер на команду /user
@router.message(Command('user'))
async def cmd_user(message: types.Message):
    # Отправляем ответное сообщение с информацией о пользователе
    user_info = f"Ваше имя пользователя в Телеграм: {message.from_user.username}\n" \
                f"Ваш ID пользователя в Телеграм: {message.from_user.id}"
    await message.reply(user_info)


#Хэндлер на команду /stop
@router.message(Command('stop'))
async def cmd_stop(message: types.Message):
    name = message.chat.first_name
    await message.answer(f'Пока, {name}')

#Хендлер на сообщения
@router.message(F.text)
async def msg_echo(message: types.Message):
    msg_user = message.text.lower()
    name = message.chat.first_name
    if 'о нас' in msg_user:
        await message.answer('Мы - компания ТехноДом, г. Челябинск.\n'
                             ' Мы оказываем специализированные услуги на дому для любых\n'
                             ' клиентов: решение всех проблем, начиная от установки\n'
                             ' программного обеспечения и настройки интернета,\n'
                             ' и заканчивая ремонтом компьютеров и удалением вирусов.')
    elif 'обратный звонок' == msg_user:
        await message.answer('Введите свой номер телефона, и мы в течении 15 минут Вам\n'
                             ' перезвоним. Наш специалист свяжется с вами и поможет\n'
                             ' решить все вопросы прямо на месте')
    else:
        await message.answer(f'Я не знаю такого слова')