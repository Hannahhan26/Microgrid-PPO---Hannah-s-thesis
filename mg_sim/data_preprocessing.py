
import os
import sys
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt


script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)


# 读取 价格数据
price_sheets_dict = pd.read_excel(os.path.join(script_dir, "data/prices.xlsx"), sheet_name=None, names=["price"], header=None)

def prices_trans(x: str):
    x = x.split(",")
    integer_part = "".join(x[0:-1])
    decimal_part = x[-1]
    total_str = ".".join([integer_part, decimal_part])
    return float(total_str)

for sheet_name in ["summer", "autumn", "winter", "spring"]:
    price_sheets_dict[sheet_name]["price"] = price_sheets_dict[sheet_name]["price"].apply(lambda x: prices_trans(x))
    price_sheets_dict[sheet_name]["price"] /= 1000
    price_sheets_dict[sheet_name] = price_sheets_dict[sheet_name].reset_index().rename(columns={"index": "hour_of_day"})
    price_sheets_dict[sheet_name]["hour_of_day"] = price_sheets_dict[sheet_name]["hour_of_day"].apply(lambda x: x%24)
    price_sheets_dict[sheet_name].to_excel(f"./data/prices_{sheet_name}.xlsx", index=False)


# 读取 需求数据
demands_sheets_dict = pd.read_excel(os.path.join(script_dir, "data/demands.xlsx"), sheet_name=None, names=["demand"])

for sheet_name in ["summer", "autumn", "winter", "spring"]:
    demands_sheets_dict[sheet_name] = demands_sheets_dict[sheet_name].reset_index().rename(columns={"index": "hour_of_day"})
    demands_sheets_dict[sheet_name]["hour_of_day"] = demands_sheets_dict[sheet_name]["hour_of_day"].apply(lambda x: x%24)
    demands_sheets_dict[sheet_name].to_excel(f"./data/demands_{sheet_name}.xlsx", index=False)


# 读取 新能源数据
renewable_sheets_dict = pd.read_excel(os.path.join(script_dir, "data/renewable.xlsx"), sheet_name=None, parse_dates=["timestamp"])
for sheet_name in ["summer", "autumn", "winter", "spring"]:
    renewable_sheets_dict[sheet_name]["timestamp"] = renewable_sheets_dict[sheet_name]["timestamp"].dt.tz_localize(None)
    renewable_sheets_dict[sheet_name]["hour_of_day"] = renewable_sheets_dict[sheet_name]["timestamp"].dt.hour
    renewable_sheets_dict[sheet_name].rename(columns={"pv / kw": "pv", "wt / kw": "wt"}, inplace=True)
    renewable_sheets_dict[sheet_name].to_excel(f"./data/renewable_{sheet_name}.xlsx", index=False)
