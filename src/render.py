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

from .visible_objects.visible_objects import visible_object_from_dict


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
                    kind, input_ref
                )
            )
        for v in value:
            if not isinstance(v, (int, float)):
                raise Exception(
                    'Values for {} must be numeric at: {}.'.format(
                        kind, input_ref
                    )
                )
        return (value[0], value[1], value[2])
    else:
        raise Exception('Cannot read {} at: {}.'.format(kind, input_ref))


def read_float(value, kind, input_ref):
    if not isinstance(value, (int, float)):
        raise Exception(
            'Value for {} must be numeric at: {}.'.format(kind, input_ref)
        )
    return value


def read_int(value, kind, input_ref):
    if not isinstance(value, int):
        raise Exception(
            'Value for {} must be integer at: {}.'.format(kind, input_ref)
        )
    return value


def blender_setup(input):
    #
    # Blender seems to start with some objects already in scene, so remove all elements first.
    bpy.ops.object.select_by_layer()
    bpy.ops.object.delete(use_global=False)

    input_settings = input['settings']

    samples = read_int(
        input_settings['samples'], 'samples', 'settings/samples'
    )

    scene = bpy.data.scenes['Scene']
    scene.world.use_nodes = True
    scene.cycles.samples = samples
    background_node = scene.world.node_tree.nodes['Background']
    background_node.inputs['Color'].default_value = (0.0, 0.0, 0.0, 0.0)


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
        bpy.ops.object.lamp_add(type='POINT', location=input_light_location)
        obj = bpy.context.object
        obj.data.type = 'POINT'

        # Apply gamma correction for Blender.
        color_list = [pow(c, 2.2) for c in colorsys.hsv_to_rgb(hue, sat, val)]
        color_list.append(1.0)
        color = tuple(color_list)

        # Set HSV color and lamp energy.
        obj.data.use_nodes = True
        obj.data.node_tree.nodes['Emission'].inputs['Strength'].default_value = input_light_energy
        obj.data.node_tree.nodes['Emission'].inputs['Color'].default_value = color


def blender_objects(input):
    input_objects = input['objects']

    if not input_objects:
        raise Exception('No objects defined.')

    for input_object in input_objects:
        visible_object = visible_object_from_dict(input_object)

        visible_object.to_bpy(bpy)


def blender_render(input, output_file, width, height):
    scene = bpy.data.scenes['Scene']
    rnd = scene.render
    rnd.engine = 'CYCLES'
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

    blender_setup(input)
    blender_camera(input)
    blender_lights(input)
    blender_objects(input)
    blender_render(input, args.output, resolution_width, resolution_height)


if __name__ == '__main__':
    main()
