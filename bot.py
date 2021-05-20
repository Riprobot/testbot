import logging
from aiogram import Bot, Dispatcher, executor, types
from sqliter import SQLiter

logging.basicConfig(level=logging.INFO)
import random

TOKEN = '948170738:AAF4VCIqAJCmBP-tzVnx11zRWZARJTxv118'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = SQLiter(
    'postgres://rsvuryejidlyzs:f824cdd6ae8af1fe80f3982809631e202b9972a8d3ac2382fc14a0d4361a1967@ec2-54-216-17-9.eu-west-1.compute.amazonaws.com:5432/d804h1sknk085j')
players = {}
WantToPlay = []
IsATTAKING = []
IsGameOn = []
LeftDistance = []
PersonAlive = []
CamelAlive = []
CamelHealth = []
PersonHealth = []
DistanceToBandits = []
CntWater = []
CntMeat = []
CntAct = []
Win = []
b = []

@dp.message_handler(commands=['start'])
async def welcome(message):
    # keyboard
    global WantToPlay
    global LeftDistance
    global PersonAlive
    global CamelHealth
    global CamelAlive
    global PersonHealth
    global DistanceToBandits
    global CntWater
    global CntMeat
    global CntAct
    global WantToPlay
    global IsGameOn
    global Win
    global b
    if message.chat.id in players:
        id = players[message.chat.id]
        WantToPlay[id] = True
        IsGameOn[id] = False
        LeftDistance[id] = 0
        PersonAlive[id] = True
        CamelAlive[id] = True
        CamelHealth[id] = 100
        PersonHealth[id] = 100
        DistanceToBandits[id] = 100
        CntWater[id] = 3
        CntMeat[id] = 3
        CntAct[id] = 1
        Win[id] = False
        LeftDistance[id] = random.randint(1200, 1200)
        b[id] = []
    else:
        players[message.chat.id] = len(WantToPlay)
        WantToPlay.append(True)
        IsGameOn.append(False)
        PersonAlive.append(True)
        IsATTAKING.append(-1)
        CamelAlive.append(True)
        PersonHealth.append(100)
        CamelHealth.append(100)
        DistanceToBandits.append(100)
        CntWater.append(3)
        CntMeat.append(3)
        CntAct.append(1)
        Win.append(False)
        LeftDistance.append(random.randint(1200, 1200))
        b.append([])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("ДА")
    item2 = types.KeyboardButton("НЕТ")
    markup.add(item1, item2)
    await bot.send_message(chat_id=message.chat.id, text=
    "Привет {0.first_name}!\nХочешь поиграть в прикольную игру?".format(message.from_user),
                           parse_mode='html', reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def actions(message):
    if message.chat.id not in players:
        await bot.send_message(chat_id=message.chat.id,
                               text="Нажми на '/start' чтобы начать игру")
        return
    ind = players[message.chat.id]
    global WantToPlay
    global IsATTAKING
    global IsGameOn
    if IsATTAKING[ind] != -1 and message.text == '🍡': IsATTAKING[ind] = -1
    if IsATTAKING[ind] != -1:
        await ATTACK(ind)
        return
    if IsGameOn[ind]:
        await gameactions(message)
        return

    if message.chat.type == 'private':
        if message.text == 'ДА':
            WantToPlay[ind] = True
            IsGameOn[ind] = True
            await bot.send_message(chat_id=message.chat.id, text="Описание игры:\n")
            await bot.send_message(chat_id=message.chat.id,
                                   text="Ты застрял в пустыне, и теперь тебе нужно добраться до оазиса, но не все так просто, за тобой гонятся головорезы,они желают поскорее догнать тебя и убить, поэтому тебе нужно поторопится\n И да тебе повезло, ведь у тебя есть верблюд")
            await gameactions(message)
            return

        if message.text == 'НЕТ':
            if WantToPlay[ind] == True:
                await bot.send_message(chat_id=message.chat.id, text="НЕ ХОЧЕШЬ ИГРАТЬ В МОЮ ИГРУ!?😡😡😡😡😡\n")
                await bot.send_message(chat_id=message.chat.id, text="Даю последний шанс передумать\n")
                await bot.send_message(chat_id=message.chat.id, text="Хочешь играть в мою игру????????")
                WantToPlay[ind] = False
            else:
                IsATTAKING[ind] = message.chat.id
                await ATTACK(ind)

            return
        await bot.send_message(chat_id=message.chat.id, text="Выбери что-то из меню")


def add_db(user_id, points):
    if (not db.player_exists(user_id)):
        db.add_player(user_id, points)
    else:
        if (db.get_points(user_id) > points):
            db.update_points(user_id, points)


async def ATTACK(ind):
    global IsATTAKING
    if IsATTAKING[ind] != -1:
        await bot.send_message(chat_id=IsATTAKING[ind], text="Ты в бане, иди в баню ")


async def gameactions(message):
    ind = players[message.chat.id]
    global LeftDistance
    global PersonAlive
    global CamelHealth
    global CamelAlive
    global PersonHealth
    global DistanceToBandits
    global CntWater
    global CntMeat
    global CntAct
    global Win
    global b
    CntAct[ind] += 1
    HasAction = True

    if Win[ind]:
        await bot.send_message(chat_id=message.chat.id, text="Вы победили, хотите поиграть еще нажмите на '/start'")
        return
    if PersonAlive[ind]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        f = LeftDistance[ind]
        if message.text == 'Ехать быстро на верблюде' and CamelAlive[ind] == True:
            CamelHealth[ind] -= random.randint(20, 30)
            PersonHealth[ind] -= random.randint(15, 20)
            LeftDistance[ind] -= random.randint(50, 70)
        elif message.text == 'Ехать спокойно на вердблюде' and CamelAlive[ind] == True:
            CamelHealth[ind] += random.randint(0, 5)
            PersonHealth[ind] -= random.randint(10, 15)
            LeftDistance[ind] -= random.randint(30, 40)
        elif message.text == 'Идти пешком':
            CamelHealth[ind] += random.randint(5, 15)
            PersonHealth[ind] -= random.randint(5, 7)
            LeftDistance[ind] -= random.randint(25, 35)
        elif message.text == 'Выпить воды' and CntWater[ind] > 0:
            CamelHealth[ind] += random.randint(50, 60)
            PersonHealth[ind] += random.randint(50, 70)
            CntWater[ind] -= 1
        elif message.text == 'Съесть мясо' and CamelAlive[ind] == False and CntMeat[ind] > 0:
            PersonHealth[ind] = 100
            CntMeat[ind] -= 1
        elif message.text == 'Отдыхать':
            CamelHealth[ind] += random.randint(40, 50)
            PersonHealth[ind] += random.randint(20, 30)
        elif message.text == 'Бежать' and CamelAlive[ind] == False:
            PersonHealth[ind] -= random.randint(20, 30)
            LeftDistance[ind] -= random.randint(40, 45)
        elif message.text == "Описание":
            st = "Итак в этой игре у вас и вашего верблюда по 100 единиц здорвья при израсходовании которых вы или ваш верблюд умирают\n<b>Описываю все доступные вам команды:</b>\n"
            if b[ind].count("Ехать быстро на верблюде") == 1:
                st += '\n'
                st += '<b>Ехать быстро на верблюде</b>\n'
                st += "1)Количество здоровья ВЕРБЛЮДА <b>уменьшается</b> на 20 - 30\n"
                st += "2)Количество здоровья ПЕРСОНАЖА <b>уменьшается</b> на 15 - 20\n"
                st += "3)Преодолевает дистаницию 50 - 70\n"
            if b[ind].count('Ехать спокойно на вердблюде') == 1:
                st += '\n'
                st += '<b>Ехать спокойно на вердблюде</b>\n'
                st += "1)Количество здоровья ВЕРБЛЮДА <b>увеличивается</b> на 0 - 5\n"
                st += "2)Количество здоровья ПЕРСОНАЖА <b>уменьшается</b> на 10 - 15\n"
                st += "3)Преодолевает дистаницию 30 - 40\n"
            if b[ind].count('Идти пешком') == 1:
                st += '\n'
                st += '<b>Идти пешком</b>\n'
                st += "1)Количество здоровья ВЕРБЛЮДА <b>увеличивается</b> на 5 - 15\n"
                st += "2)Количество здоровья ПЕРСОНАЖА <b>уменьшается</b> на 5 - 7\n"
                st += "3)Преодолевает дистаницию 25 - 35\n"
            if b[ind].count('Выпить воды') == 1:
                st += '\n'
                st += '<b>Выпить воды</b>\n'
                st += "1)Количество здоровья ВЕРБЛЮДА <b>увеличивается</b> на 50 - 60\n"
                st += "2)Количество здоровья ПЕРСОНАЖА <b>увеличивается</b> на 50 - 70\n"
            if b[ind].count('Съесть мясо') == 1:
                st += '\n'
                st += '<b>Съесть мясо</b>\n'
                st += "1)Количество здоровья ПЕРСОНАЖА <b>увеличивается</b> до 100\n"
            if b[ind].count('Отдыхать') == 1:
                st += '\n'
                st += '<b>Отдыхать</b>\n'
                st += "1)Количество здоровья ВЕРБЛЮДА <b>увеличивается</b> на 40 - 50\n"
                st += "2)Количество здоровья ПЕРСОНАЖА <b>увеличивается</b> на 20 - 30\n"
            if b[ind].count('Бежать') == 1:
                st += '\n'
                st += '<b>Бежать</b>\n'
                st += "1)Количество здоровья ПЕРСОНАЖА <b>уменьшается</b> на 20 - 30\n"
                st += "2)Преодолевает дистаницию 40 - 45\n"
            st += '\n'
            st += '\n'
            st += "<b>Система предупреждений:</b>\n"
            st += "Для верблюда и персонажа срабатывает предупреждение когда их здоровье меньше 30"
            await bot.send_message(chat_id=message.chat.id, text=st, parse_mode='html')
            HasAction = False
        else:
            await bot.send_message(chat_id=message.chat.id, text="Выбери что-то из меню")
            HasAction = False
        a = ""
        PersonHealth[ind] = min(100, PersonHealth[ind])
        CamelHealth[ind] = min(100, CamelHealth[ind])
        if CamelHealth[ind] <= 0 and CamelAlive[ind] == True:
            CamelAlive[ind] = False
            a += "😥К моему сожалению ваш верблюд умер и но зато у вас появился новый ресурс МЯСО\n"
        if PersonHealth[ind] <= 0 and PersonAlive[ind] == True:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item1 = types.KeyboardButton("/start")
            markup.add(item1)
            PersonAlive[ind] = False
            await bot.send_message(chat_id=message.chat.id,
                                   text="К моему сожалению вы умерли от усталости, начните игру занаво оправив '/start'",
                                   reply_markup=markup)
            return
        if (LeftDistance[ind] <= 0 and PersonAlive[ind] == True):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item1 = types.KeyboardButton("😉Хорошо")

            markup.add(item1)
            await bot.send_message(chat_id=message.chat.id,
                                   text="Поздравляем вы победили и дорабрались до оазиза за " + str(
                                       CntAct[
                                           ind] - 1) + " дней" + "\nЕсли вам понравилась моя игра то можете поделится ей со своими друзьями\n",
                                   reply_markup=markup)
            Win[ind] = True
            N = "{0.username}".format(message.from_user)
            lastVal = db.get_points(N)
            newVal = min(lastVal, CntAct[ind] - 1)
            if lastVal > newVal:
                await bot.send_message(chat_id=message.chat.id, text="Неплохо ты побил свой прошлый рекорд " + str(
                    lastVal) + "\nТеперь твой рекорд " + newVal + "\n")
            add_db(N, newVal)
            db.commit()
            newList = db.get_players()
            st = "Топ 3 игроков:\n"
            sz = len(newList)
            id = 0
            while sz != id and (id) < 3:
                st += "<b>" + str(newList[id][0]) + "</b>" + " прошел игру за " + str(newList[id][1]) + " дней" + "\n"
                id += 1
            await bot.send_message(chat_id=message.chat.id, text=st + "\n", parse_mode='html')
            return
        DistanceToBandits[ind] += f - LeftDistance[ind]
        if HasAction == True:
            DistanceToBandits[ind] -= random.randint(40, 50)
        if DistanceToBandits[ind] <= 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item1 = types.KeyboardButton("/start")
            markup.add(item1)
            PersonAlive[ind] = False
            await bot.send_message(chat_id=message.chat.id,
                                   text="К моему сожалению на вас напали бандиты, начните игру занаво нажав на '/start'",
                                   reply_markup=markup)
            return

        if CamelHealth[ind] <= 30 and CamelAlive[ind] == True:
            a += "🐪 <b>Ваш верблюд устает ему следует ОТДОХНУТЬ</b> 🐪\n".format()
        if PersonHealth[ind] <= 30:
            a += "🚶 <b>Вы устаете вам следует ОТДОХНУТЬ</b> 🚶\n".format()
        b[ind].clear()
        item1 = types.KeyboardButton("Ехать быстро на верблюде")
        item2 = types.KeyboardButton("Ехать спокойно на вердблюде")
        item6 = types.KeyboardButton("Отдыхать")
        item7 = types.KeyboardButton("Бежать")
        item3 = types.KeyboardButton("Идти пешком")
        item4 = types.KeyboardButton("Выпить воды")
        item5 = types.KeyboardButton("Съесть мясо")
        markup.add(item3, item6)
        b[ind].append(item3.text)
        b[ind].append(item6.text)
        if HasAction == False: CntAct[ind] -= 1
        a += "☀День " + str(CntAct[ind]) + "\n"
        a += "💧ВОДА " + str(CntWater[ind]) + " шт" + "\n"
        if CamelAlive[ind] == False:
            a += "🥩МЯСО " + str(CntMeat[ind]) + " шт" + "\n"
        if CamelAlive[ind] == True:
            markup.add(item1)
            b[ind].append(item1.text)
            markup.add(item2)
            b[ind].append(item2.text)
        else:
            markup.add(item5, item7)
            if (CntMeat[ind] > 0):
                b[ind].append(item5.text)
            b[ind].append(item7.text)
        if CntWater[ind] > 0:
            markup.add(item4)
            b[ind].append(item4.text)
        item8 = types.KeyboardButton("Описание")
        markup.add(item8)
        a += "👳🏻‍♂️Бандитам до вас осталось " + str(DistanceToBandits[ind]) + "км\n"
        a += "⛲️До оазиса осталось " + str(LeftDistance[ind]) + "км"
        await bot.send_message(chat_id=message.chat.id, text=a, reply_markup=markup, parse_mode='html')
    else:
        await bot.send_message(chat_id=message.chat.id, text="Вы умерли, начните игру заново нажав на '/start'")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
