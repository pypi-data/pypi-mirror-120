from typing import Dict, List, Union

from pandas import DataFrame
from marco.frecuency_table import frecuency_table


def categorical_table(data: Union[List, Dict]) -> DataFrame:
    """
    Generate a dataframe with the required fields for a
    frecuency table of categorical variables
    """
    return frecuency_table(data)
