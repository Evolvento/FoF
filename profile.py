class Profile:
    def __init__(self):
        self.__telegram_id = None
        self.__name = None
        self.__age = None
        self.__gender = None
        self.__mode = None
        self.__photo = None
        self.__information = None
        self.__active = False
        self.__height = None
        self.__liked = []

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

    def set_photo(self, photo):
        self.__photo = photo

    def set_information(self, information):
        self.__information = information

    def set_height(self, height):
        self.__height = height

    def append_liked(self, telegram_id):
        self.__liked.append(telegram_id)

    def change_active(self):
        self.__active = not self.__active

    def get_telegram_id(self):
        return self.__telegram_id

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def get_gender(self):
        return self.__gender

    def get_mode(self):
        return self.__mode

    def get_photo(self):
        return self.__photo

    def get_information(self):
        return self.__information

    def get_height(self):
        return self.__height

    def get_active(self):
        return self.__active

    def get_liked(self):
        return self.__liked
