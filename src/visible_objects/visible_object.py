from abc import ABC, abstractmethod


class VisibleObject(ABC):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'smooth':
                self._smooth = value
            elif key == 'dict':
                if 'smooth' in value:
                    self._smooth = dict['smooth']

    @abstractmethod
    def aabb(self):
        pass

    @abstractmethod
    def to_json_objects(self):
        pass

    @abstractmethod
    def to_bpy(self, bpy):
        pass

    def apply_common_bpy_properties(self, blender_obj):
        if self._smooth:
            modifier = blender_obj.modifiers.new('Subsurf', 'SUBSURF')
            modifier.levels = self._smooth
            modifier.render_levels = self._smooth

            for poly in blender_obj.data.polygons:
                poly.use_smooth = True
