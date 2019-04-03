from .visible_object import VisibleObject

from ..aabb import AABB


class Sphere(VisibleObject):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'location':
                self._location = value
            elif key == 'size':
                self._size = value
            elif key == 'smooth':
                self._smooth = value
            elif key == 'dict':
                self._location = value['location']
                self._size = value['size']
                self._smooth = value['smooth']
            else:
                raise TypeError('Unknown argument "{}".'.format(key))

        super().__init__(**kwargs)

    def aabb(self):
        (cx, cy, cz) = self._location
        r = self._size
        return AABB(cx - r, cx + r, cy - r, cy + r, cz - r, cz + r)

    def to_json_objects(self):
        (cx, cy, cz) = self._location
        return [{
            'type': 'sphere',
            'location': [cx, cy, cz],
            'size': self._size,
            'smooth': self._smooth
        }]

    def to_bpy(self, bpy):
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=self._location, size=self._size
        )
        obj = bpy.context.object

        super().apply_common_bpy_properties(obj)

        return obj
