import sqlite3


class DataAccessObject:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.connection = sqlite3.connect('my_database.db')
        self.dao = self.connection.cursor()
        self.dao.execute('''
            CREATE TABLE IF NOT EXISTS OurDataBase (
            telegram_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            mode TEXT NOT NULL,
            age INTEGER,
            information TEXT NOT NULL
            )
        ''')

    def create_user(self, profile):
        self.dao.execute("INSERT INTO OurDataBase VALUES(?, ?, ?, ?, ?, ?)", (profile.get_telegram_id(), profile.get_name(), profile.get_gender(), profile.get_mode(), profile.get_age(), profile.get_information()))

    def edit_user(self, profile):
        #self.dao.execute("SELECT * FROM OurDataBase WHERE telegramid = ?", profile.telegram_id)
        self.dao.execute("UPDATE OurDataBase SET (name, gender, mode, age information) VALUES (?, ?, ?, ?, ?) WHERE telegram_id = ?", (profile.get_name(), profile.get_gender(), profile.get_mode(), profile.get_age(), profile.get_information(), profile.get_telegram_id()))

    def delete_user(self, profile):
        self.dao.execute(f"DELETE FROM OurDataBase WHERE telegram_id = {profile}")

    def commit_changes(self):
        self.connection.commit()        

    def close_database(self):
        self.connection.close()

    def show_base(self):
        result = self.dao.fetchall()
        for row in result:
            print(row)
