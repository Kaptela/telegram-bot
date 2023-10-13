import telebot
import os
import openai
import sqlite3
from telebot import types
from PIL import Image
from dotenv import load_dotenv
from app.functions.text_detection import detect_text
from app.functions.admin import is_admin
from app.functions.user import is_authenticated, has_group
from app.database.sqls import Database 
load_dotenv()

# SETTINGS
OPENAI_KEY = os.getenv('OPENAI_KEY')
TELEGRAM_BOT_KEY = os.getenv('TELEGRAM_BOT_KEY')
openai.api_key = OPENAI_KEY
bot = telebot.TeleBot(TELEGRAM_BOT_KEY)


messages = []
system_msg = 'Imagine that you are a writing ielts examiner'
messages.append({"role": "system", "content": system_msg})


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

@bot.message_handler(commands=['admin'])
def adminCommands(message):
    if is_admin(message):
        mainMenu = types.ReplyKeyboardMarkup(row_width=2)
        btn1 = types.KeyboardButton('Проверить запись на спикинг клаб')
        btn2 = types.KeyboardButton('Выйти с панели администратора')
        mainMenu.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы вошли на панель администратора', reply_markup=mainMenu)
    else:
        bot.send_message(message.chat.id, "You don't have permission to run this command")

    
@bot.message_handler(content_types=['text'])
def user(message):
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
    elif message.text == 'Задать вопрос':
        markup = types.InlineKeyboardMarkup()
        redirectButton = types.InlineKeyboardButton('Перейти', url='https://t.me/theycallmearuka')
        markup.add(redirectButton)
        with open('img/admin.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=markup)
    elif message.text == 'Проверка эссе 📝':
        msg = bot.send_message(message.chat.id, "Пожалуйста, отправьте текст вашего эссе или его фотографию.")
        bot.register_next_step_handler(msg, check_essay)
    elif message.text == 'Запись на консультацию по курсу IELTS':
        pass
    elif message.text == 'IELTS 6 week study plan 🌟':
        bot.send_document(message.chat.id, open('6 week study plan.pdf', 'rb'))
    elif message.text == 'Запись на speaking club SAYra':
        options = types.ReplyKeyboardMarkup(row_width=2)
        btns = {}

        CoursesFromDb = Database.getAvailableTimes()
        if not CoursesFromDb:
            bot.send_message(message.chat.id, 'Доступных дат пока что нету!\nЗагляните позже')
            return
        for course in CoursesFromDb:
            btnText = f'{course["grou_id"]} - {course["day_of_the_week"]}, {course["time"]}, {course["duration"]}'
            btn = types.KeyboardButton(btnText)
            btns[btnText] = course
            options.row(btn)
        back = types.KeyboardButton('Назад')
        options.row(back)
        msg = bot.send_message(message.chat.id, 'Выберите удобное для вас время', reply_markup=options)
        bot.register_next_step_handler(msg, registerUserToSpeakingClub, kwargs=btns)
    elif message.text == 'Выйти с панели администратора':
        if not is_admin(message):
            bot.send_message(message.chat.id, "You don't have permission to run this command")
            return
        mainMenu = types.ReplyKeyboardMarkup(row_width=2)
        btn1 = types.KeyboardButton('Книги на английском 📚')
        btn2 = types.KeyboardButton('Задать вопрос')
        btn3 = types.KeyboardButton('Проверка эссе 📝')
        btn4 = types.KeyboardButton('Запись на консультацию по курсу IELTS')
        btn5 = types.KeyboardButton('IELTS 6 week study plan 🌟')
        btn6 = types.KeyboardButton('Запись на speaking club SAYra')
        mainMenu.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, 'Главная страница', reply_markup=mainMenu)
    elif message.text == 'Проверить запись на спикинг клаб':
        if not is_admin(message):
            bot.send_message(message.chat.id, "You don't have permission to run this command")
            return
        bot.send_message(message.chat.id, 'В разработке')

def registerUserToSpeakingClub(message, **kwargs:dict):
    usersTelegram = f'@{message.from_user.username}'
    if has_group(usersTelegram):
       bot.send_message(message.chat.id, 'You are already registered to speaking club') 
       return
    text = message.text
    course = kwargs['kwargs'][text]
    Database.registerUserToGroup(telegram=usersTelegram, group_id=course['grou_id'])
    bot.send_message(message.chat.id, f'Вы успешно зарегистрировались на спикинг клаб\nС нетерпением ждем вас в {course["time"]}')
    return


def check_essay(message):
    if message.content_type == 'text':
        text = message.text
        analyzing_message = bot.send_message(message.chat.id, 'Analyzing essay...')
        user_messages = [{"role": "user", "content": text + "\n You should highlight the candidate's shortcomings and strong qualities, "
                                                           "make suggestions for improvement, and provide an honest IELTS Writing score."}]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=user_messages
        )
        reply = response["choices"][0]["message"]["content"]
        bot.edit_message_text(chat_id=message.chat.id, message_id=analyzing_message.message_id, text=reply)
    elif message.content_type == 'photo':
        analyzing_message = bot.send_message(message.chat.id, 'Analyzing essay...')
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = bot.download_file(file_info.file_path)

        with open('temp_essay.jpg', 'wb') as f:
            f.write(file)

        detected_text = detect_text('temp_essay.jpg')
        
        print(detected_text)

        os.remove('temp_essay.jpg')

        messages.append({"role": "user", "content": detected_text + "\n You should highlight the candidate's shortcomings and strong qualities, "
                                                        "make suggestions for improvement, and provide an honest IELTS Writing score."})
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages)
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})

        bot.edit_message_text(chat_id=message.chat.id, message_id=analyzing_message.message_id, text=reply)





bot.polling(none_stop=True)

