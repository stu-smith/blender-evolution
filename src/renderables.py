from .camera import Camera

from .lights.point_light import PointLight

from .visible_objects.sphere import Sphere
from .visible_objects.mesh import Mesh


def renderable_from_dict(dict):
    constructors = {
        Camera.TYPE: Camera,

        PointLight.TYPE: PointLight,

        Sphere.TYPE: Sphere,
        Mesh.TYPE: Mesh
    }

    type_name = dict['type']

    constructor = constructors[type_name]

    return constructor(dict=dict)
