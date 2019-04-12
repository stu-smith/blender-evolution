import math
import bpy
# pylint:disable=import-error
from mathutils import Vector
# pylint:enable=import-error

from ..aabb import AABB
from ..camera import Camera


class GenomeExpression(object):

    def __init__(self):
        self._visible_objects = []
        self._lights = []

    def add_visible_object(self, visible_object):
        self._visible_objects.append(visible_object)

    def add_light(self, light):
        self._lights.append(light)

    def get_visible_object_bounds(self):
        bounds = None

        for visible_object in self._visible_objects:
            visible_object_bounds = visible_object.aabb()

            if not visible_object.ignore_for_camera_position:
                bounds = AABB.union(bounds, visible_object_bounds)

        return bounds

    def generate_render_dict(self):
        bounds = self.get_visible_object_bounds()

        objects_list = []
        lights_list = []

        #
        # Convert visible objects to JSON objects.
        for visible_object in self._visible_objects:
            json_object = visible_object.to_json_object()
            objects_list.append(json_object)

        #
        # Convert lights to JSON objects.
        for light in self._lights:
            json_object = light.to_json_object()
            lights_list.append(json_object)

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

        camera = Camera(
            location=camera_location[:], rotation=camera_rotation[:])

        result = {
            'settings': {},
            'camera': camera.to_json_object(),
            'lights': lights_list,
            'objects': objects_list
        }

        return result
