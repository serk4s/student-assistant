import telebot  #сам бот
from telebot import types  # для указание типов
import requests  #парсинг
import pandas as pd  #таблицы exel
import threading  #заметки
import datetime  #заметки и расписание
bot = telebot.TeleBot('6896125004:AAFmm3jzKFvLZCrZNLYduRmjurh87bQUxQ0')

sch = pd.read_excel("C:\cifrick_tg_bot\расписание.xlsx")

fit_sch_lst = []  #расписание для фит
for i in range(0, 7):
    day = str(sch.iat[i, 0])
    fit_sch_lst.append(day)

moa_sch_lst = []  #расписание для моа
for i in range(0, 7):
    day = sch.iat[i, 1]
    moa_sch_lst.append(day)

pmi_sch_lst = []  #расписание для пми
for i in range(0, 7):
    day = sch.iat[i, 2]
    pmi_sch_lst.append(day)

pi_sch_lst = []  #расписание для пи
for i in range(0, 7):
    day = sch.iat[i, 3]
    pi_sch_lst.append(day)

kb_sch_lst = []  #расписание для кб
for i in range(0, 7):
    day = sch.iat[i, 4]
    kb_sch_lst.append(day)


@bot.message_handler(commands=['start'])
def start_and_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Расписание")
    btn2 = types.KeyboardButton("Погода")
    btn3 = types.KeyboardButton("Заметки")
    markup.add(btn1 , btn2, btn3)
    bot.send_message(message.chat.id ,
                     text="Привет, {0.first_name}! Я бот цифрик! \nЯ буду твоим помощником в Telegram, просто выбери функцию, которой ты хочешь воспользоваться.".format(
                         message.from_user) , reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Погода"):
        url = 'https://api.openweathermap.org/data/2.5/weather?q=kemerovo&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

        weather_data = requests.get(url).json()
        print(weather_data)

        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])

        w_now = 'Сейчас в Кемерово ' + ' ' + str(temperature) + ' °C'
        w_feels = 'По ощущениям ' + str(temperature_feels) + ' °C'

        bot.send_message(message.from_user.id , w_now)
        bot.send_message(message.from_user.id , w_feels)

        wind_speed = round(weather_data['wind']['speed'])
        if wind_speed < 5:   #ветер слабый (от 5м\с), но бот должен понимать температуру для советов студенту
            if temperature_feels <= -25:
                bot.send_message(message.from_user.id ,
                                 'Ветра почти нет, но мороз стоит жуткий 🥶\nБудем надеятся, что отправят на дистант')
            elif -25 < temperature_feels <= -15:
                bot.send_message(message.from_user.id ,
                                 'Ветра почти нет, но холодно ☃\nТебе стоит одеться потеплее!')
            elif -15 < temperature_feels <= 0:
                bot.send_message(message.from_user.id ,
                                 'Ветра почти нет, но прохладно \nБудь я человеком, не вышел бы на улицу без шарфа... 🤧\n(это прямой намек)')
            elif 0 < temperature_feels <= 15:
                bot.send_message(message.from_user.id ,
                                 'Ветра почти нет и тепло 😎\nИдеальная погода, чтобы погулять или сходить на пары 😉')
            elif temperature_feels > 25:
                bot.send_message(message.from_user.id ,
                                 'Ветра почти нет и очень жарко 😰\nНе забывай пить побольше воды в такую жару!')

        elif wind_speed < 10:   #блок кода для ветра посильнее (5 -  10м\с)
            if temperature_feels <= -25:
                bot.send_message(message.from_user.id ,
                                 'На улице ветер и мороз стоит жуткий 🥶\nБудем надеятся, что отправят на дистант')
            elif -25 < temperature_feels <= -15:
                bot.send_message(message.from_user.id ,
                                 'На улице ветер и холодно ☃\nТебе стоит одеться потеплее!')
            elif -15 < temperature_feels <= 0:
                bot.send_message(message.from_user.id ,
                                 'На улице ветер и прохладно \nБудь я человеком, не вышел бы на улицу без шарфа... 🤧\n(это прямой намек)')
            elif 0 < temperature_feels <= 15:
                bot.send_message(message.from_user.id ,
                                 'На улице ветерок и тепло 😎\nИдеальная погода, чтобы погулять или сходить на пары 😉')
            elif temperature_feels > 25:
                bot.send_message(message.from_user.id ,
                                 'На улице очень жарко 😰, но дует ветерок\nЯ бы пошел гулять 😎')

        elif wind_speed < 20:  #ветер очень сильный (10 - 20м\с)
            if temperature_feels <= -25:
                bot.send_message(message.from_user.id ,
                                 'На улице сильный ветер и мороз стоит жуткий 🥶\nБудем надеятся, что отправят на дистант')
            elif -25 < temperature_feels <= -15:
                bot.send_message(message.from_user.id ,
                                 'На улице сильный ветер и холодно ☃\nТебе стоит одеться потеплее!')
            elif -15 < temperature_feels <= 0:
                bot.send_message(message.from_user.id ,
                                 'На улице сильный ветер и прохладно\nБудь я человеком, не вышел бы на улицу без шарфа... 🤧\n(это прямой намек)')
            elif 0 < temperature_feels <= 15:
                bot.send_message(message.from_user.id ,
                                 'На улице сильный ветер, но тепло 🤔\nНормальная погода на самом деле,\nна пары идти можно (и нужно😑)')
            elif temperature_feels > 25:
                bot.send_message(message.from_user.id ,
                                 'На улице может быть неслабый ветер, но так же очень жарко 😰\nЯ не знаю что сегодня надевать даже...')
        else:   #ветер больше 20м\с - шторм
            if temperature_feels <= -25:
                bot.send_message(message.from_user.id ,
                                 'На улице шторм и мороз стоит жуткий 🥶\nБудем надеятся, что отправят на дистант')
            elif -25 < temperature_feels <= -15:
                bot.send_message(message.from_user.id ,
                                 'На улице шторм и холодно ☃\nЛучше остаться дома')
            elif -15 < temperature_feels <= 0:
                bot.send_message(message.from_user.id ,
                                 'На улице шторм и прохладно 🤧\nДалеко не самая приятная погода...\nЛучше остаться дома')
            elif 0 < temperature_feels <= 15:
                bot.send_message(message.from_user.id ,
                                 'На тепло 😎, но штормит\nЛучше остаться дома')
            elif temperature_feels > 25:
                bot.send_message(message.from_user.id ,
                                 'На улице шторм, но так же очень жарко 😰\nЯ не могу понять что тебе советовать🙁')

    elif (message.text == "Расписание"):
        bot.send_message(message.chat.id , 'Напиши название своей группы')
        bot.register_next_step_handler(message, sch)


    elif (message.text == "Заметки"):
        bot.send_message(message.chat.id, 'Введи название заметки:')
        bot.register_next_step_handler(message, set_reminder_name)

