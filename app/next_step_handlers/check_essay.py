from app.functions.text_detection import detect_text
from bot import bot
import os
from PIL import Image
from dotenv import load_dotenv
import openai

load_dotenv()
# SETTINGS
OPENAI_KEY = os.getenv('OPENAI_KEY')

openai.api_key = OPENAI_KEY



messages = []
system_msg = 'Imagine that you are a writing ielts examiner'
messages.append({"role": "system", "content": system_msg})

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

