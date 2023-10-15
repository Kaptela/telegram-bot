from telebot import types
from dotenv import load_dotenv
from app.functions.admin import is_admin
from app.functions.user import is_authenticated
from app.database.sqls import Database
from app.next_step_handlers.registerUserToSpeakingClub import registerUserToSpeakingClub
from app.next_step_handlers.check_essay import check_essay
from app.next_step_handlers.askQuestionAboutIelts import getQuestionSubject, getQuestion
from app.next_step_handlers.RegisterUser import getFirstName
from bot import bot
import datetime

load_dotenv()

@bot.message_handler(commands=['start'])
def start(message):
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
        btn2 = types.KeyboardButton('Проверить вопросы по курсу IELTS')
        logout = types.KeyboardButton('Выйти с панели администратора')
        mainMenu.add(btn1, btn2, logout)
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
        options = types.ReplyKeyboardMarkup(row_width=2)
        back = types.KeyboardButton('Назад')
        options.row(back)
        msq = bot.send_message(message.chat.id, 
            '*Провила задавания вопроса*:\n'
            '_Вопрос не должен отходить от темы_\n'
            '\n',
            parse_mode='Markdown'
        )
        msg = bot.send_message(message.chat.id, 'Напишите тему вопроса: ')
        bot.register_next_step_handler(msg, getQuestionSubject)  # No need to store it in a variable
        user = f"@{message.from_user.username}"
        date = datetime.datetime.now()
    elif message.text == 'IELTS 6 week study plan 🌟':
        bot.send_document(message.chat.id, open('6 week study plan.pdf', 'rb'))
    elif message.text == 'Запись на speaking club SAYra':
        if not is_authenticated(message):
            msg = bot.send_message(message.chat.id, '*Пожалуйста зарегистрируйтесь!*', parse_mode='Markdown')
            msg = bot.send_message(message.chat.id, 'Напишите ваше имя: ')
            bot.register_next_step_handler(msg, getFirstName)
            return
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
        listOfUsers = Database.getAllUsersRegisteredSpeakingClub()
        if listOfUsers:
            botsendmessage = '*Список людей зарегистрированных на спикинг клаб:*\n'
            for i in listOfUsers:
                ms =    f"{i['telegram']}\n"\
                        f"Day: {i['day of the week']}\n"\
                        f"Time: {i['time']}\n\n"
                botsendmessage += ms
            bot.send_message(message.chat.id, botsendmessage, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, 'No users', parse_mode='Markdown')
    elif message.text == 'Проверить вопросы по курсу IELTS':
        if not is_admin(message):
            bot.send_message(message.chat.id, "You don't have permission to run this command")
            return
        listOfQuestions = Database.getAllQuestionsAboutIelts()
        if listOfQuestions:
            botsendmessage = '*Список вопросов по курсу IELTS:*\n'
            for i in listOfQuestions:
                ms =    f"{i['user']}\n"\
                        f"Subject: {i['question_subject']}\n"\
                        f"Question: {i['question']}\n"\
                        f"Date: {i['date']}\n\n"
                botsendmessage += ms
            bot.send_message(message.chat.id, botsendmessage, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, 'No questions', parse_mode='Markdown')

bot.polling(none_stop=True)

