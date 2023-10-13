from dotenv import load_dotenv
import os

load_dotenv()


def is_admin(message):
    admin = os.getenv('ADMIN')
    username = f"@{message.from_user.username}" if message.from_user.username else None
    return username == admin

