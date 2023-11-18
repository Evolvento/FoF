import sqlite3


class DataAccessObject:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite3')
        self.dao = self.connection.cursor()
        self.dao.execute('''
            CREATE TABLE IF NOT EXISTS OurDataBase (
            telegram_id INTEGER NOT NULL PRIMARY KEY,
            name TEXT,
            gender TEXT,
            age INTEGER,
            height INTEGER,
            mode TEXT,
            information TEXT,
            photo TEXT
            )
        ''')
        self.connection.commit()

    def create_user(self, telegram_id, name, gender, age, height, mode, information, photo):
        self.dao.execute(
            'INSERT or REPLACE INTO OurDataBase(telegram_id, name, gender, age, height, mode, information, photo) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
            (telegram_id, name, gender, age, height, mode, information, photo))
        self.connection.commit()

    def edit_user(self, profile):
        #self.dao.execute("SELECT * FROM OurDataBase WHERE telegramid = ?", profile.telegram_id)
        self.dao.execute("UPDATE OurDataBase SET (name, gender, mode, age, information) VALUES (?, ?, ?, ?, ?) WHERE telegram_id = ?", (profile.get_name(), profile.get_gender(), profile.get_mode(), profile.get_age(), profile.get_information(), profile.get_telegram_id()))

    def delete_user(self, profile):
        self.dao.execute(f"DELETE FROM OurDataBase WHERE telegram_id = {profile}")

    def commit_changes(self):
        self.connection.commit()

    def close_database(self):
        self.connection.close()

    def return_profiles(self, min_age, max_age, mode, gender, min_height, max_height):
        self.dao.execute('SELECT telegram_id FROM OurDataBase WHERE mode = ?', (mode,))
        if mode == '👊':
            self.dao.execute('SELECT telegram_id FROM OurDataBase WHERE gender = ?', (gender,))
        else:
            self.dao.execute('SELECT telegram_id FROM OurDataBase WHERE gender != ?', (gender,))
        self.dao.execute('SELECT telegram_id FROM OurDataBase WHERE age >= ? AND age <= ?', (min_age, max_age))
        self.dao.execute('SELECT telegram_id FROM OurDataBase WHERE height >= ? AND height <= ?', (min_height, max_height))
        return self.dao.fetchall()
    
    def show_base(self):
        self.dao.execute('SELECT * FROM OurDataBase')
        result = self.dao.fetchall()
        for row in result:
            print(row)

    def get_user(self, telegram_id):
        self.dao.execute('SELECT * FROM OurDataBase WHERE telegram_id = ?', (telegram_id,))
        return self.dao.fetchone()
