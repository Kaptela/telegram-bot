import telebot
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_KEY = os.getenv('TELEGRAM_BOT_KEY')

bot = telebot.TeleBot(TELEGRAM_BOT_KEY)