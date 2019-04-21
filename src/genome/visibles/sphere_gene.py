from ..gene import Gene
from ..scalar_gene_property import ScalarGeneProperty
from ..color_gene_property import ColorGeneProperty

from ...visible_objects.sphere import Sphere


class SphereGene(Gene):
    def __init__(self):
        self._size_property = ScalarGeneProperty(min=0.1, max=20, value=2)
        self._color_property = ColorGeneProperty(hsv=[0.0, 0.0, 1.0])

    def all_properties(self):
        return [
            self._size_property,
            self._color_property
        ]

    def express(self, genome_expression):
        location = [0, 0, 0]  # TODO genome_expression stack position
        size = self._size_property.value
        sphere = Sphere(location=location, size=size)
        # TODO color
        genome_expression.add_visible_object(sphere)
