from abc import ABC, abstractmethod


class VisibleObject(ABC):

    def __init__(self, attribute_mappings, **kwargs):
        self._smooth = 0
        self._ignore_for_camera_position = False

        common_attribute_mappings = {
            'smooth': {
                'attribute': '_smooth'
            },
            'ignore_for_camera_position': {
                'attribute': '_ignore_for_camera_position'
            }
        }

        all_attribute_mappings = {
            **attribute_mappings, **common_attribute_mappings
        }

        for key, value in kwargs.items():
            found = False
            for setting, attribute_dict in all_attribute_mappings.items():
                attribute = attribute_dict['attribute']
                if key == setting:
                    setattr(self, attribute, value)
                    found = True
                elif key == 'dict':
                    if setting in value:
                        setattr(self, attribute, value[setting])
                        found = True
            if not found:
                raise('Unknown parameter {}.'.format(key))

    @abstractmethod
    def aabb(self):
        pass

    @abstractmethod
    def to_json_objects(self):
        pass

    @abstractmethod
    def to_bpy(self, bpy, name_prefix):
        pass

    def apply_common_bpy_properties(self, blender_obj):
        if self._smooth:
            modifier = blender_obj.modifiers.new('Subsurf', 'SUBSURF')
            modifier.levels = self._smooth
            modifier.render_levels = self._smooth

            for poly in blender_obj.data.polygons:
                poly.use_smooth = True

    def get_common_json_properties(self):
        return {
            'smooth': self._smooth
        }

    @property
    def ignore_for_camera_position(self):
        return self._ignore_for_camera_position
