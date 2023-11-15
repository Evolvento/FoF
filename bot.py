import telebot
import sqlite3
from telebot import types
from abc import ABC, abstractmethod

bot = telebot.TeleBot('token')

if True:
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        create_account = types.KeyboardButton('Создать профиль')
        markup.add(create_account)
        bot.send_message(message.chat.id, 'Я бот FoF. Здесь вы можете найти с кем подраться или потрахаться', reply_markup=markup)
        id = message.from_user.id
        bot.register_next_step_handler(message, name)


    def name(message):
        bot.send_message(message.chat.id, 'Напиши имя')
        bot.register_next_step_handler(message, age)


    def age(message):
        bot.send_message(message.chat.id, 'Сколько тебе лет?')
        bot.register_next_step_handler(message)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    pass


class Menu:
    def __init__(self):
        self.profile = None

    def create_profile(self):
        self.profile = Profile()

    def partner_search(self):
        controller = Controller()
        if self.profile.get_mode() == 'love':
            controller.set_strategy(StrategyLove())
        if self.profile.get_mode() == 'fight':
            controller.set_strategy(StrategyFight())
        return controller.execute(self.profile)

    def display_profile(self, profile):
        pass


class Profile:
    def __init__(self):
        self.__name = None
        self.__age = None
        self.__gender = None
        self.__mode = None
        self.__active = False

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        self.__age = age

    def set_gender(self, gender):
        self.__gender = gender

    def set_mode(self, mode):
        self.__mode = mode

    def change_active(self):
        self.__active = not self.__active

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def get_gender(self):
        return self.__age

    def get_mode(self):
        return self.__mode

    def get_active(self):
        return self.__active


class IStrategy(ABC):
    @abstractmethod
    def search(self, profile):
        pass


class StrategyLove(IStrategy):
    def search(self, profile):
        pass


class StrategyFight(IStrategy):
    def search(self, profile):
        pass


class Controller:
    def __init__(self):
        self.strategy = None

    def set_strategy(self, strategy: IStrategy):
        self.strategy = strategy

    def execute(self, profile):
        return self.strategy.search(profile)


connection = sqlite3.connect('my_database.db')
dao = connection.cursor()
dao.execute('''
CREATE TABLE IF NOT EXISTS OurDataBase (
id INTEGER PRIMARY KEY,
fullname TEXT NOT NULL,
telegramid TEXT NOT NULL,
age INTEGER
height INTEGER
weight INTEGER
information TEXT NOT NULL
)
''')
#dao.execute('CREATE INDEX telid ON OurDataBase (telegramid)')
dao.execute('INSERT or IGNORE INTO OurDataBase (id, fullname, telegramid, age) VALUES (?, ?, ?, ?)', (0, 'sharik', '5', 5))
dao.execute('INSERT or IGNORE INTO OurDataBase (id, fullname, telegramid, age) VALUES (?, ?, ?, ?)', (1, 'butilka', '4', 4))
dao.execute('UPDATE OurDataBase SET telegramid = ? WHERE fullname = ?', ('0', 'jopa'))
dao.execute('SELECT * FROM OurDataBase')
users = dao.fetchall()
for user in users:
    print(user)
connection.commit()
connection.close()


bot.polling(none_stop=True, interval=0)
