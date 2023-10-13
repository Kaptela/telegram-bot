import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    DATABASE_HOST=os.getenv('DATABSE_HOST')
    DATABASE_NAME=os.getenv('DATABASE_NAME')
    DATABASE_USER=os.getenv('DATABASE_USER')
    DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')

    _connection = None

    @staticmethod
    def connect():
        '''Open the database connection if it's not already open'''
        if Database._connection is None:
            Database._connection = psycopg2.connect(
                host="127.0.0.1",
                database="telegram-bot",
                user="postgres",
                password="1245"
            )

    # DONE
    @staticmethod
    def getAllUsers(limit='', order=''):
        '''Возврашает всех пользователей с базы данных (Зареганных)
        Возвращает list и внутри dict

        Пример пользование:
        run: Database.getAllUsers()\n
        returns: [
                    {
                        'id': 1,\n
                        'name': 'Yedige',\n
                        'surname': 'Mazhit',\n 
                        'phone': '8 708 549 29 37',\n
                        'telegram': '@Yedige',\n
                        'group': 'A1'\n
                    },\n 
                    {\n
                        'id': 2,\n 
                        'name': 'Ansar',\n 
                        'surname': 'Zhexengali',\n 
                        'phone': '8 708 549 29 37',\n 
                        'telegram': '@Kaptela',\n
                        'group': 'A2'\n
                    }\n
                ]
        '''
        toreturn = []
        Database.connect()
        cursor = Database._connection.cursor()
        query = "SELECT u.id, u.name, u.surname, u.phone, u.telegram, g.group_name FROM users AS u JOIN speaking_club_group AS g ON u.group = g.id"  # Select only the columns you need
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            for row in results:
                final = {
                    "id" : row[0],
                    'name' : row[1],
                    'surname' : row[2],
                    'phone' : row[3],
                    'telegram' : row[4],
                    'group' : row[5]
                }
                toreturn.append(final)
        else:
            return "No rows found."

        cursor.close()
        return toreturn

    # DONE
    @staticmethod
    def getAvailableTimes(limit = '', order = ''):
        '''
        Возвращает все свободные слоты в расписании для записи

        Возвращает тоже list и внутри dict

        Пример пользование:\n
        run: Database.getAvailableTimes()\n
        returns:\n
                [\n
                    {\n
                        'grou_id': 1,\n 
                        'group': 'A1',\n 
                        'day_of_the_week': 'Monday',\n 
                        'time': '15:00',\n 
                        'duration': '2 hourse'\n
                    },\n
                    {\n
                        'grou_id': 2,\n 
                        'group': 'A2',\n 
                        'day_of_the_week': 'Sunday',\n 
                        'time': '15:00',\n 
                        'duration': '2 hourse'\n
                        }\n
                    ]\n
        '''
        toreturn = []
        Database.connect()
        cursor = Database._connection.cursor()
        query = 'SELECT g.id, g.group_name, s.day_of_the_week, TO_CHAR(s.time, \'HH24:MI\') AS formatted_time, g.duration FROM speaking_club_group AS g JOIN speaking_club_group__schedule AS gs ON g.id = gs."group" JOIN schedule AS s ON gs.schedule = s.id WHERE (SELECT COUNT(*) FROM "users" AS u WHERE u."group" = g.id) < g.group_capacity;'
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            for row in results:
                final = {
                    'grou_id' : row[0],
                    'group' : row[1],
                    'day_of_the_week' : row[2],
                    'time' : row[3],
                    'duration' : f'{row[4]} hourse'
                }
                toreturn.append(final)
        else:
            return "No rows found."

        cursor.close()
        return toreturn


    # DONE
    @staticmethod
    def registerUserToGroup(telegram: str, group_id: int, limit='', order=''):
        '''
        Регистрирует пользователя в базу данных группы,
        Возвращает просто dict

        Пример пользование:\n
        run: Database.registerUserToGroup()\n
        returns:\n
                {\n
                    "id": user_id,\n
                    'name': name,\n
                    'surname': surname,\n
                    'phone': phone,\n
                    'telegram': telegram,\n
                    'group': group_id,\n
                }
        '''
        Database.connect()
        cursor = Database._connection.cursor()
        query = f"update users set \"group\" = {group_id} where users.telegram = '{telegram}' returning *"

        cursor.execute(query)
        user_id_row = cursor.fetchone()

        if user_id_row is not None:
            user_id = user_id_row[0]
        else:
            user_id = None

        Database._connection.commit()
        cursor.close()

        entered_values = {
            "id": user_id,
            'telegram': telegram,
            'group': group_id,
        }

        return entered_values

    

    # DONE
    @staticmethod
    def registerUser(name:str, surname:str, phone:str, telegram:str):
        '''
        Регистрирует пользователя в базу данных,
        Возвращает просто dict

        Пример пользование:\n
        run: Database.registerUser(name:str, surname:str, phone:str, telegram:str)\n
        returns:\n
                {\n
                    "id": user_id,\n
                    'name': name,\n
                    'surname': surname,\n
                    'phone': phone,\n
                    'telegram': telegram,\n
                }
        '''
        Database.connect()
        cursor = Database._connection.cursor()
        query = f"INSERT INTO users (name, surname, phone, telegram) " \
                f"VALUES ('{name}', '{surname}', '{phone}', '{telegram}') RETURNING id;"

        cursor.execute(query)
        user_id = cursor.fetchone()[0]

        Database._connection.commit()

        cursor.close()
        

        entered_values = {
            "id": user_id,
            'name': name,
            'surname': surname,
            'phone': phone,
            'telegram': telegram,
        }

        return entered_values


    # DONE
    @staticmethod
    def is_authenticated(telegram:str):
        toreturn = []
        Database.connect()
        cursor = Database._connection.cursor()
        query = f'SELECT u.id, u.name, u.surname, u.phone, u.telegram, g.group_name FROM users AS u JOIN speaking_club_group AS g ON u.group = g.id WHERE telegram = \'{telegram}\''
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            for row in results:
                final = {
                    "id" : row[0],
                    'name' : row[1],
                    'surname' : row[2],
                    'phone' : row[3],
                    'telegram' : row[4],
                    'group' : row[5]
                }
                toreturn.append(final)
        else:
            return False

        cursor.close()
        
        return True
    
    @staticmethod
    def has_group(telegram:str):
        toreturn = None
        Database.connect()
        cursor = Database._connection.cursor()
        query = f'SELECT u.id, u.name, u.surname, u.phone, u.telegram, u."group" FROM users as u WHERE u.telegram = \'{telegram}\''
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            for row in results:
                final = {
                    "id" : row[0],
                    'name' : row[1],
                    'surname' : row[2],
                    'phone' : row[3],
                    'telegram' : row[4],
                    'group' : row[5]
                }
                toreturn = final
        else:
            # print(toreturn['group'])
            return False

        cursor.close()
        print(toreturn)
        if toreturn['group'] == None:
            return False

        return True

    # DONE
    @staticmethod
    def createGroup(group_name: str, group_capacity: int, duration: int, location: str):
        '''
        Создает новую спикинг группу и добавляет в бд,
        Возвращает просто dict

        Возвращает тоже list и внутри dict

        Пример пользование:\n
        run: Database.createGroup(group_name:str, group_capacity:str, duration:str, location:str)\n
        returns:\n
                {\n
                    "group_id" : group_id,\n
                    "group_name": group_name,\n
                    "group_capacity": group_capacity,\n
                    "duration": duration,\n
                    "location": location\n
                }
        '''
        Database.connect()
        cursor = Database._connection.cursor()
        query = f"INSERT INTO speaking_club_group (group_name, group_capacity, duration, location) " \
                f"VALUES ('{group_name}', {group_capacity}, {duration}, '{location}') RETURNING id;"

        cursor.execute(query)
        group_id = cursor.fetchone()[0]

        Database._connection.commit()

        cursor.close()
        

        # Create a dictionary with the entered values
        entered_values = {
            "group_id" : group_id,
            "group_name": group_name,
            "group_capacity": group_capacity,
            "duration": duration,
            "location": location
        }

        return entered_values



# print(Database.registerUser(input('Enter your name; '), input('Enter your surname: '), input('Enter your phone'), input('Enter your telegram: ')))
print(Database.has_group('@Kaptela'))