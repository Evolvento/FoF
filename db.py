import sqlite3
class DataAccessObject:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(cls):
        connection = sqlite3.connect('my_database.db')
        dao = connection.cursor()
        dao.execute('''
            CREATE TABLE IF NOT EXISTS OurDataBase (
            telegramid TEXT PRIMARY KEY
            fullname TEXT NOT NULL,
            gender TEXT NOT NULL,
            mode TEXT NOT NULL,
            age INTEGER
            height INTEGER
            weight INTEGER
            information TEXT NOT NULL
            )
        ''')

    def create_user(self, profile):
        self.dao.execute("INSERT INTO OurDataBase VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (profile.telegram_id, profile.fullname, profile.gender, profile.mode, profile.age, profile.height, profile.weight, profile.information))

    def edit_user(self, profile):
        #self.dao.execute("SELECT * FROM OurDataBase WHERE telegramid = ?", profile.telegram_id)

        self.dao.execute("UPDATE OurDataBase SET (fullname, gender, mode, age, height, weight, information) VALUES (?, ?, ?, ?, ?, ?, ?) WHERE telegramid = ?", (profile.fullname, profile.gender, profile.mode. profile.age, profile.height, profile.weight, profile.information, profile.telegram_id))
    def delete_user(self, profile):

        self.dao.execute(f"DELETE FROM OurDataBase WHERE telegramid = {profile}")
    def commit_changes(self):
        self.connection.commit()        

    def close_database(self):
        self.connection.close()
