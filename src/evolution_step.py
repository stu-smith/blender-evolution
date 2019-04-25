from enum import Enum
import json
import math
import os
import subprocess
import tempfile
import threading
import time

from .genome.genome_expression import GenomeExpression
from .visible_objects.sphere import Sphere
from .visible_objects.mesh import Mesh
from .lights.point_light import PointLight

# spellchecker:ignore isfile


class EvolutionStepState(Enum):
    not_started = 0,
    mutating = 1,
    rendering = 2,
    done = 3


class EvolutionStep(object):

    def __init__(self, configuration, genome, do_mutate=True):
        self._state = EvolutionStepState.not_started
        self._tempdir = tempfile.TemporaryDirectory()
        self._render_width = None
        self._render_height = None
        self._destroyed = False
        self._configuration = configuration
        self._genome = genome
        self._do_mutate = do_mutate

        threading.Thread(target=self._process).start()

    @property
    def state(self):
        return self._state

    @property
    def output_image_path(self):
        return self._output_path

    def set_render_size(self, width, height):
        self._render_width = width
        self._render_height = height

        if self._state == EvolutionStepState.done:
            threading.Thread(target=self._process_render_only).start()

    def destroy(self):
        if self._tempdir:
            self._tempdir.cleanup()
            self._tempdir = None
        self._destroyed = True

    def _process(self):
        if self._do_mutate:
            self._state = EvolutionStepState.mutating
            self._genome.mutate()

        json_dict = self._generate_json()
        self._input_path = self._write_json(json_dict)

        self._process_render_only()

    def _process_render_only(self):
        self._state = EvolutionStepState.rendering

        while True:
            self._start_render_width = self._render_width
            self._start_render_height = self._render_height
            self._output_path = self._render(self._input_path)

            if self._start_render_width == self._render_width and self._start_render_height == self._render_height:
                break

        self._state = EvolutionStepState.done

    def _generate_json(self):
        genome_expression = self._genome.express()

        # TODO: Make ground part of genome, size to objects.
        ground = Mesh(
            vertexes=[
                [-10, -10, -3],
                [10, -10, -3],
                [10, 10, -3],
                [-10, 10, -3]
            ],
            faces=[[0, 1, 2, 3]],
            ignore_for_camera_position=True
        )

        genome_expression.add_visible_object(ground)

        json_dict = genome_expression.generate_render_dict()

        json_dict['settings']['samples'] = self._configuration.cycles_samples
        json_dict['settings']['max_bounces'] = self._configuration.cycles_max_bounces

        return json_dict

    def _write_json(self, json_dict):
        path = os.path.join(self._tempdir.name, 'input.json')

        with open(path, 'w') as s:
            json.dump(json_dict, s)

        return path

    def _render(self, input_path):
        output_path = os.path.join(self._tempdir.name, 'output.png')

        if os.path.isfile(output_path):
            os.remove(output_path)

        while self._render_width is None or self._render_height is None:
            if self._destroyed:
                return
            time.sleep(0.1)

        if self._destroyed:
            return

        args = [
            'pipenv', 'run', 'python', '-m', 'src.render',
            '--input', input_path,
            '--output', output_path,
            '--resolution', '{}x{}'.format(self._render_width,
                                           self._render_height)
        ]

        subprocess.call(args)

        return output_path
