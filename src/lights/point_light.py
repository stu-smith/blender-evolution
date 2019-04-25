import colorsys

from .light import Light


class PointLight(Light):

    TYPE = 'point-light'

    def __init__(self, **kwargs):
        self._location = [0, 0, 0]
        self._hsv = [0, 0, 1]
        self._energy = 100

        attribute_mappings = {
            'location': {
                'attribute': '_location'
            },
            'hsv': {
                'attribute': '_hsv'
            },
            'energy': {
                'attribute': '_energy'
            }
        }

        super().__init__(PointLight.TYPE, attribute_mappings, **kwargs)

    def to_bpy(self, bpy, name_prefix):
        bpy.ops.object.lamp_add(type='POINT', location=tuple(self._location))
        obj = bpy.context.object
        obj.data.type = 'POINT'

        color_list = [pow(c, 2.2) for c in colorsys.hsv_to_rgb(*self._hsv)]
        color_list.append(1.0)
        color = tuple(color_list)

        obj.data.use_nodes = True
        emission_node = obj.data.node_tree.nodes['Emission']
        emission_node.inputs['Strength'].default_value = self._energy
        emission_node.inputs['Color'].default_value = color
