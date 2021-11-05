import pyomo.environ as py


def set_and_index(data=None):

    """

    Parameters
    ----------
    data : IamDataFrame, required
        Includes the temporal resolved time series input data. The default is None.

    Returns
    -------
    Year : Includes a list containing the years.
    Month : Includes a list containing the months.

    """

    Year = data.year
    Month = list(data.data["month"].unique())

    return Year, Month


# def init_spot(m, t):
#     return m.time["Spot"][t]


def create_and_initialize_the_model(sets=None, cop=None):

    """

    Parameters
    ----------
    Sets : Tuple, required
        Includes the index for years and months. The default is None.

    Returns
    -------
    m : PyomoModel.ConcreteModel
        Includes the model instance.

    """

    m = py.ConcreteModel()
    m.name = "MOJET"
    m.set_years = py.Set(initialize=sets[0])
    m.set_init_year = py.Set(initialize=[min(sets[0])])
    m.set_months = py.Set(initialize=sets[1])
    m.cop = cop
    return m


def add_input_values_to_model(model=None, df=None, alternative=None):

    """

    Parameters
    ----------
    model : PyomoModel.ConcreteModel
        Includes the model and set/index information only.
    df : IamDataFrame, required
        Includes the input values (that are not higher temporal resolved, i.e., a single value per year).
        The default is None.
    alternative : String, Required
        Defines the alternative heating system. The default is None.

    Returns
    -------
    model : PyomoModel.ConcreteModel
        ConceteteModel with added parameters.

    """

    model.n = py.Param(
        initialize=float(df.filter(variable="Number of tenants").data["value"][0]),
    )

    model.i_g = py.Param(
        initialize=float(
            df.filter(variable="Interest rate|governance").data["value"][0]
        ),
    )
    model.i_l = py.Param(
        initialize=df.filter(variable="Interest rate|landlord").data["value"][0],
    )
    model.i_t = py.Param(
        initialize=df.filter(variable="Interest rate|tenant").data["value"][0],
    )

    model.c_inv = py.Param(
        initialize=df.filter(
            variable="Heat system alternative|" + alternative + "|Investment costs"
        ).data["value"][0],
    )
    model.c_con = py.Param(
        initialize=df.filter(
            variable="Heat system alternative|" + alternative + "|Construction costs"
        ).data["value"][0],
    )

    model.r_bar = py.Param(
        initialize=df.filter(variable="Initial rent price").data["value"][0],
    )
    model.a = py.Param(
        initialize=df.filter(variable="Rented area").data["value"][0],
    )

    return model


def init_load(m, t, month):
    return float(
        m.df_time.filter(variable="Demand|Heat", year=2025, month=month)
        .data["value"]
        .values
    )


def init_peak_demand(m):
    """
    Set the peak demand of the building.

    Parameters
    ----------
    m : py.ConcreteModel
        Instance of the pyomo model.

    Returns
    -------
    float
        The max heat demand value.

    """
    return float(max(
        m.df_time.filter(variable="Demand|Heat", year=2025)
        .data["value"]
        .values
    ))




def init_load_factor(model, month):
    return float(
        model.df_time.filter(variable="Load factor|Heat", year=2025, month=month)
        .data["value"]
        .values
    )


def init_CO2_price(model, year, month):
    return float(
        model.df_time.filter(
            variable="Price|CO2", year=year, month=month, scenario=model.scenario
        )
        .data["value"]
        .values
    )


def init_p_init(model, year, month):
    return float(
        model.df_time.filter(variable="Price|Natural gas", year=year, month=month)
        .data["value"]
        .values
    )


def init_p_dh(model, year, month):
    return float(
        model.df_time.filter(variable="Price|District heating", year=year, month=month)
        .data["value"]
        .values
    )


def init_p_hp(model, year, month):
    return float(
        model.df_time.filter(
            variable="Price|Heat pump|Electricity", year=year, month=month
        )
        .data["value"]
        .values / model.cop
    )


def init_specific_dh_emissions(model, year, month):
    return float(
        model.df_time.filter(
            variable="Emissions|District heating", year=year, month=month
        )
        .data["value"]
        .values
    )


def init_specific_elec_emissions(model, year, month):
    return float(
        model.df_time.filter(
            variable="Emissions|Heat pump|Electricity", year=year, month=month
        )
        .data["value"]
        .values / model.cop
    )


def add_time_series_inputs_to_model(model=None, alternative=None, scenario=None):

    """

    Parameters
    ----------
    model : PyomoModel.ConcreteModel
        Includes the model and set/index information only.
    alternative : String, required
        Defines the alternative heating system. The default is None.
    scenario : String, required
        Defines the scenario and thus the CO2 price of the analysis.

    Returns
    -------
    model : TYPE
        ConcreteModel with added time-series information.

    """

    model.scenario = scenario

    model.q_load = py.Param(
        model.set_years, model.set_months, initialize=init_load, within=py.Reals
    )

    model.peak = py.Param(initialize=init_peak_demand, within=py.Reals)

    model.alpha = py.Param(
        model.set_months, initialize=init_load_factor, within=py.Reals
    )
    model.p_CO2 = py.Param(
        model.set_years * model.set_months, initialize=init_CO2_price, within=py.Reals
    )
    model.p_init = py.Param(
        model.set_years * model.set_months, initialize=init_p_init, within=py.Reals
    )
    if alternative == "District heating":
        _func = init_p_dh
        _func2 = init_specific_dh_emissions
    else:
        _func = init_p_hp
        _func2 = init_specific_elec_emissions

    model.p_alt = py.Param(
        model.set_years * model.set_months, initialize=_func, within=py.Reals
    )
    model.factor_CO2 = py.Param(
        model.set_years * model.set_months, initialize=_func2, within=py.Reals
    )

    return model


def add_decision_variables(m):

    m.investment = py.Var(domain=py.NonNegativeReals)
    m.subsidy = py.Var(domain=py.NonNegativeReals)
    m.pi = py.Var(domain=py.NonNegativeReals)
    m.heat_subsidy = py.Var(m.set_years, m.set_months,
                            domain=py.NonNegativeReals)
    m.q_alt = py.Var(m.set_years, m.set_months, domain=py.NonNegativeReals)
    m.r = py.Var(m.set_years, m.set_months, domain=py.NonNegativeReals)
    m.rent_revenues = py.Var(domain=py.NonNegativeReals)
    m.total_rent = py.Var(m.set_years, m.set_months,
                          domain=py.NonNegativeReals)

    return m


def tenant_subsidies(model, year):
    _val = sum(
        (model.n / ((1 + model.i_g) ** (y - year))) * model.heat_subsidy[y, m]
        for y in model.set_years
        for m in model.set_months
    )
    return model.subsidy == _val


def objective_function_maximize_revenues(m):
    """Model's objective function minimizing governance's net present value."""
    return m.investment + m.subsidy


def add_objective_function(m):
    """
    Includes the objective function of the model.

    Parameters
    ----------
    m : pyomo.ConcreteModel
        The model instance.

    Returns
    -------
    m : pyomo.ConcreteModel
        The concrete modele instance with objective function added.

    """
    # This constraint calculates the total tentants-related subsidies
    # (see 'def tenant_subsidies' above)
    m.tenant_subsidy = py.Constraint(m.set_init_year, rule=tenant_subsidies)

    # Below, the objective function (cost-minimizing) is defined
    m.objective = py.Objective(
        expr=objective_function_maximize_revenues(m), sense=py.minimize
    )
    return m
