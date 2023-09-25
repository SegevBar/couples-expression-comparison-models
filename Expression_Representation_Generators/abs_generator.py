from abc import ABC, abstractmethod

class AbstractGenerator(ABC):

    @abstractmethod
    def generate_expressions_representation(self):
        pass