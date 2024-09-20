
import numpy as np

from .base import BaseModule


class FixedModule(BaseModule):
    def __init__(self, values: np.ndarray, initial_step=0):
        super().__init__(initial_step)
        self.values = values

    def _get_state(self):
        return self.values[self._current_step]
    
    def step(self, action=None):
        curr_state = self._get_state()
        self._update_step()
        return curr_state

    def __len__(self):
        return len(self.values)


class PVModule(FixedModule):
    def __init__(self, values, initial_step=0):
        super().__init__(values, initial_step)        


class WTModule(FixedModule):
    def __init__(self, values, initial_step=0):
        super().__init__(values, initial_step)


class Demand(FixedModule):
    def __init__(self, values, initial_step=0):
        super().__init__(values, initial_step)


class Price(FixedModule):
    def __init__(self, values, initial_step=0):
        super().__init__(values, initial_step)
