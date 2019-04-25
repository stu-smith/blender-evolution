import random

from .gene_property import GeneProperty


class ColorGeneProperty(GeneProperty):

    def __init__(self, hsv):
        self._hsv = hsv

    @property
    def value(self):
        return self._hsv

    def mutate(self, configuration):
        if random.random() < configuration.p_color_mutation:
            sigma = configuration.color_sigma

            new_hsv = [c + random.normalvariate(0, sigma) for c in self._hsv]

            self._hsv = [max(0.0, min(c, 1.0)) for c in new_hsv]
