
from .base import BaseModule


class HydroFuelCell(BaseModule):
    def __init__(self, min_capacity, max_capacity, rated_soel, rated_sofc, e2h, h2e, soel_efficiency, sofc_efficiency, hydrogen_price, init_soc, initial_step=0):
        super().__init__(initial_step)
        
        self.min_capacity = min_capacity
        self.max_capacity = max_capacity
        self.min_soc = self.min_capacity / self.max_capacity
        
        self.rated_soel = rated_soel
        self.rated_sofc = rated_sofc
        
        self.e2h = e2h
        self.h2e = h2e
        
        self.soel_efficiency = soel_efficiency
        self.sofc_efficiency = sofc_efficiency
        
        self.hydrogen_price = hydrogen_price
        
        self.init_soc = init_soc
        self.curr_soc = init_soc

    def get_state(self):
        return self.curr_soc

    def reset(self):
        self.curr_soc = self.init_soc

    def step(self, action):
        profit, fossil = 0, 0
        if action >= 0:
            # soel
            soel_power = min(action, self.rated_soel)
            delta_soc = soel_power * self.soel_efficiency * self.e2h / self.max_capacity
            new_soc = self.curr_soc + delta_soc
            if new_soc >= 1:
                self.curr_soc = self.min_soc
                profit = (self.max_capacity - self.min_capacity) * self.hydrogen_price
            else:
                self.curr_soc = new_soc
        else:
            # sofc
            action = -action
            sofc_power = min(action, self.rated_sofc)
            delta_soc = sofc_power / self.sofc_efficiency / self.h2e / self.max_capacity
            new_soc = self.curr_soc - delta_soc
            if new_soc < self.min_soc:
                self.curr_soc = self.min_soc
                fossil = (self.min_soc - new_soc) * self.max_capacity * self.h2e * self.sofc_efficiency
            else:
                self.curr_soc = new_soc

        self._update_step()

        return profit, fossil
