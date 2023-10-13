from app.database.sqls import Database

def is_authenticated(message):
    user = f"@{message.from_user.username}"
    Databaseuser = Database.is_authenticated(user)
    return Databaseuser

def has_group(username):
    return Database.has_group(username)