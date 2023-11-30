import telebot  #сам бот
from telebot import types  # для указание типов
import requests  #парсинг
import pandas as pd  #таблицы exel
import threading  #заметки
import datetime  #заметки и расписание
bot = telebot.TeleBot('6840844685:AAG6vsQWmGVtpAVTnZFVyP8Y6op35FsxJ9k')

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
        if wind_speed < 5:
            bot.send_message(message.from_user.id , 'Ветра нет, хорошая погода, чтобы пойти на пары')
        elif wind_speed < 10:
            bot.send_message(message.from_user.id , 'На улице ветрено, оденьсья теплее чтобы пойти на пары')
        elif wind_speed < 20:
            bot.send_message(message.from_user.id , 'Ветер очень сильный, будьте осторожны, идя на пары')
        else:
            bot.send_message(message.from_user.id , 'На улице шторм, на улицу лучше не выходить, напиши старосте, что не пойдешь на пары')

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
