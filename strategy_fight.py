from istrategy import IStrategy
from db import DataAccessObject


class StrategyFight(IStrategy):
    def search(self, profile):
        if len(profile.get_liked()) != 0:
            return ((profile.get_liked().pop(0),),)
        else:
            return DataAccessObject().return_profiles(profile.get_age() - 5, profile.get_age() + 5, profile.get_mode(), profile.get_gender(), profile.get_height() - 10, profile.get_height() + 10)
