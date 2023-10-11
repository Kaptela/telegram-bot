import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('6697433375:AAGsMB4aQ7hpQ6SLJ7Xj4TEoaoYwP3c006U')

@bot.message_handler(commands=['start'])
def start(message):
    # conn = sqlite3.connect('studywitharuzhan.sql')
    # cur = conn.cursor()
    # conn.commit()
    # cur.close()
    # conn.close()
    # cur.execute('') # Создание таблицы
    mainMenu = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Книги на английском 📚')
    btn2 = types.KeyboardButton('Задать вопрос')
    btn3 = types.KeyboardButton('Проверка эссе 📝')
    btn4 = types.KeyboardButton('Запись на консультацию по курсу IELTS')
    btn5 = types.KeyboardButton('IELTS 6 week study plan 🌟')
    btn6 = types.KeyboardButton('Запись на speaking club SAYra')
    mainMenu.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, 'Привет', reply_markup=mainMenu)

@bot.message_handler(content_types=['text'])
def bookCategory(message):
    if message.text == 'Книги на английском 📚':
        bookCategory = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Книга 1')
        btn2 = types.KeyboardButton('Книга 2')
        bookCategory.row(btn1, btn2)
        btn3 = types.KeyboardButton('Книга 3')
        btn4 = types.KeyboardButton('Книга 4')
        bookCategory.row(btn3, btn4)
        btn5 = types.KeyboardButton('Книга 5')
        btn6 = types.KeyboardButton('Книга 6')
        bookCategory.row(btn5, btn6)
        back = types.KeyboardButton('Назад')
        bookCategory.row(back)
        bot.send_message(message.chat.id, 'Материал для практики', reply_markup=bookCategory)

    elif message.text == 'Книга 1':
        pass
    elif message.text == 'Книга 2':
        pass
    elif message.text == 'Книга 3':
        pass
    elif message.text == 'Книга 4':
        pass
    elif message.text == 'Книга 5':
        pass
    elif message.text == 'Назад':
        mainMenu = types.ReplyKeyboardMarkup(row_width=2)
        btn1 = types.KeyboardButton('Книги на английском 📚')
        btn2 = types.KeyboardButton('Задать вопрос')
        btn3 = types.KeyboardButton('Проверка эссе 📝')
        btn4 = types.KeyboardButton('Запись на консультацию по курсу IELTS')
        btn5 = types.KeyboardButton('IELTS 6 week study plan 🌟')
        btn6 = types.KeyboardButton('Запись на speaking club SAYra')
        mainMenu.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, 'Главная страница', reply_markup=mainMenu)

    # elif message.text == 'Задать вопрос':
    #     pass
    # elif message.text == 'Проверка эссе 📝':
    #     pass
    # elif message.text == 'Запись на консультацию по курсу IELTS':
    #     pass
    # elif message.text == 'IELTS 6 week study plan 🌟':
    #     pass
    # elif message.text == 'Запись на speaking club SAYra':
    #     pass

bot.polling(none_stop=True)

