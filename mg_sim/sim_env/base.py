
import numpy as np


class BaseModule:
    """
    Base class for all microgrid _modules.
    All values passed to step(self) that result in non-negative
    """
    
    def __init__(self, initial_step=0):

        self.initial_step = initial_step
        self._current_step = initial_step

    def reset(self):
        """
        Reset the module to step zero.

        """
        self._update_step(reset=True)

    def _update_step(self, reset=False):
        if reset:
            self._current_step = self.initial_step
        else:
            self._current_step += 1

    def step(self, action):
        """
        Take one step in the module, attempting to draw or send ``action`` amount of energy.
        """
        pass
