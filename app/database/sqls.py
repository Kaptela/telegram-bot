import psycopg2

class Database:
    _connection = psycopg2.connect(
        host="127.0.0.1",
        database="telegram-bot",
        user="postgres",
        password="1245"
    )

    # DONE
    @staticmethod
    def getAllUsers(limit='', order=''):
        toreturn = []
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
        Database._connection.close()
        print(toreturn)
        return toreturn

    # DONE
    @staticmethod
    def getAvailableTimes(limit = '', order = ''):
        toreturn = []
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
        Database._connection.close()
        print(toreturn)
        return toreturn

    @staticmethod
    def registerUserToGroup(name, surname, phone, telegram, group_id, limit='', order=''):
        cursor = Database._connection.cursor()
        query = f"INSERT INTO users (name, surname, phone, telegram, \"group\") " \
                f"VALUES ('{name}', '{surname}', '{phone}', '{telegram}', {group_id}) RETURNING id;"

        cursor.execute(query)
        user_id = cursor.fetchone()[0]

        Database._connection.commit()

        cursor.close()
        Database._connection.close()

        entered_values = {
            "id": user_id,
            'name': name,
            'surname': surname,
            'phone': phone,
            'telegram': telegram,
            'group': group_id,
        }

        return entered_values

    

    # DONE
    @staticmethod
    def registerUser(name, surname, phone, telegram):
        cursor = Database._connection.cursor()
        query = f"INSERT INTO users (name, surname, phone, telegram) " \
                f"VALUES ('{name}', '{surname}', '{phone}', '{telegram}') RETURNING id;"

        cursor.execute(query)
        user_id = cursor.fetchone()[0]

        Database._connection.commit()

        cursor.close()
        Database._connection.close()

        # Create a dictionary with the entered values
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
    def getCurrentUser(telegram:str):
        toreturn = []
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
            return "No user found."

        cursor.close()
        Database._connection.close()
        print(toreturn)
        return toreturn
    


    # DONE
    @staticmethod
    def createGroup(group_name: str, group_capacity: int, duration: int, location: str):
        cursor = Database._connection.cursor()
        query = f"INSERT INTO speaking_club_group (group_name, group_capacity, duration, location) " \
                f"VALUES ('{group_name}', {group_capacity}, {duration}, '{location}') RETURNING id;"

        cursor.execute(query)
        group_id = cursor.fetchone()[0]

        Database._connection.commit()

        cursor.close()
        Database._connection.close()

        # Create a dictionary with the entered values
        entered_values = {
            "group_id" : group_id,
            "group_name": group_name,
            "group_capacity": group_capacity,
            "duration": duration,
            "location": location
        }

        return entered_values



print(Database.registerUser(input('Enter your name; '), input('Enter your surname: '), input('Enter your phone'), input('Enter your telegram: ')))
