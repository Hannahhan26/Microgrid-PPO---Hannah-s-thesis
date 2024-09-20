
from .base import BaseModule


class Battery(BaseModule):
    def __init__(self, min_capacity, max_capacity, rated_charge, rated_discharge, charge_efficiency, discharge_efficiency, init_soc, initial_step=0):
        super().__init__(initial_step)
        
        self.min_capacity = min_capacity
        self.max_capacity = max_capacity
        self.min_soc = self.min_capacity / self.max_capacity
        
        self.rated_charge = rated_charge
        self.rated_discharge = rated_discharge
        
        self.charge_efficiency = charge_efficiency
        self.discharge_efficiency = discharge_efficiency
        
        self.init_soc = init_soc
        self.curr_soc = init_soc
    
    def get_state(self):
        return self.curr_soc
    
    def reset(self):
        self.curr_soc = self.init_soc
    
    def step(self, action):
        curtailment, fossil = 0, 0
        if action >= 0:
            # charge
            charge_power = min(action, self.rated_charge)
            delta_soc = charge_power * self.charge_efficiency / self.max_capacity
            new_soc = self.curr_soc + delta_soc
            if new_soc >= 1:
                self.curr_soc = 1
                curtailment = (new_soc - 1) * self.max_capacity
            else:
                self.curr_soc = new_soc
        else:
            # discharge
            action = -action
            discharge_power = min(action, self.rated_discharge)
            delta_soc = discharge_power / self.discharge_efficiency / self.max_capacity
            new_soc = self.curr_soc - delta_soc
            if new_soc < self.min_soc:
                self.curr_soc = self.min_soc
                fossil = (self.min_soc - new_soc) * self.max_capacity * self.discharge_efficiency
            else:
                self.curr_soc = new_soc
            
        self._update_step()
        
        return curtailment, fossil
