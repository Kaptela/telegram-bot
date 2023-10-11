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
        btn1 = types.KeyboardButton('Alwyn Cox - Dangerous Journey')
        btn2 = types.KeyboardButton('Arthur Conan Doyle - Sherlock Holmes and the Sport of Kings')
        bookCategory.row(btn1, btn2)
        btn3 = types.KeyboardButton('Atomic Habits James Clear')
        btn4 = types.KeyboardButton("Breakfast At Tiffany's")
        bookCategory.row(btn3, btn4)
        btn5 = types.KeyboardButton('Harry Potter and the Sorcerers Stone')
        btn6 = types.KeyboardButton('The Fault in Our Stars')
        bookCategory.row(btn5, btn6)
        back = types.KeyboardButton('Назад')
        bookCategory.row(back)
        bot.send_message(message.chat.id, 'Материал для практики', reply_markup=bookCategory)

    elif message.text == 'Alwyn Cox - Dangerous Journey':
        bot.send_document(message.chat.id, open('books/Alwyn Cox - Dangerous Journey.pdf', 'rb'))

    elif message.text == 'Arthur Conan Doyle - Sherlock Holmes and the Sport of Kings':
        bot.send_document(message.chat.id, open('books/Arthur Conan Doyle - Sherlock Holmes and the Sport of Kings.pdf', 'rb'))
    elif message.text == 'Atomic Habits James Clear':
        bot.send_document(message.chat.id, open('books/Atomic Habits James Clear.pdf', 'rb'))
    elif message.text == "Breakfast At Tiffany's":
        bot.send_document(message.chat.id, open("books/Breakfast At Tiffany's.pdf", 'rb'))
    elif message.text == 'Harry Potter and the Sorcerer\'s Stone':
        bot.send_document(message.chat.id, open('books/Harry Potter and the Sorcerer\'s Stone.pdf', 'rb'))
    elif message.text == 'The Fault in Our Stars':
        bot.send_document(message.chat.id, open('books/The Fault in Our Stars.pdf', 'rb'))

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

