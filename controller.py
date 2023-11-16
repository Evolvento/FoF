from istrategy import IStrategy


class Controller:
    def __init__(self):
        self.strategy = None

    def set_strategy(self, strategy: IStrategy):
        self.strategy = strategy

    def execute(self, profile):
        return self.strategy.search(profile)