"""Includes the required modules and packages."""
import pyomo.environ as py
import numpy as np


def constraint_cover_total_monthly_demand(model, year, month):
    """
    Covering the total monthly demand of all n tenants within the building.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.
    year : Set
        Includes the year.
    month : Set
        Includes the month.

    Returns
    -------
    py.Constraint
        Foreach year and month.

    """
    return model.n * model.q_load[year, month] <= model.q_alt[year, month]


def constraint_cover_peak_demand(model, year, month):
    """
    Covering the peak demand of all n tenants within the building.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.
    year : Set
        Includes the year.
    month : Set
        Includes the month.

    Returns
    -------
    py.Constraint
        Foreach year and month.

    """
    return model.alpha[month] * model.q_alt[year, month] <= model.pi


def landlords_npv_equal_zero(model):
    """
    Set the landlord's net present value equal to zero.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.

    Returns
    -------
    py.Constraint
        A single constraint for the model.

    """
    _rev_rent = sum(
        (1 / (1 + model.i_l) ** (year - 2025)) * model.r[year, month] * model.a
        for year in model.set_years
        for month in model.set_months
    )
    _tenants = model.n * (model.c_con - _rev_rent)
    return -model.c_inv * model.pi + model.investment - _tenants == 0


def tenants_positive_npv(model):
    """
    Set the tenants' net present value (npv) equal to the initial one.

    The initial npv is calculated based on the annual initial spendings for
    living (rent) and energy. "_left" corresponds to the total costs of the
    alternative heating system and "_right" to those associated with the
    initial heating system.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.

    Returns
    -------
    py.Constraint
        A single constraint for the model.

    """
    _left = sum(
        (1 / (1 + model.i_t) ** (year - 2025))
        * (
            -(model.r_bar + model.r[year, month]) * model.a
            - model.q_load[year, month]
            * (
                model.p_alt[year, month]
                + model.factor_CO2[year, month] * model.p_CO2[year, month]
            )
            + model.heat_subsidy[year, month]
        )
        for year in model.set_years
        for month in model.set_months
    )

    _right = sum(
        (1 / (1 + model.i_t) ** (year - 2025))
        * (
            -model.r_bar * model.a
            - model.q_load[2025, month]
            * (model.p_init[2025, month] + 0.00022 * model.p_CO2[2025, month])
        )
        for year in model.set_years
        for month in model.set_months
    )
    return _left == _right


def governances_grant_subsidy_parity(model):
    """
    Set the parity between the landlord's and tenants' subsidies/grants.

    "Investment grants + rent-related revenues" == "heating costs subsidies"

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.

    Returns
    -------
    py.Constraint
        A single constraint for the model.

    """
    return (
        model.investment
        + sum(
            (1 / (1 + model.i_g) ** (year - 2025))
            * model.r[year, month]
            * model.a
            * model.n
            for year in model.set_years
            for month in model.set_months
        )
        == model.subsidy
    )


def set_upper_bound_to_max_inv_costs(model):
    """
    Set upper bound of the total investment grants.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.

    Returns
    -------
    py.Constraint
        A single constraint for the model.

    """
    return (
        model.investment
        <= model.n * model.c_con + model.peak * model.alpha[1] * model.c_inv
    )


def landlords_rent_revenues(model):
    """
    Calculate landlord's rent-related revenues.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.

    Returns
    -------
    py.Constraint
        A single constraint for the model.

    """
    return model.rent_revenues == sum(
        (1 / (1 + model.i_l) ** (year - 2025))
        * model.r[year, month]
        * model.a
        * model.n
        for year in model.set_years
        for month in model.set_months
    )


def constant_subsidy_per_year(model, year, month):
    """
    Set constant subsidy per month within a single year.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.
    year : py.Set
        Includes the year.
    month : py.Set
        Includes the month.

    Returns
    -------
    py.Constraint
        A single constraint for the model.

    """
    if month == 1:
        return model.heat_subsidy[year, month] == model.heat_subsidy[year, 12]
    else:
        return model.heat_subsidy[year, month] == model.heat_subsidy[year, month - 1]


