# pylint:disable=import-error
from mathutils import Euler, Vector
# pylint:enable=import-error

from .renderable import Renderable


class Camera(Renderable):

    TYPE = 'camera'

    def __init__(self, **kwargs):
        self._location = [0, 0, 0]
        self._rotation = [0, 0, 0]

        attribute_mappings = {
            'location': {
                'attribute': '_location'
            },
            'rotation': {
                'attribute': '_rotation'
            }
        }

        super().__init__(Camera.TYPE, attribute_mappings, **kwargs)

    def to_bpy(self, bpy, name_prefix):
        bpy.ops.object.add(type='CAMERA', location=tuple(self._location))
        cam = bpy.context.object
        cam.rotation_euler = Euler(tuple(self._rotation), 'XYZ')
        bpy.context.scene.camera = cam
