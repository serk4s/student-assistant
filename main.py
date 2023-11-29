import telebot
from telebot import types  # для указание типов
import requests
import config
import numpy as np  #импорт библиотек для работы с exlel файлов
import pandas as pd
import threading
import datetime
bot = telebot.TeleBot('6840844685:AAG6vsQWmGVtpAVTnZFVyP8Y6op35FsxJ9k')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Расписание")
    btn2 = types.KeyboardButton("Погода")
    btn3 = types.KeyboardButton("Заметки")
    markup.add(btn1 , btn2, btn3)
    bot.send_message(message.chat.id ,
                     text="Привет, {0.first_name}! Я тестовый бот цифрик".format(
                         message.from_user) , reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Погода"):
        url = 'https://api.openweathermap.org/data/2.5/weather?q=kemerovo&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

        weather_data = requests.get(url).json()
        print(weather_data)

        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])

        w_now = 'Сейчас в городе Кемерово ' + ' ' + str(temperature) + ' °C'
        w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'

        bot.send_message(message.from_user.id , w_now)
        bot.send_message(message.from_user.id , w_feels)

        wind_speed = round(weather_data['wind']['speed'])
        if wind_speed < 5:
            bot.send_message(message.from_user.id , '✅ Погода хорошая, ветра почти нет')
        elif wind_speed < 10:
            bot.send_message(message.from_user.id , '🤔 На улице ветрено, оденьтесь чуть теплее')
        elif wind_speed < 20:
            bot.send_message(message.from_user.id , '❗️ Ветер очень сильный, будьте осторожны, выходя из дома')
        else:
            bot.send_message(message.from_user.id , '❌ На улице шторм, на улицу лучше не выходить')

    elif (message.text == "Расписание"):
        bot.send_message(message.chat.id, "txt")

    elif (message.text == "Заметки"):
        bot.send_message(message.chat.id, 'Введите название заметки:')
        bot.register_next_step_handler(message, set_reminder_name)

def set_reminder_name(message):
        user_data = {}
        user_data[message.chat.id] = {'reminder_name': message.text}
        bot.send_message(message.chat.id,
                         'Введите дату и время, когда вы хотите получить напоминание в формате ГГГГ.ММ.ДД чч.мм')
        bot.register_next_step_handler(message, reminder_set, user_data)


def reminder_set(message, user_data):
        try:
            reminder_time = datetime.datetime.strptime(message.text, '%Y.%m.%d %H.%M')
            now = datetime.datetime.now()
            delta = reminder_time - now
            if delta.total_seconds() <= 0:
                bot.send_message(message.chat.id, 'Вы ввели прошедшую дату, попробуйте еще раз.')
            else:
                reminder_name = user_data[message.chat.id]['reminder_name']
                bot.send_message(message.chat.id,
                                 'Напоминание "{}" установлено на {}.'.format(reminder_name, reminder_time))
                reminder_timer = threading.Timer(delta.total_seconds(), send_reminder, [message.chat.id, reminder_name])
                reminder_timer.start()
        except ValueError:
            bot.send_message(message.chat.id, 'Вы ввели неверный формат даты и времени, попробуйте еще раз.')


def send_reminder(chat_id, reminder_name):
        bot.send_message(chat_id, 'Напоминание: "{}"'.format(reminder_name))



#if __name__ == '__main__':
bot.polling(none_stop=True)
