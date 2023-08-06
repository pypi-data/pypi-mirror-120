from typing import Any, Dict, List, Union
from pandas.core.frame import DataFrame
from pandas.core.series import Series


def frecuency_table(data: Union[List, Dict]) -> DataFrame:
    """
    Generate a dataframe with the required fields for a frecuency table
    """
    mapped_data = data
    if isinstance(data, list):
        mapped_data = map_frecuency_data(sorted(data))

    cumulative_absolute = Series(mapped_data.values()).cumsum()
    relative_frecuency = [v / sum(mapped_data.values()) for v in mapped_data.values()]
    cumulative_relative = Series(relative_frecuency).cumsum()
    percentage_frequency = [i * 100 for i in relative_frecuency]

    return DataFrame(
        {
            "Clase": mapped_data.keys(),
            "ni": mapped_data.values(),
            "Ni": cumulative_absolute.tolist(),
            "hi": relative_frecuency,
            "Hi": cumulative_relative.tolist(),
            "%": percentage_frequency,
            "% acum": Series(percentage_frequency).cumsum().tolist(),
        }
    )

def map_frecuency_data(data: List[Any]) -> Dict[Any, int]:
    """Counts the absolute frecuency of a data"""
    mapped = {}
    for element in data:
        mapped[element] = mapped.get(element, 0) + 1
    return mapped

