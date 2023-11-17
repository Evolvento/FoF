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
            telegram_id TEXT NOT NULL PRIMARY KEY,
            name TEXT,
            gender TEXT,
            age INTEGER,
            mode TEXT,
            information TEXT
            )
        ''')
        self.connection.commit()

    def create_user(self, telegram_id, name, gender, age, mode, information):
        self.dao.execute('INSERT or REPLACE INTO OurDataBase(telegram_id, name, gender, age, mode, information) VALUES(?, ?, ?, ?, ?, ?)', (telegram_id, name, gender, age, mode, information))
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

    def return_profiles(self, delta_age, mode, gender):
        self.dao.execute('SELECT telegram_id FROM OurDataBase GROUP BY mode HAVING mode = ?', (mode),)
        if mode == 'fight':
            self.dao.execute('SELECT telegram_id FROM OurDataBase GROUP BY gender HAVING gender IS ?', (gender),)
        else:
            self.dao.execute('SELECT telegram_id FROM OurDataBase GROUP BY gender HAVING gender IS NOT ?', (gender))
        self.dao.execute('SELECT telegram_id FROM OurDataBase GROUP BY age HAVING age >= ? AND age <= ?', (delta_age, delta_age))
        return self.dao.fetchall()
    def show_base(self):
        self.dao.execute('SELECT * FROM OurDataBase')
        result = self.dao.fetchall()
        for row in result:
            print(row)
