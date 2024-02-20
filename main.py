from config import API_TOKEN
from config import BOT_TOKEN
import requests
import telebot


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def greet_user(message):
    bot.send_message(message.chat.id, "Привет!")


@bot.message_handler(commands=["mars_photo"])
def get_mars_photo(message):
    sent = bot.send_message(message.chat.id,
                            "Введите номер сола, за который вы хотите получить фото с марсохода.")
    bot.register_next_step_handler(sent, sol_getter)


def sol_getter(message):
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
    bot.register_next_step_handler(sent, date_getter)


def date_getter(message):
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
