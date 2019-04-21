from abc import ABC, abstractmethod


class GeneProperty(ABC):

    @abstractmethod
    def mutate(self, configuration):
        pass
