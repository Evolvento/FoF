import telebot
from telebot import types

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


bot.polling(none_stop=True, interval=0)
