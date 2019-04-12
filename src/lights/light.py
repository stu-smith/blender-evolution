from ..renderable import Renderable


class Light(Renderable):
    def __init__(self, type, attribute_mappings, **kwargs):

        common_attribute_mappings = {

        }

        all_attribute_mappings = {
            **attribute_mappings, **common_attribute_mappings
        }

        super().__init__(type, all_attribute_mappings, **kwargs)
