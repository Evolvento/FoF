from abc import ABC, abstractmethod


class IStrategy(ABC):
    @abstractmethod
    def search(self, profile):
        pass