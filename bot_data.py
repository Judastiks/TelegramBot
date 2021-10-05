import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from bot_id import telegram_token

boters = Bot(token=telegram_token)
disp = Dispatcher(boters)
response = requests.get("https://mhw-db.com/monsters")
data = response.json()


def get_data(message):
    url = "https://mhw-db.com/monsters?q={" + '"' + str("name") + '"' + ':' + '"' + str(message) + '"}'
    response = requests.get(url)
    datas = response.json()
    return datas


@disp.message_handler(commands=["start"])
async def start_comm(message: types.message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = KeyboardButton('Show monster base')
    but2 = KeyboardButton('Quit')
    markup.add(but1, but2)

    await boters.send_message(message.chat.id, 'Hellow, {0.first_name}!'.format(message.from_user), reply_markup=markup)


@disp.message_handler(content_types=['text'])
async def bot_message(message):
    info = []
    for element in range(len(data)):
        info.append(data[element]["name"])
    if message.chat.type == 'private':
        if message.text == 'Show monster base':
            await message.reply(('\n'.join(info)))

        elif message.text in info:
            chatID = message.chat.id
            datas = get_data(message.text)

            monster = datas[0]["name"]
            description = datas[0]["description"]
            species = datas[0]["species"]

            markup = InlineKeyboardMarkup(resize_keyboard=True)
            btn1 = InlineKeyboardButton('Weaknesses', callback_data='btn1')
            btn2 = InlineKeyboardButton('Resistances', callback_data='btn2')
            btn3 = InlineKeyboardButton('Locations', callback_data='btn3')
            markup.add(btn1, btn2, btn3)

            await boters.send_photo(chatID, open('Pic/'+str(message.text)+ '.png','rb'))
            await boters.send_message(chatID, f"Name : {monster}\nDescription : {description}\nSpecies: {species}")
            await boters.send_message(chatID, f'{message.text}', reply_markup=markup)
        elif message.text == 'Quit':
            await boters.send_message(message.chat.id, '_', reply_markup=types.ReplyKeyboardRemove())
        else:
            await boters.send_message(message.chat.id,"Check the name of the monster")


@disp.callback_query_handler(text_contains='btn1')
async def weaknes(call):
    datas = get_data(call.message.text)
    weaknesses = datas[0]["weaknesses"]
    elem = []
    weakn = []
    star = []
    stars = []
    for i in weaknesses:
        elem.append(i["element"])
        star.append(i["stars"])
    for count in star:
        stars.append(count * '⭐')
    for (a, b) in zip(elem, stars):
        weakn += (a, b)
    new_weakn = [i.capitalize() for i in weakn]
    await boters.send_message(call.message.chat.id, ('\n'.join(new_weakn)))

@disp.callback_query_handler(text_contains='btn2')
async def resist(call):
    datas = get_data(call.message.text)
    res = datas[0]["resistances"]
    elem = []
    cross = []
    cross2 = []
    if (res ==[]):
        await boters.send_message(call.message.chat.id, ('Resistances:  N/A'))
    for i in res:
        elem.append(i["element"])
    for count in range(len(elem)):
        cross.append('❌')
    for (a, b) in zip(elem, cross):
            cross2 += (a, b)
    new_res = [b.capitalize() for b in cross2]
    await boters.send_message(call.message.chat.id,('\n'.join(new_res)))

@disp.callback_query_handler(text_contains='btn3')
async def resist(call):
    datas = get_data(call.message.text)
    location = datas[0]["locations"]
    loc = []
    for i in location:
        loc.append(i["name"])
    new_loc = [b.capitalize() for b in loc]
    await boters.send_message(call.message.chat.id, ('\n'.join(new_loc)))

if __name__ == '__main__':
    executor.start_polling(disp)
