from enum import Enum
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
        threading.Thread(target=self._process).start()

    @property
    def state(self):
        return self._state

    def _process(self):
        time.sleep(2)
        self._state = EvolutionStepState.mutating
        time.sleep(3)
        self._state = EvolutionStepState.rendering
        time.sleep(5)
        self._state = EvolutionStepState.done

    def destroy(self):
        pass
