import datetime
from app.database.sqls import Database
from bot import bot

def getQuestionSubject(message):
    if message.content_type != 'text': 
        bot.send_message(message.chat.id, '**Пожалуйста, введите текст!**', parse_mode='Markdown')
    else:
        question_subject = message.text
        msg = bot.send_message(message.chat.id, 'Напишите сам вопрос: ')
        bot.register_next_step_handler(msg, getQuestion, question_subject=question_subject)  # Pass question_subject as a parameter

def getQuestion(message, question_subject):
    if message.content_type != 'text': 
        bot.send_message(message.chat.id, '**Пожалуйста, введите текст!**', parse_mode='Markdown')
    else:
        question = message.text
        user = f"@{message.from_user.username}"
        date = datetime.datetime.now()
        result = Database.saveQuestionFromUser(user, question_subject=question_subject, question=question, date=date)
        if result:
            bot.send_message(message.chat.id, 'Мы получили ваше сообщение!\nВ скором времени с вами свяжется Аружан')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Попробуйте позже')