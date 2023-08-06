from abc import ABC, abstractmethod
from multiprocessing import Process as _Process
from threading import Thread as _Thread


class AbstractBaseProcessingStrategy(ABC):
    def __init__(self, target):
        self.target = target

    @abstractmethod
    def start():
        pass

    @abstractmethod
    def join():
        pass


class ExpensiveIOStrategy(_Thread, AbstractBaseProcessingStrategy):
    pass


class ExpensiveCalculationStrategy(_Process, AbstractBaseProcessingStrategy):
    pass
