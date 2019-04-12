from ..gene_property import GeneProperty
from .circle_white_point_lights import CircleWhitePointLights


class LightingGeneProperty(GeneProperty):

    def mutate(self):
        pass

    def available_types(self):
        return [
            CircleWhitePointLights
        ]
