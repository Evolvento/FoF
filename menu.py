from profile import Profile
from controller import Controller
from strategy_love import StrategyLove
from strategy_fight import StrategyFight


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