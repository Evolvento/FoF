import telebot
import sqlite3
from db import DataAccessObject
from telebot import types
from abc import ABC, abstractmethod


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
        self.__telegram_id = None
        self.__name = None
        self.__age = None
        self.__gender = None
        self.__mode = None
        self.__information = None
        self.__active = False

    def set_telegram_id(self, telegram_id):
        self.__telegram_id = telegram_id

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        self.__age = age

    def set_gender(self, gender):
        self.__gender = gender

    def set_mode(self, mode):
        self.__mode = mode

    def set_information(self, information):
        self.__information = information

    def change_active(self):
        self.__active = not self.__active

    def get_telegram_id(self):
        return self.__telegram_id

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def get_gender(self):
        return self.__age

    def get_mode(self):
        return self.__mode

    def get_information(self):
        return self.__information

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


bot = telebot.TeleBot('token')
menu = Menu()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_account = types.KeyboardButton('Создать профиль')
    markup.add(create_account)
    bot.send_message(message.chat.id, 'Я бот FoF. Здесь вы можете найти с кем подраться или потрахаться', 
                     reply_markup=markup)
    id = message.from_user.id
    bot.register_next_step_handler(message, name)


def name(message):
    bot.send_message(message.chat.id, 'Напиши имя', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_name)
    bot.register_next_step_handler(message, gender)


def get_name(message):
    nik = message.text


def gender(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    man = types.KeyboardButton('♂ М')
    woman = types.KeyboardButton('♀ Ж')
    markup.add(man, woman)
    bot.send_message(message.chat.id, 'Выбери пол', reply_markup=markup)
    bot.register_next_step_handler(message, get_gender)
    bot.register_next_step_handler(message, age)


def get_gender(message):
    gen = message.text


def age(message):
    bot.send_message(message.chat.id, 'Сколько тебе лет?', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_gender)
    bot.register_next_step_handler(message, mode)


def get_gender(message):
    count_years = message.text


def mode(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    favorite = types.KeyboardButton('❤')
    fight = types.KeyboardButton('👊')
    markup.add(favorite, fight)
    bot.send_message(message.chat.id, 'Укажи свой интерес', reply_markup=markup)
    bot.register_next_step_handler(message, get_mode)
    bot.register_next_step_handler(message, photo)


def get_mode(message):
    mood = message.text


def photo(message):
    bot.send_message(message.chat.id, 'Отправь фото', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_user_photo)
    bot.register_next_step_handler(message, about_me)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    photography = message.photo


def about_me(message):
    bot.send_message(message.chat.id, 'Расскажи о себе')
    bot.register_next_step_handler(message, get_about_me)
    bot.register_next_step_handler(message, finish)
    
    
def get_about_me(message):
    info = message.text
    
    
def finish(message):
    bot.send_message(message.chat.id, 'Анкета успешна создана')

bot.polling(none_stop=True, interval=0)