def upper_bound_for_annual_tenants_costs(model, year):
    """
    Set constant subsidy per month within a single year.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.
    year : py.Set
        Includes the year.
    month : py.Set
        Includes the month.

    Returns
    -------
    py.Constraint
        A single constraint for the model.

    """
    annual_rent_spendings = model.r_bar * model.a * 12
    annual_energy_spendings = sum(
        model.q_load[2025, month]
        * (model.p_init[2025, month] + 0.00022 * model.p_CO2[2025, month])
        for month in model.set_months
    )
    annual_initial_spendings = annual_rent_spendings + annual_energy_spendings

    annual_decarbonized_costs = sum(
        (model.r_bar + model.r[year, month]) * model.a
        + model.q_load[year, month]
        * (
            model.p_alt[year, month]
            + model.factor_CO2[year, month] * model.p_CO2[year, month]
        )
        - model.heat_subsidy[year, month]
        for month in model.set_months
    )

    return annual_decarbonized_costs <= 1.5 * annual_initial_spendings


def subsidy_rent_costs_increase(model, year, month):
    """
    Set lower bound of monthly heating costs subsidies.

    This constraint ensures that at least the heat subsidies cover the
    rent-related spendings of the tenants.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.
    year : py.Set
        Includes the year.
    month : py.Set
        Includes the month.

    Returns
    -------
    py.Constraint
        Foreach year and month.

    """
    return model.heat_subsidy[year, month] >= model.r[year, month] * model.a


def set_total_rent_per_month(model, y, m):
    return model.total_rent[y, m] == model.r_bar + model.r[y, m]


def constant_total_rent_per_year(model, year, month):
    if month == 1:
        return model.total_rent[year, month] == model.total_rent[year, 12]
    else:
        return model.total_rent[year, month] == model.total_rent[year, month - 1]


def constant_total_rent_within_two_years_and_maximum_increase(model, year, month):
    if np.mod(year, 2) == 0:
        return model.total_rent[year, month] == model.total_rent[year - 1, month]
    else:
        if year == 2025:
            return model.total_rent[year, month] <= 1.1 * model.r_bar
        else:
            return (
                model.total_rent[year, month]
                <= 1.1 * model.total_rent[year - 1, month]
            )


def increase_total_rent(model, year):
    """
    Increasing total rent per square metre.

    Parameters
    ----------
    model : py.ConcreteModel
        Includes the pyomo model instance.
    year : Set
        Includes the year.

    Returns
    -------
    py.Constraint
        Includes the constraint.

    """
    if year != 2025:
        return model.total_rent[year, 1] >= model.total_rent[year - 1, 1]
    else:
        return py.Constraint.Skip


def add_constraints_to_model(model=None):

    model.con1_cover_demand = py.Constraint(
        model.set_years, model.set_months, rule=constraint_cover_total_monthly_demand
    )
    model.con2_cover_peak_demand = py.Constraint(
        model.set_years, model.set_months, rule=constraint_cover_peak_demand
    )

    model.con3_landlord_zero_npv = py.Constraint(rule=landlords_npv_equal_zero)

    model.con4_tenants_profitability = py.Constraint(rule=tenants_positive_npv)

    model.con5_governance_equality = py.Constraint(
        rule=governances_grant_subsidy_parity
    )

    model.con6_upper_bound_for_inv_grants = py.Constraint(
        rule=set_upper_bound_to_max_inv_costs
    )

    model.con7_sum_up_landlords_rent_revenues = py.Constraint(
        rule=landlords_rent_revenues
    )

    model.con8_constant_subsidy_within_year = py.Constraint(
        model.set_years, model.set_months, rule=constant_subsidy_per_year
    )

    model.con9_limit_annual_decarbonized_spendings = py.Constraint(
        model.set_years, rule=upper_bound_for_annual_tenants_costs
    )

    model.con10_limit_lower_bound_of_subsidies = py.Constraint(
        model.set_years, model.set_months, rule=subsidy_rent_costs_increase
    )

    model.con11_define_monthly_total_rent = py.Constraint(
        model.set_years, model.set_months, rule=set_total_rent_per_month
    )

    model.con12_constant_total_rent_within_year = py.Constraint(
        model.set_years, model.set_months, rule=constant_total_rent_per_year
    )

    model.con13_con_rent_over_two_years = py.Constraint(
        model.set_years,
        model.set_months,
        rule=constant_total_rent_within_two_years_and_maximum_increase,
    )

    model.con14_increase_total_rent = py.Constraint(
        model.set_years, rule=increase_total_rent
    )

    return model
