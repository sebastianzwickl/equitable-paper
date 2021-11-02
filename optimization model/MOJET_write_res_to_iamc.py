import pandas as pd
import numpy as np
import pyomo.environ as py
import os
# import NoCopHH_mod_plot_IAMC as plot_IAMC


def write_IAMC(output_df, model, scenario, region, variable, unit, time, values):

    if isinstance(values, list):
        _df = pd.DataFrame(
            {
                "model": model,
                "scenario": scenario,
                "region": region,
                "variable": variable,
                "unit": unit,
                "year": time,
                "value": values,
            }
        )
    else:
        _df = pd.DataFrame(
            {
                "model": model,
                "scenario": scenario,
                "region": region,
                "variable": variable,
                "unit": unit,
                "year": time,
                "value": values,
            },
            index=[0],
        )

    output_df = output_df.append(_df)
    return output_df


def write_results_to_ext_iamc_format(m, res_dir):
    
    
    
    output_iamc = pd.DataFrame()
    
    _region = "Multi-Apartment building"
    _unit = "EUR"
    _time = 2025

    # Spot markt revenues
    _value = np.around(py.value(m.investment), 2)
    output_iamc = write_IAMC(
        output_iamc, m.name, m.scenario, _region, "Landlord's investment grant", _unit, _time, _value
    )
    
    _time = [_t for _t in m.set_years]
    _value = []
    for year in m.set_years:
        _value.append(sum(
            np.around(py.value(m.heat_subsidy[year, month]), 0)
            for month in m.set_months
            )
        )
    output_iamc = write_IAMC(
        output_iamc, m.name, m.scenario, _region,
        "Annual tenants' heating cost subsidy", _unit, _time, _value)

    _value = []
    for year in m.set_years:
        _value.append(np.around(py.value(m.r[year, 1]), 2))
    output_iamc = write_IAMC(
        output_iamc, m.name, m.scenario, _region,
        "Monthly rent charge adjustment", r'EUR / m ** 2', _time, _value
    )

    _value = []
    for year in m.set_years:
        _val_1 = sum(py.value(m.heat_subsidy[year, month])
                              for month in m.set_months)
        _val_2 = sum(py.value(m.q_load[year, month])
                              for month in m.set_months)
        _value.append(np.around(_val_1/_val_2, 5))

    output_iamc = write_IAMC(
        output_iamc, m.name, m.scenario, _region,
        "Specific heating costs subsidy payment", r'EUR / kWh', _time, _value)

    _value = np.around(py.value(m.objective), 0)
    output_iamc = write_IAMC(
        output_iamc, m.name, m.scenario, _region,
        "Objective value", _unit, 2025, _value
    )
    
    _value = np.around(py.value(m.investment) / py.value(m.pi), 1)
    output_iamc = write_IAMC(
        output_iamc, m.name, m.scenario, _region,
        "Specific investment grant", r'EUR / kW', 2025, _value
    )

    output_iamc.to_excel(os.path.join(res_dir, "model-values.xlsx"),
                         index=False)

    # _unit = "MWh"
    
    # output_iamc = pd.DataFrame()

    # # Quantity future
    
    # # Quantity day-ahead
    # _value = []
    # for _t in m.set_time:
    #     _value.append(np.around(py.value(m.v_q_spot[_t]), 0))
    # output_iamc = write_IAMC(
    #     output_iamc, _model, _scenario, _region, "Day-Ahead", _unit, _time, _value
    # )
    # # Quantity hydrogen
    # _value = []
    # for _t in m.set_time:
    #     _value.append(np.around(py.value(m.v_q_H2[_t]), 0))
    # output_iamc = write_IAMC(
    #     output_iamc, _model, _scenario, _region, "Hydrogen", _unit, _time, _value
    # )

    # output_iamc.to_excel(os.path.join(res_dir, "IAMC_hourly.xlsx"), index=False)

    # _value = []
    # for _t in m.set_time:
    #     _value.append(np.around(py.value(m.v_q_fossil[_t]), 0))
    # output_iamc = write_IAMC(
    #     output_iamc, _model, _scenario, _region, "Conventional", _unit, _time, _value
    # )

    # output_iamc.to_excel(os.path.join(res_dir, "IAMC_supply.xlsx"), index=False)

    # plot_IAMC.plot_results(res_dir)

    # # Write shadow price and projecte shadow price to result file
    # output_iamc = pd.DataFrame()
    # _value = []
    # for _t in m.set_time:
    #     _value.append(np.around(-py.value(m.dual_lambda_load[_t]), 2))
    # output_iamc = write_IAMC(
    #     output_iamc, _model, _scenario, _region, "Shadow price", _unit, _time, _value
    # )

    # output_iamc.to_excel(
    #     os.path.join(res_dir, "IAMC_Profitability_Gap.xlsx"), index=False
    # )
