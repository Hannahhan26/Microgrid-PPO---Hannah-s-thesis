
from .base import Agent


# class NaiveAgent(Agent):
#     def __init__(self, rated_charge, rated_discharge, rated_soel, rated_sofc):
#         self.rated_charge = rated_charge
#         self.rated_discharge = rated_discharge
#         self.rated_soel = rated_soel
#         self.rated_sofc = rated_sofc

#     def action(self, state):
#         # 优先电池充电/放电，然后燃料电池电解/放电
#         hour_of_day, p_demand, price_elec, p_pv, p_wt, soc_battery, soc_fc = state
#         p_battery, p_fc = 0, 0        
#         p_renewable = p_pv + p_wt
#         delta = p_renewable - p_demand
#         if delta > 0:
#             if soc_battery >= 1:
#                 p_battery = 0
#                 p_fc = min(delta, self.rated_soel)
#             else:
#                 if delta >= self.rated_charge:
#                     p_battery = self.rated_charge
#                     p_fc = min(delta - self.rated_charge, self.rated_soel)
#                 else:
#                     p_battery = delta
#                     p_fc = 0
#         else:
#             delta = -delta
#             if soc_battery > 0.2:
#                 if delta > self.rated_discharge:
#                     p_battery = -self.rated_discharge
#                     p_fc = -min(delta - self.rated_discharge, self.rated_sofc)
#                 else:
#                     p_battery = -delta
#                     p_fc = 0
#             else:
#                 p_battery = 0
#                 if soc_fc > 0:
#                     p_fc = -min(delta, self.rated_sofc)
#                 else:
#                     p_fc = 0

#         return p_battery, p_fc


class NaiveAgent(Agent):
    def __init__(self, rated_charge, rated_discharge, rated_soel, rated_sofc):
        self.rated_charge = rated_charge
        self.rated_discharge = rated_discharge
        self.rated_soel = rated_soel
        self.rated_sofc = rated_sofc

    def action(self, state):
        # 优先电池充电/放电，然后燃料电池电解/放电
        hour_of_day, p_demand, price_elec, p_pv, p_wt, soc_battery, soc_fc = state
        p_battery, p_fc = 0, 0        
        p_renewable = p_pv + p_wt
        delta = p_renewable - p_demand
        if delta > 0:
            if delta >= self.rated_charge:
                p_battery = self.rated_charge
                p_fc = min(delta - self.rated_charge, self.rated_soel)
            else:
                p_battery = delta
                p_fc = 0
        else:
            delta = -delta
            if delta > self.rated_discharge:
                p_battery = -self.rated_discharge
                p_fc = -min(delta - self.rated_discharge, self.rated_sofc)
            else:
                p_battery = -delta
                p_fc = 0

        return p_battery, p_fc
