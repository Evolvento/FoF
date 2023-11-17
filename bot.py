import telebot
import sqlite3
from db import DataAccessObject
from telebot import types
from menu import Menu
from profile import Profile
from controller import Controller
from strategy_love import StrategyLove
from strategy_fight import StrategyFight


bot = telebot.TeleBot('token')
menu = Menu()


def like(our_id, liked_id):
    menu.array_profiles[liked_id].append_liked(our_id)


def partner_search(telegram_id):
    controller = Controller()
    if menu.array_profiles[telegram_id].get_mode() == 'love':
        controller.set_strategy(StrategyLove())
    if menu.array_profiles[telegram_id].get_mode() == 'fight':
        controller.set_strategy(StrategyFight())
    return controller.execute(menu.array_profiles[telegram_id])


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_account = types.KeyboardButton('Создать профиль')
    markup.add(create_account)
    bot.send_message(message.chat.id, 'Я бот FoF. Здесь вы можете найти, с кем подраться или подружиться',
                     reply_markup=markup)
    menu.array_profiles[message.from_user.id] = Profile()
    menu.array_profiles[message.from_user.id].set_telegram_id(message.from_user.id)
    bot.register_next_step_handler(message, name)


def name(message):
    bot.send_message(message.chat.id, 'Напиши имя', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_name)
    bot.register_next_step_handler(message, gender)


def get_name(message):
    nik = message.text
    menu.array_profiles[message.from_user.id].set_name(nik)


def gender(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    man = types.KeyboardButton('♂️')
    woman = types.KeyboardButton('♀️')
    markup.add(man, woman)
    bot.send_message(message.chat.id, 'Выбери пол', reply_markup=markup)
    bot.register_next_step_handler(message, get_gender)
    bot.register_next_step_handler(message, age)


def get_gender(message):
    gen = message.text
    menu.array_profiles[message.from_user.id].set_gender(gen)


def age(message):
    bot.send_message(message.chat.id, 'Сколько тебе лет?', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_age)
    bot.register_next_step_handler(message, mode)


def get_age(message):
    count_years = message.text
    menu.array_profiles[message.from_user.id].set_age(count_years)


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
    menu.array_profiles[message.from_user.id].set_mode(mood)


def photo(message):
    bot.send_message(message.chat.id, 'Отправь фото', reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_user_photo)
    bot.register_next_step_handler(message, about_me)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file = requests.get('https://api.telegram.org/file/bot{}/{}'.format('6442510200:AAHIEQsXG6ypotSBDDE3lmIj2NksGHrCArw', file_info.file_path))
    filename = 'Files/photo_{}.jpg'.format(file_info.file_id)
    menu.array_profiles[message.from_user.id].set_photo(file_info.file_id)
    with open(filename, 'wb') as f:
        f.write(file.content)
    photography = file_info.file_id


def about_me(message):
    bot.send_message(message.chat.id, 'Расскажи о себе')
    bot.register_next_step_handler(message, get_about_me)
    bot.register_next_step_handler(message, finish)


def get_about_me(message):
    information = message.text
    menu.array_profiles[message.from_user.id].set_information(information)


def finish(message):
    bot.send_message(message.chat.id, 'Анкета успешна создана')
    dao = DataAccessObject()
    dao.create_user(menu.array_profiles[message.from_user.id].get_telegram_id(),
                    menu.array_profiles[message.from_user.id].get_name(),
                    menu.array_profiles[message.from_user.id].get_gender(),
                    menu.array_profiles[message.from_user.id].get_age(),
                    menu.array_profiles[message.from_user.id].get_mode(),
                    menu.array_profiles[message.from_user.id].get_information(),
                    menu.array_profiles[message.from_user.id].get_photo())
    dao.show_base()
    info(message)
    main_buttons(message)


def main_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    watch_account = types.KeyboardButton('👀')
    start_search = types.KeyboardButton('🔍')
    more_not_need = types.KeyboardButton('🚪')
    markup.add(watch_account, start_search, more_not_need)
    bot.send_message(message.chat.id, '👀 - посмотреть профиль \n'
                                      '🔍 - начать поиск \n'
                                      '🚪 - перестать кого-либо искать', reply_markup=markup)


def info(message):
    photography = open('Files/photo_{}.jpg'.format(DataAccessObject().get_user(message.from_user.id)[6]), 'rb')
    bot.send_photo(message.chat.id, photography, f'{DataAccessObject().get_user(message.from_user.id)[1]}, '
                                                 f'{DataAccessObject().get_user(message.from_user.id)[3]}, \n'
                                                 f'{DataAccessObject().get_user(message.from_user.id)[5]}')


bot.polling(none_stop=True, interval=0)
