from .visible_object import VisibleObject
from ..aabb import AABB


class Mesh(VisibleObject):
    def __init__(self, **kwargs):
        self._vertexes = []
        self._faces = []

        attribute_mappings = {
            'vertexes': {
                'attribute': '_vertexes'
            },
            'faces': {
                'attribute': '_faces'
            }
        }

        super().__init__(attribute_mappings, **kwargs)

    def aabb(self):
        bounds = None

        for vertex in self._vertexes:
            vx = vertex[0]
            vy = vertex[1]
            vz = vertex[2]

            point = AABB(x1=vx, x2=vx, y1=vy, y2=vy, z1=vz, z2=vz)
            bounds = AABB.union(bounds, point)

        return bounds

    def to_json_objects(self):
        json = {
            'type': 'mesh',
            'vertexes': self._vertexes,
            'faces': self._faces
        }
        json = {**json, **self.get_common_json_properties()}
        return [json]

    def to_bpy(self, bpy, name_prefix):
        vertexes = [tuple(v) for v in self._vertexes]
        faces = [tuple(f) for f in self._faces]

        mesh = bpy.data.meshes.new(name_prefix)

        obj = bpy.data.objects.new(name_prefix, mesh)

        bpy.context.scene.objects.link(obj)

        mesh.from_pydata(vertexes, [], faces)
        mesh.update(calc_edges=True)

        # obj.location.x = px
        # obj.location.y = py
        # obj.location.z = pz

        super().apply_common_bpy_properties(obj)

        return obj
