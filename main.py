from config import API_TOKEN
from config import BOT_TOKEN
from datetime import date
import requests
import telebot


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def greet_user(message):
    bot.send_message(message.chat.id, "Привет!")


@bot.message_handler(commands=["picture"])
def send_picture(message):
    current_date = date.today()
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_TOKEN}&date={current_date}"
    picture = requests.get(url).json()

    bot.send_photo(message.chat.id, picture["hdurl"])


bot.polling()
