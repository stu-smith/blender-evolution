from abc import ABC, abstractmethod


class Gene(ABC):
    @abstractmethod
    def all_properties(self):
        pass

    @abstractmethod
    def mutate(self, configuration):
        pass

    @abstractmethod
    def express(self, genome_expression):
        pass
