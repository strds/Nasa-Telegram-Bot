from config import API_TOKEN
from config import BOT_TOKEN
import requests
import telebot
import sqlite3


bot = telebot.TeleBot(BOT_TOKEN)

users = {}

DELETE_DATE_QUERY = '''
    DELETE FROM users_requests
    WHERE chat_id = (?)
'''
INSERT_DATE_QUERY = '''
    INSERT INTO users_requests (chat_id, date) VALUES(?, ?)
'''
SELECT_USERS_DATES_QUERY = '''
    SELECT date FROM users_requests
    WHERE chat_id = (?)
'''


@bot.message_handler(commands=["start"])
def greet_user(message):
    bot.send_message(message.chat.id, "Привет!")


@bot.message_handler(commands=["add_favorite"])
def add_favorite(message):
    bot.send_message(message.chat.id, "Какую дату вы хотите добавить в избранное?")
    bot.register_next_step_handler(message, proceed_date)


def proceed_date(message):
    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()

    res = cursor.execute(SELECT_USERS_DATES_QUERY, (message.chat.id,)).fetchone()
    if res:
        bot.send_message(message.chat.id, "У вас в избранном уже есть дата!")
        print(res)
    else:
        cursor.execute(INSERT_DATE_QUERY, (message.chat.id, message.text))
        conn.commit()

        bot.send_message(message.chat.id, "Я добавил эту дату в избранное!")
    # users[message.chat.id] = message.text


@bot.message_handler(commands=["delete_favorite"])
def delete_favorite(message):
    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()

    cursor.execute(DELETE_DATE_QUERY, (message.chat.id,)).fetchone()
    conn.commit()

    bot.send_message(message.chat.id, "Я удалил ваше избранное!")


@bot.message_handler(commands=["get_favorite"])
def get_favorite(message):
    conn = sqlite3.connect("requests.db")
    cursor = conn.cursor()

    res = cursor.execute(SELECT_USERS_DATES_QUERY, (message.chat.id,)).fetchone()
    if res:
        bot.send_message(message.chat.id, *res)
    else:
        bot.send_message(message.chat.id, "У вас нет избранных дат.")


@bot.message_handler(commands=["get_mars_photo"])
def get_mars_photo(message):
    sent = bot.send_message(message.chat.id,
                            "Введите номер сола, за который вы хотите получить фото с марсохода.")
    bot.register_next_step_handler(sent, get_sol)


def get_sol(message):
    sol = message.text

    try:
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/" \
              f"curiosity/photos?sol={sol}&camera=fhaz&api_key={API_TOKEN}"
        response = requests.get(url).json()
        bot.send_photo(message.chat.id, response["photos"][0]["img_src"])
    except:
        bot.reply_to(message, "Произошла ошибка при получении данных. Пожалуйста, попробуйте другой сол.")


@bot.message_handler(commands=["picture_of_the_day"])
def get_picture_of_the_day(message):
    sent = bot.send_message(message.chat.id,
                            "Введите дату в формате ГГГГ-ММ-ДД после 1995-6-16 и до нынешней даты,"
                            " чтобы получить фото за эту дату.")
    bot.register_next_step_handler(sent, get_earth_date)


def get_earth_date(message):
    date = message.text
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_TOKEN}&date={date}"
        response = requests.get(url).json()
        if response["media_type"] == "image":
            if len(response["explanation"]) > 4096:
                for x in range(0, len(response["explanation"]), 4096):
                    bot.send_photo(message.chat.id, response["hdurl"])
                    bot.send_message(message.chat.id, "Описание: " + '{}'.format(response[x:x + 4096]))
            else:
                bot.send_photo(message.chat.id, response["hdurl"])
                bot.send_message(message.chat.id, "Описание: " + '{}'.format(response["explanation"]))
        else:
            bot.send_message(message.chat.id, "К сожалению за эту дату нет фотографий :(")
    except:
        bot.reply_to(message, "Произошла ошибка при получении данных. Пожалуйста, попробуйте другую дату.")


bot.polling()
