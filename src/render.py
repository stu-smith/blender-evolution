#
# This code is based on the examples found here:
# https://github.com/njanakiev/blender-scripting
#

import argparse
import json
import os
import re

import bpy
import colorsys
from math import pi
# pylint:disable=import-error
from mathutils import Euler
# pylint:enable=import-error

tau = 2*pi


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input',
        help='specify input JSON scene to be rendered',
        action='store',
        required=True
    )
    parser.add_argument(
        '--output',
        help='specify output location for PNG file',
        action='store',
        required=True
    )
    parser.add_argument(
        '--resolution',
        help='specify output resolution',
        action='store',
        required=True,
        metavar='WxH'
    )

    return parser.parse_args()


def load_input(file):
    with open(file) as stream:
        data = json.load(stream)
    return data


def read_triple(value, kind, input_ref):
    #
    # Read XYZ coordinate or rotation values.
    if isinstance(value, list):
        if len(value) != 3:
            raise Exception(
                'Expected exactly three {} components at: {}.'.format(
                    kind, input_ref)
            )
        for v in value:
            if not isinstance(v, (int, float)):
                raise Exception(
                    'Values for {} must be numeric at: {}.'.format(
                        kind, input_ref)
                )
        return (value[0], value[1], value[2])
    else:
        raise Exception('Cannot read {} at: {}.'.format(kind, input_ref))


def read_float(value, kind, input_ref):
    if not isinstance(value, (int, float)):
        raise Exception(
            'Value for {} must be numeric at: {}.'.format(
                kind, input_ref)
        )
    return value


def blender_setup():
    #
    # Blender seems to start with some objects already in scene, so remove all elements first.
    bpy.ops.object.select_by_layer()
    bpy.ops.object.delete(use_global=False)


def blender_camera(input):
    #
    # Read input values.
    input_camera = input['camera']
    input_camera_location = read_triple(
        input_camera['location'], 'location', 'camera/location'
    )
    input_camera_rotation = read_triple(
        input_camera['rotation'], 'Euler angles', 'camera/rotation'
    )

    #
    # Create camera.
    bpy.ops.object.add(type='CAMERA', location=input_camera_location)
    cam = bpy.context.object
    cam.rotation_euler = Euler(input_camera_rotation, 'XYZ')

    #
    # Make this the current camera
    bpy.context.scene.camera = cam


def blender_lights(input):
    #
    # Read input values.
    input_lights = input['lights']

    if not input_lights:
        raise Exception('No lights defined.')

    for idx, input_light in enumerate(input_lights):
        (hue, sat, val) = read_triple(
            input_light['hsv'], 'HSV', 'lights/{}/hsv'.format(str(idx))
        )
        input_light_location = read_triple(
            input_light['location'], 'HSV', 'lights/{}/location'.format(
                str(idx))
        )
        input_light_energy = read_float(
            input_light['energy'], 'energy', 'lights/{}/energy'.format(
                str(idx))
        )

        #
        # Create lamp.
        bpy.ops.object.add(type='LAMP', location=input_light_location)
        obj = bpy.context.object
        obj.data.type = 'POINT'

        # Apply gamma correction for Blender.
        color = tuple(pow(c, 2.2) for c in colorsys.hsv_to_rgb(hue, sat, val))

        # Set HSV color and lamp energy.
        obj.data.color = color
        obj.data.energy = input_light_energy


def blender_sphere(input_object, input_ref):
    sphere_location = read_triple(
        input_object['location'], 'location', '{}/location'.format(input_ref)
    )
    sphere_size = read_float(
        input_object['size'], 'size', '{}/size'.format(input_ref)
    )
    bpy.ops.mesh.primitive_ico_sphere_add(
        location=sphere_location, size=sphere_size
    )
    obj = bpy.context.object
    return obj


def blender_modifiers(blender_obj, input_obj, input_ref):
    if 'smooth' in input_obj:
        input_smooth = read_float(
            input_obj['smooth'], 'smooth', '{}/smooth'.format(input_ref)
        )

        modifier = blender_obj.modifiers.new('Subsurf', 'SUBSURF')
        modifier.levels = input_smooth
        modifier.render_levels = input_smooth

        for poly in blender_obj.data.polygons:
            poly.use_smooth = True


def blender_objects(input):
    type_dict = {
        'sphere': blender_sphere
    }

    input_objects = input['objects']

    if not input_objects:
        raise Exception('No objects defined.')

    for idx, input_object in enumerate(input_objects):
        input_object_type = input_object['type']
        input_ref = 'objects/{}[{}]'.format(idx, input_object_type)

        if not input_object_type in type_dict:
            raise Exception(
                'Unknown object type "{}" at: {}.'.format(
                    input_object_type, input_ref)
            )

        object_fn = type_dict[input_object_type]

        blender_obj = object_fn(input_object, input_ref)

        blender_modifiers(blender_obj, input_object, input_ref)


def blender_render(input, output_file, width, height):
    rnd = bpy.data.scenes['Scene'].render
    rnd.resolution_x = width
    rnd.resolution_y = height
    rnd.resolution_percentage = 100
    rnd.filepath = output_file
    bpy.ops.render.render(write_still=True)


def main():
    args = parse_args()

    if not os.path.exists(args.input):
        raise Exception('Input file "{}" not found.'.format(args.input))
    if os.path.exists(args.output):
        raise Exception('Output file "{}" already exists.'.format(args.output))

    resolution_pattern = r'^(\d+)x(\d+)$'

    resolution_match = re.search(resolution_pattern, args.resolution)

    if not resolution_match:
        raise Exception(
            'Resolution must be specified in the format WxH where W and H are numeric.'
        )

    resolution_width = int(resolution_match.group(1))
    resolution_height = int(resolution_match.group(2))

    input = load_input(args.input)

    blender_setup()
    blender_camera(input)
    blender_lights(input)
    blender_objects(input)
    blender_render(input, args.output, resolution_width, resolution_height)


if __name__ == '__main__':
    main()
