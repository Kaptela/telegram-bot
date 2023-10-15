from bot import bot
from app.database.sqls import Database

def getFirstName(message):
    if message.content_type != 'text': 
        bot.send_message(message.chat.id, '**Пожалуйста, введите текст!**', parse_mode='Markdown')
    else:
        name = message.text
        msg = bot.send_message(message.chat.id, 'Напишите вашу фамилию: ')
        bot.register_next_step_handler(msg, getLastName, name=name)

def getLastName(message, name):
    if message.content_type != 'text': 
        bot.send_message(message.chat.id, '**Пожалуйста, введите текст!**', parse_mode='Markdown')
    else:
        lastname = message.text
        msg = bot.send_message(message.chat.id, 'Напишите ваш номер телефона: ')
        bot.register_next_step_handler(msg, getPhoneNumber, name=name, lastname=lastname)

def getPhoneNumber(message, name, lastname):
    if message.content_type != 'text': 
        bot.send_message(message.chat.id, '**Пожалуйста, введите текст!**', parse_mode='Markdown')
    else:
        phone = message.text
        user = f"@{message.from_user.username}"
        result = Database.registerUser(name, lastname, phone, user)
        if result:
            bot.send_message(message.chat.id, '**Вы успешно зарегистрировались!**', parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, '**Ошибка, попробуйте позже**', parse_mode='Markdown')
