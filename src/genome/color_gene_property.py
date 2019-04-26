import pprint
import random

from .gene_property import GeneProperty


class ColorGeneProperty(GeneProperty):

    def __init__(self, hsv):
        self._hsv = hsv

    @property
    def value(self):
        return self._hsv

    def mutate(self, configuration):
        print('in color.mutate')
        if random.random() < configuration.p_color_mutation:
            print('yes')
            sigma = configuration.color_sigma

            new_hsv = [c + random.normalvariate(0, sigma) for c in self._hsv]
            pprint.pprint(new_hsv)

            self._hsv = [max(0.0, min(c, 1.0)) for c in new_hsv]
        else:
            print('no')
