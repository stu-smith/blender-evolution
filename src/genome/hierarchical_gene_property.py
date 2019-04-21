from abc import abstractmethod

from .gene_property import GeneProperty


class HierarchicalGeneProperty(GeneProperty):

    def mutate(self, configuration):
        pass

    @abstractmethod
    def available_types(self):
        pass
