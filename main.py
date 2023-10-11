import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('6697433375:AAGsMB4aQ7hpQ6SLJ7Xj4TEoaoYwP3c006U')

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('studywitharuzhan.sql')
    cur = conn.cursor()
    conn.commit()
    cur.close()
    conn.close()
    # cur.execute('') # Создание таблицы
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Книги на английском 📚')
    btn2 = types.KeyboardButton('Задать вопрос')
    btn3 = types.KeyboardButton('Проверка эссе 📝')
    btn4 = types.KeyboardButton('Запись на консультацию по курсу IELTS')
    btn5 = types.KeyboardButton('IELTS 6 week study plan 🌟')
    btn6 = types.KeyboardButton('Запись на speaking club SAYra')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    # bot.register_next_step_handler(message, on_click)

# def on_click(message):



bot.polling(none_stop=True)

