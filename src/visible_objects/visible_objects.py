from .sphere import Sphere


def visible_object_from_dict(dict):
    constructors = {
        'sphere': Sphere
    }

    type_name = dict['type']

    constructor = constructors[type_name]

    return constructor(dict=dict)
