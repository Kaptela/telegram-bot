from app.database.sqls import Database
from app.functions.user import has_group
from bot import bot

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