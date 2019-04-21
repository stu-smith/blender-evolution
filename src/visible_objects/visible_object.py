from abc import abstractmethod
import colorsys
from ..renderable import Renderable


class VisibleObject(Renderable):

    def __init__(self, type, attribute_mappings, **kwargs):
        self._smooth = 0
        self._hsv = None
        self._ignore_for_camera_position = False

        common_attribute_mappings = {
            'smooth': {
                'attribute': '_smooth'
            },
            'hsv': {
                'attribute': '_hsv'
            },
            'ignore_for_camera_position': {
                'attribute': '_ignore_for_camera_position'
            }
        }

        all_attribute_mappings = {
            **attribute_mappings, **common_attribute_mappings
        }

        super().__init__(type, all_attribute_mappings, **kwargs)

    @abstractmethod
    def aabb(self):
        pass

    def apply_common_bpy_properties(self, bpy, blender_obj, name_prefix):
        if self._smooth:
            modifier = blender_obj.modifiers.new('Subsurf', 'SUBSURF')
            modifier.levels = self._smooth
            modifier.render_levels = self._smooth

            for poly in blender_obj.data.polygons:
                poly.use_smooth = True

        if self._hsv:
            mat = bpy.data.materials.new('{}_mat'.format(name_prefix))
            mat.diffuse_color = tuple(colorsys.hsv_to_rgb(*self._hsv))
            blender_obj.data.materials.append(mat)

    def get_common_json_properties(self):
        return {
            'smooth': self._smooth,
            'hsv': self._hsv
        }

    @property
    def ignore_for_camera_position(self):
        return self._ignore_for_camera_position
