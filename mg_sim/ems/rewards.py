
import numpy as np


# def cal_yc(p_pv, p_wt, p_battery, p_fc, p_cur):
#     p_battery = - p_battery if p_battery < 0 else 0
#     p_fc = - p_fc if p_fc < 0 else 0
    
#     yc = p_cur / (p_pv + p_wt + p_battery + p_fc)
    
#     return yc


def cal_yc(p_pv, p_wt, p_battery, p_fc, p_cur):
    p_battery = - p_battery if p_battery < 0 else 0
    p_fc = - p_fc if p_fc < 0 else 0
    
    yc = p_cur / (p_pv + p_wt + p_battery + p_fc)
    
    return min(1, yc)


def cal_yf(p_pv, p_wt, p_battery, p_fc, p_fossil):
    p_battery = - p_battery if p_battery < 0 else 0
    p_fc = - p_fc if p_fc < 0 else 0
    
    y_f = p_fossil / (p_fossil + p_pv + p_wt + p_battery + p_fc)
    
    return y_f


def reward_1(yc, yf, b11=0.1, w11=2, w12=1):
    reward = - w11 * yc - w12 * yf
    if yc == 0:
        reward += b11
    return reward


def reward_2(rev, w21=1000):
    reward = w21 * rev
    return reward


def reward_3(soc_battery_flag):
    reward = -1 if soc_battery_flag is True else 0
    return reward


def reward_4(soc_fc_flag):
    reward = -1 if soc_fc_flag is True else 0
    return reward
