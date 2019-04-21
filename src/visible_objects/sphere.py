from .visible_object import VisibleObject
from ..aabb import AABB


class Sphere(VisibleObject):

    TYPE = 'sphere'

    def __init__(self, **kwargs):
        self._location = [0, 0, 0]
        self._size = 2

        attribute_mappings = {
            'location': {
                'attribute': '_location'
            },
            'size': {
                'attribute': '_size'
            }
        }

        super().__init__(Sphere.TYPE, attribute_mappings, **kwargs)

    def aabb(self):
        (cx, cy, cz) = self._location
        r = self._size
        return AABB(cx - r, cx + r, cy - r, cy + r, cz - r, cz + r)

    def to_bpy(self, bpy, name_prefix):
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=self._location, size=self._size
        )
        obj = bpy.context.object

        super().apply_common_bpy_properties(bpy, obj, name_prefix)

        return obj
