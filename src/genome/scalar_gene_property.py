import random

from .gene_property import GeneProperty


class ScalarGeneProperty(GeneProperty):

    def __init__(self, min, max, value):
        self._min = min
        self._max = max
        self._value = value

    @property
    def value(self):
        return self._value

    def mutate(self, configuration):
        if random.random() < configuration.p_scalar_mutation:
            range = self._max - self._min
            sigma = range * configuration.scalar_range_sigma
            move = random.normalvariate(0, sigma)

            self._value += move

            if self._value < self._min:
                self._value = self._min
            if self._value > self._max:
                self._value = self._max
