"""Import modules and further requirements."""
import pyam
import utils
import pyomo.environ as py
import os
import numpy as np
import MOJET_write_res_to_iamc as write
from datetime import datetime
import MOJET_constraints as Con
from pathlib import Path

_data_folder = Path("data")
# _data_folder = Path("validation")

_alt = "District heating"
# _alt = "Heat pump"

_scenario = "Directed Transition"
# _scenario = "Societal Commitment"
# _scenario = "Gradual Development"
# _scenario = "Low CO2 price"

if _scenario == "Gradual Development":
    _df_time = pyam.IamDataFrame(
        _data_folder / "_input-time-series_GD_2050.xlsx")
if _scenario == "Low CO2 price":
    _df_time = pyam.IamDataFrame(
        _data_folder / "_input-time-series_LOW.xlsx")
if _scenario in ["Societal Commitment", "Directed Transition"]:
    _df_time = pyam.IamDataFrame(
        _data_folder / "input-time-series.xlsx")

_df_val = pyam.IamDataFrame(_data_folder / "input-values.xlsx")


"""Sensitivity analysis"""
sens = tuple([False, "10%"])
if sens[0] is True:
    _df_val = pyam.IamDataFrame(_data_folder / "input-values_10%.xlsx")
    _df_time = pyam.IamDataFrame(_data_folder / "input-time-series_10%.xlsx")


_sets = utils.set_and_index(_df_time)

cop = 2.5
model = utils.create_and_initialize_the_model(_sets, cop=cop)
model = utils.add_input_values_to_model(model, _df_val, _alt)

model.df_time = _df_time
model = utils.add_time_series_inputs_to_model(model, _alt, _scenario)

# add decision variables
model = utils.add_decision_variables(model)
model = utils.add_objective_function(model)

model = Con.add_constraints_to_model(model)


"""
DEACTIVATE CONSTRAINTS HERE IF NECESSARY.
"""
# print(model.con9_limit_annual_decarbonized_spendings[2025].expr)
# model.con9_limit_annual_decarbonized_spendings.deactivate()
# model.con13_con_rent_over_two_years.deactivate()
model.con10_limit_lower_bound_of_subsidies.deactivate()
# model.con13_con_rent_over_two_years.deactivate()
# model.con14_increase_total_rent.deactivate()
"""
SOLVING THE MODEL
"""


solver = py.SolverFactory("gurobi")
solution = solver.solve(model)

print("\n****************************")
print("Objective function value:", int(model.objective()))
print("Installed capacity:", float(model.pi()))

print("Landlord's investment grant:",
      float(np.round(model.investment(), decimals=0)))
print("Tenant's heating costs subsidy:",
      float(np.round(model.subsidy(), decimals=0)))


print("Landlord's rent revenues:",
      float(np.round(model.rent_revenues(), decimals=0)))

for i in range(2025, 2041, 1):
    _val = sum(
        model.heat_subsidy[i, m]()
        for m in model.set_months
        )
    print(np.round(_val, decimals=1))

for i in range(2025, 2041, 1):
    print(np.round(model.r[i, 1](), decimals=4))


_now = datetime.now().strftime("%Y%m%dT%H%M")
if sens[0] is True:
    _results_name = _alt + " " + _scenario + sens[1] + str(cop)
else:
    _results_name = _alt + " " + _scenario
result_dir = os.path.join("result", "{}-{}".format(_results_name, _now))
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

write.write_results_to_ext_iamc_format(model, result_dir)

model.con4_tenants_profitability.display()

# print(model.con4_tenants_profitability.expr)
