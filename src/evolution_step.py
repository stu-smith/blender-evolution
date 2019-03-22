from enum import Enum
import json
import os
import subprocess
import tempfile
import threading
import time


class EvolutionStepState(Enum):
    not_started = 0,
    mutating = 1,
    rendering = 2,
    done = 3


class EvolutionStep(object):
    def __init__(self):
        self._state = EvolutionStepState.not_started
        self._tempdir = tempfile.TemporaryDirectory()

        threading.Thread(target=self._process).start()

    @property
    def state(self):
        return self._state

    @property
    def output_image_path(self):
        return self._output_path

    def destroy(self):
        if self._tempdir:
            self._tempdir.cleanup()
            self._tempdir = None

    def _process(self):
        time.sleep(2)

        self._state = EvolutionStepState.mutating
        time.sleep(3)
        json_dict = self._generate_json()
        input_path = self._write_json(json_dict)
        print('input_path: ' + input_path)

        self._state = EvolutionStepState.rendering
        self._output_path = self._render(input_path)
        print('output_path: ' + self._output_path)

        self._state = EvolutionStepState.done

    def _generate_json(self):
        json_dict = {
            "camera": {
                "location": [0, -10, 0],
                "rotation": [1.57, 0, 0]
            },
            "lights": [{
                "location": [-5, 0, 10],
                "hsv": [0, 1, 1],
                "energy": 1
            }, {
                "location": [5, 0, 10],
                "hsv": [0.6, 1, 1],
                "energy": 1
            }],
            "objects": [{
                "type": "sphere",
                "location": [-2.5, 0, 0],
                "size": 2
            }, {
                "type": "sphere",
                "location": [2.5, 0, 0],
                "size": 2,
                "smooth": 3
            }]
        }
        return json_dict

    def _write_json(self, json_dict):
        path = os.path.join(self._tempdir.name, 'input.json')

        with open(path, 'w') as s:
            json.dump(json_dict, s)

        return path

    def _render(self, input_path):
        output_path = os.path.join(self._tempdir.name, 'output.png')

        args = [
            'pipenv', 'run', 'python', '-m', 'src.render',
            '--input', input_path,
            '--output', output_path,
            '--resolution', '200x200'
        ]

        subprocess.call(args)

        return output_path
