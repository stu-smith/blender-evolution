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

from .renderables import renderable_from_dict


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
    max_bounces = read_int(
        input_settings['max_bounces'], 'max_bounces', 'settings/max_bounces'
    )

    scene = bpy.data.scenes['Scene']
    scene.world.use_nodes = True
    scene.cycles.samples = samples
    scene.cycles.max_bounces = max_bounces
    background_node = scene.world.node_tree.nodes['Background']
    background_node.inputs['Color'].default_value = (0.0, 0.0, 0.0, 0.0)


def blender_renderables(input):
    kinds = ['camera', 'lights', 'objects']

    for kind in kinds:
        input_objects = input[kind]

        if not isinstance(input_objects, list):
            input_objects = [input_objects]

        if not input_objects:
            raise Exception('No {} defined.'.format(kind))

        for idx, input_object in enumerate(input_objects):
            renderable = renderable_from_dict(input_object)
            name_prefix = '{}_{}_'.format(kind, idx)

            renderable.to_bpy(bpy, name_prefix)


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
    blender_renderables(input)
    blender_render(input, args.output, resolution_width, resolution_height)


if __name__ == '__main__':
    main()
