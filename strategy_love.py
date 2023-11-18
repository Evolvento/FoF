from istrategy import IStrategy
from db import DataAccessObject


class StrategyLove(IStrategy):
    def search(self, profile):
        if len(profile.get_liked) != 0:
            return profile.get_liked.pop(0)
        else:
            return DataAccessObject().return_profiles(5, profile.get_mode(), profile.get_gender()).pop(0)[0]