def sch(message):
    today_date = datetime.datetime.now()
    if (message.text.lower() == "фит" or message.text.lower() == "фит 231" or message.text.lower() == "фит231" or message.text.lower() == "фит-231"):
        bot.send_message(message.chat.id, fit_sch_lst[today_date.weekday()])

    elif (message.text.lower() == "моа" or message.text.lower() == "моа 231" or message.text.lower() == "моа231" or message.text.lower() == "моа-231"):
        bot.send_message(message.chat.id, moa_sch_lst[today_date.weekday()])

    elif (message.text.lower() == "пми" or message.text.lower() == "пми 231" or message.text.lower() == "пми231" or message.text.lower() == "пми-231"):
        bot.send_message(message.chat.id, pmi_sch_lst[today_date.weekday()])

    elif (message.text.lower() == "пи" or message.text.lower() == "пи 231" or message.text.lower() == "пи231" or message.text.lower() == "пи-231"):
        bot.send_message(message.chat.id, pi_sch_lst[today_date.weekday()])

    elif (message.text.lower() == "кб" or message.text.lower() == "кб 231" or message.text.lower() == "кб231" or message.text.lower() == "кб-231"):
        bot.send_message(message.chat.id, kb_sch_lst[today_date.weekday()])

    else:
        bot.send_message(message.chat.id, 'Такой группы я не знаю( \nПопробуй ввести название группы в виде абриатуры без чисел и знаков')
        bot.register_next_step_handler(message , sch)


def set_reminder_name(message):
        user_data = {}
        user_data[message.chat.id] = {'reminder_name': message.text}
        bot.send_message(message.chat.id,
                         'Введи дату и время, когда ты хочешь получить напоминание в формате ГГГГ.ММ.ДД чч.мм')
        bot.register_next_step_handler(message, reminder_set, user_data)


def reminder_set(message, user_data):
        try:
            reminder_time = datetime.datetime.strptime(message.text, '%Y.%m.%d %H.%M')
            now = datetime.datetime.now()
            delta = reminder_time - now
            if delta.total_seconds() <= 0:
                bot.send_message(message.chat.id, 'Это прошедшая дата, попробуй еще раз.')
            else:
                reminder_name = user_data[message.chat.id]['reminder_name']
                bot.send_message(message.chat.id,
                                 'Напомню про\n"{}"\nПримерно в {}.'.format(reminder_name, reminder_time))
                reminder_timer = threading.Timer(delta.total_seconds(), send_reminder, [message.chat.id, reminder_name])
                reminder_timer.start()
        except ValueError:
            bot.send_message(message.chat.id, 'Неверный формат даты и времени, попробуй еще раз, пожалуйста')


def send_reminder(chat_id, reminder_name):
        bot.send_message(chat_id, 'Напоминаю:\n"{}"'.format(reminder_name))


bot.polling(none_stop=True)
