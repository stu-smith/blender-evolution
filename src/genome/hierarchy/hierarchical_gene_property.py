from abc import abstractmethod
import random

from ..gene_property import GeneProperty
from ..visibles.sphere_gene import SphereGene


class HierarchicalGeneProperty(GeneProperty):

    def __init__(self):
        self._gene = random.choice(self.available_types())()

    def mutate(self, configuration):
        self._gene.mutate(configuration)

    def available_types(self):
        return [
            SphereGene
        ]

    @property
    def gene(self):
        return self._gene
