from abc import ABC, abstractmethod


class Gene(ABC):
    @abstractmethod
    def all_properties(self):
        pass

    def mutate(self, configuration):
        properties = self.all_properties()

        for property in properties:
            property.mutate(configuration)

    @abstractmethod
    def express(self, genome_expression):
        pass
