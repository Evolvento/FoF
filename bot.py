import telebot
import sqlite3
import requests
from db import DataAccessObject
from telebot import types
from profile import Profile
from controller import Controller
from strategy_love import StrategyLove
from strategy_fight import StrategyFight


class Bot:
    def __init__(self):
        self.array_profiles = {}
        self.bot = telebot.TeleBot('6442510200:AAHIEQsXG6ypotSBDDE3lmIj2NksGHrCArw')

        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            create_account = types.KeyboardButton('Создать профиль')
            markup.add(create_account)
            self.bot.send_message(message.chat.id, 'Я бот FoF. Здесь вы можете найти, с кем подраться или подружиться',
                             reply_markup=markup)
            self.array_profiles[message.from_user.id] = Profile()
            self.array_profiles[message.from_user.id].set_telegram_id(message.from_user.id)
            self.bot.register_next_step_handler(message, name)

        def like(our_id, liked_id):
            self.array_profiles[liked_id].append_liked(our_id)

        def partner_search(telegram_id):
            controller = Controller()
            if self.array_profiles[telegram_id].get_mode() == 'love':
                controller.set_strategy(StrategyLove())
            if self.array_profiles[telegram_id].get_mode() == 'fight':
                controller.set_strategy(StrategyFight())
            return controller.execute(self.array_profiles[telegram_id])

        def name(message):
            self.bot.send_message(message.chat.id, 'Напиши имя', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, get_name)
            self.bot.register_next_step_handler(message, gender)

        def get_name(message):
            nik = message.text
            self.array_profiles[message.from_user.id].set_name(nik)

        def gender(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            man = types.KeyboardButton('male')
            woman = types.KeyboardButton('female')
            markup.add(man, woman)
            self.bot.send_message(message.chat.id, 'Выбери пол', reply_markup=markup)
            self.bot.register_next_step_handler(message, get_gender)
            self.bot.register_next_step_handler(message, age)

        def get_gender(message):
            gen = message.text
            self.array_profiles[message.from_user.id].set_gender(gen)

        def age(message):
            self.bot.send_message(message.chat.id, 'Сколько тебе лет?', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, get_age)
            self.bot.register_next_step_handler(message, mode)

        def get_age(message):
            count_years = message.text
            self.array_profiles[message.from_user.id].set_age(count_years)

        def mode(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            favorite = types.KeyboardButton('❤')
            fight = types.KeyboardButton('👊')
            markup.add(favorite, fight)
            self.bot.send_message(message.chat.id, 'Укажи свой интерес', reply_markup=markup)
            self.bot.register_next_step_handler(message, get_mode)
            self.bot.register_next_step_handler(message, photo)

        def get_mode(message):
            mood = message.text
            self.array_profiles[message.from_user.id].set_mode(mood)

        def photo(message):
            self.bot.send_message(message.chat.id, 'Отправь фото', reply_markup=types.ReplyKeyboardRemove())
            self.bot.register_next_step_handler(message, get_user_photo)
            self.bot.register_next_step_handler(message, about_me)

        @self.bot.message_handler(content_types=['photo'])
        def get_user_photo(message):
            file_info = self.bot.get_file(message.photo[-1].file_id)
            file = requests.get('https://api.telegram.org/file/bot{}/{}'.format('6442510200:AAHIEQsXG6ypotSBDDE3lmIj2NksGHrCArw', file_info.file_path))
            filename = 'Files/photo_{}.jpg'.format(file_info.file_id)
            self.array_profiles[message.from_user.id].set_photo(file_info.file_id)
            with open(filename, 'wb') as f:
                f.write(file.content)
            photography = file_info.file_id

        def about_me(message):
            self.bot.send_message(message.chat.id, 'Расскажи о себе')
            self.bot.register_next_step_handler(message, get_about_me)
            self.bot.register_next_step_handler(message, finish)

        def get_about_me(message):
            information = message.text
            self.array_profiles[message.from_user.id].set_information(information)

        def finish(message):
            self.bot.send_message(message.chat.id, 'Анкета успешна создана')
            dao = DataAccessObject()
            dao.create_user(self.array_profiles[message.from_user.id].get_telegram_id(),
                            self.array_profiles[message.from_user.id].get_name(),
                            self.array_profiles[message.from_user.id].get_gender(),
                            self.array_profiles[message.from_user.id].get_age(),
                            self.array_profiles[message.from_user.id].get_mode(),
                            self.array_profiles[message.from_user.id].get_information(),
                            self.array_profiles[message.from_user.id].get_photo())
            dao.show_base()
            info(message, message.from_user.id)

        def main_buttons(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            watch_account = types.KeyboardButton('👀')
            start_search = types.KeyboardButton('🔍')
            more_not_need = types.KeyboardButton('🚪')
            markup.add(watch_account, start_search, more_not_need)
            self.bot.send_message(message.chat.id, '👀 - посмотреть профиль \n'
                                              '🔍 - начать поиск \n'
                                              '🚪 - перестать кого-либо искать', reply_markup=markup)

        @self.bot.message_handler(func=lambda m: m.text == "👀")
        def show_my_profile(message):
            info(message, message.from_user.id)

        @self.bot.message_handler(func=lambda m: m.text == "🔍")
        def search(message):
            partner_id = partner_search(message.from_user.id)
            info(message, partner_id)
            main_buttons()

        def info(message, telegram_id):
            photography = open('Files/photo_{}.jpg'.format(DataAccessObject().get_user(telegram_id)[6]), 'rb')
            self.bot.send_photo(message.chat.id, photography, f'{DataAccessObject().get_user(telegram_id)[1]}, '
                                                         f'{DataAccessObject().get_user(telegram_id)[3]} \n'
                                                         f'{DataAccessObject().get_user(telegram_id)[5]}')
            main_buttons(message)

    def run(self):
        self.bot.polling(none_stop=True, interval=0)


telegram = Bot()
telegram.run()
