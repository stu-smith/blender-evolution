import math
import bpy
# pylint:disable=import-error
from mathutils import Vector
# pylint:enable=import-error

from ..aabb import AABB


class GenomeExpression(object):

    def __init__(self):
        self._visible_objects = []

    def add_object(self, visible_object):
        self._visible_objects.append(visible_object)

    def generate_render_dict(self):
        result = {
            'settings': {},
            'camera': {},
            'lights': [],
            'objects': []
        }

        bounds = None

        #
        # Convert visible objects to JSON objects.
        # Also compute overall model bounds.
        for visible_object in self._visible_objects:
            json_objects = visible_object.to_json_objects()
            result['objects'] += json_objects
            visible_object_bounds = visible_object.aabb()
            bounds = AABB.union(bounds, visible_object_bounds)

        #
        # Arrange lights in a circle around the midpoint.
        light_count = 10
        light_circle_radius = max(bounds.x2 - bounds.x1, bounds.y2 - bounds.y1)
        light_circle_z = bounds.z2 + (bounds.z2 - bounds.z1) * 2

        for light_index in range(0, light_count):
            light_angle = light_index / light_count * math.pi * 2
            light_x = math.cos(light_angle) * light_circle_radius
            light_y = math.sin(light_angle) * light_circle_radius

            result['lights'].append({
                'location': [light_x, light_y, light_circle_z],
                'hsv': [0, 0, 1],
                'energy': 2000  # TODO: Compute based on light distance.
            })

        #
        # Position camera.
        camera_x = bounds.mid_x
        camera_y = bounds.y1 - (bounds.y2 - bounds.y1) * 2.5
        camera_z = bounds.z2

        focus_point = Vector((bounds.mid_x, bounds.mid_y, bounds.mid_z))
        camera_location = Vector((camera_x, camera_y, camera_z))

        camera_look = camera_location - focus_point
        rot_quat = camera_look.to_track_quat('Z', 'Y')

        camera_rotation = rot_quat.to_euler()

        result['camera']['location'] = list(camera_location)
        result['camera']['rotation'] = list(camera_rotation)

        return result
