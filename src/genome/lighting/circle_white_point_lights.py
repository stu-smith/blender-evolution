import math

from ..gene import Gene
from ...lights.point_light import PointLight


class CircleWhitePointLightsGene(Gene):

    def all_properties(self):
        return []

    def express(self, genome_expression):
        bounds = genome_expression.get_visible_object_bounds()

        light_count = 10
        light_circle_radius = max(bounds.x2 - bounds.x1, bounds.y2 - bounds.y1)
        light_circle_z = bounds.z2 + (bounds.z2 - bounds.z1) * 2

        for light_index in range(0, light_count):
            light_angle = light_index / light_count * math.pi * 2
            light_x = math.cos(light_angle) * light_circle_radius
            light_y = math.sin(light_angle) * light_circle_radius

            light_location = [light_x, light_y, light_circle_z]
            light = PointLight(location=light_location,
                               hsv=[0, 0, 1],
                               energy=200)

            genome_expression.add_light(light)
