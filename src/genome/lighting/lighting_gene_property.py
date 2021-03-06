import random

from ..gene_property import GeneProperty
from .circle_white_point_lights import CircleWhitePointLightsGene


class LightingGeneProperty(GeneProperty):

    def __init__(self):
        self._gene = random.choice(self.available_types())()

    def mutate(self, configuration):
        self._gene.mutate(configuration)

    def available_types(self):
        return [
            CircleWhitePointLightsGene
        ]

    @property
    def gene(self):
        return self._gene
