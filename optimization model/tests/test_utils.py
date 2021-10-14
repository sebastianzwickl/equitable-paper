import pyam
import pandas as pd
import numpy as np

from utils import set_and_index


def _create_gen_iamdf():

    _TEST_DF = pd.DataFrame(
        [
            ["model_a", "scen_a", "Europe", "Hydrogen", "TWh", 3,1],
            ["model_a", "scen_a", "Europe", "Hydrogen", "TWh", 2,2],
        ],
        columns=["model", "scenario", "region", "variable", "unit", 2050, "month"],
    )
    _df = pyam.IamDataFrame(_TEST_DF)
    return _df


def test_validate_input_data():
    _gen = _create_gen_iamdf()
    Year, Month = set_and_index(_gen)
    
    assert (Year == [2050]) & np.array_equal(Month, [1,2])
