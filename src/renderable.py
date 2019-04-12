from abc import ABC, abstractmethod


class Renderable(ABC):

    def __init__(self, type, attribute_mappings, **kwargs):
        self._type = type

        common_attribute_mappings = {
            'type': {
                'attribute': '_type'
            }
        }

        self._attribute_mappings = {
            **attribute_mappings, **common_attribute_mappings
        }

        for key, value in kwargs.items():
            found = False
            for setting, attribute_dict in self._attribute_mappings.items():
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

    def to_json_object(self):
        obj = {}

        for setting, attribute_dict in self._attribute_mappings.items():
            attribute = attribute_dict['attribute']
            value = getattr(self, attribute)
            obj[setting] = value

        return obj

    @abstractmethod
    def to_bpy(self, bpy, name_prefix):
        pass
