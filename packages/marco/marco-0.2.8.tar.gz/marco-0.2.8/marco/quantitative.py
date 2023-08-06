"""
Quantitative table generation
"""

from math import ceil, log10
from numbers import Real
from typing import Dict, List, Tuple

from numpy import arange
from pandas import DataFrame, Series

from marco.frecuency_table import frecuency_table
from marco.grouped_frame import GroupedFrame
from marco.quantitative_frame import QuantitativeFrame
from marco.ungrouped_frame import UngroupedFrame

QuantitativeClass = List[Tuple[Real, Real]]


def quantitative_table(data: List[Real]) -> QuantitativeFrame:
    """Generate a QuantitativeFrame depending on the data size"""
    if len(data) > 20:
        return generate_grouped_table(data)
    return generate_ungrouped_table(sorted(data))


def generate_grouped_table(data: List[Real]) -> GroupedFrame:
    """Generates a GroupedFrame for data size more than 20 elements"""
    Ro = range_set(data)
    class_n = class_amount(len(data))
    fixed_data = apply_range_fix(data, Ro)
    interval_value = interval(Ro, class_n)
    q_class = quantitative_class(fixed_data, interval_value, class_n)
    mi = class_mark(q_class)
    ni = quantitative_absolute_frecuency(sorted(data), q_class)
    mi_x_ni = [a * b for a, b in zip(mi, ni.values())]

    relative_frecuency = [v / sum(ni.values()) for v in ni.values()]
    cumulative_relative = Series(relative_frecuency).cumsum()
    percentage_frequency = [i * 100 for i in relative_frecuency]

    return GroupedFrame(
        data,
        DataFrame(
            {
                "Clase": q_class,
                "mi": mi,
                "ni": ni.values(),
                "Ni": Series(ni.values()).cumsum().tolist(),
                "hi": relative_frecuency,
                "Hi": cumulative_relative,
                "%": percentage_frequency,
                "% acum": Series(percentage_frequency).cumsum().tolist(),
                "mi x ni": mi_x_ni,
            },
        ),
        interval_value
    )


def generate_ungrouped_table(data: List[Real]) -> UngroupedFrame:
    """
    Generates a UngroupedFrame for the quantitative varibles when data size is up to 20
    """
    return UngroupedFrame(data, frecuency_table(data))


def range_set(data: List[Real]) -> Real:
    """Compute range set of a list of elements"""
    return max(data) - min(data)


def class_amount(data_amount: int) -> int:
    """Compute class amount (k) of a data size"""
    return ceil(1 + 3.3 * log10(data_amount))


def interval(range_interval: Real, class_amount: int) -> int:
    """Compute how wide is a data size"""
    return ceil(range_interval / class_amount)


def quantitative_class(
    data: List[Real], interval: int, class_amount: int
) -> QuantitativeClass:
    """Generates the classes from grouped data"""
    tuples_list = []
    lower_limit = data[0]
    for _ in range(class_amount):
        upper_limit = lower_limit + interval
        tuples_list.append((lower_limit, upper_limit))
        lower_limit += interval

    return tuples_list


def class_mark(quantitative_class: QuantitativeClass) -> List[Real]:
    """Compute the class marks of each class in a quantitative class"""
    return [(q[0] + q[1]) / 2 for q in quantitative_class]


def fix_range(class_amount: int, interval: int, range_interval: Real) -> Real:
    """Get the fix range of a data size"""
    return (class_amount * interval - range_interval) / 2


def apply_range_fix(data: List[Real], range_interval: Real) -> List[Real]:
    """Get a new list with the corner elements' range fixed"""
    sorted_data = sorted(data)
    class_n = class_amount(len(data))
    interval_value = interval(range_interval, class_n)
    range_fix = fix_range(class_n, interval_value, range_interval)
    sorted_data[0] -= range_fix
    sorted_data[-1] += range_fix
    return sorted_data


def quantitative_absolute_frecuency(
    data: List[Real], q_class: QuantitativeClass
) -> Dict[str, int]:
    """Compute the absolute frecuency of a grouped data"""
    mapped = {str(clazz): 0 for clazz in q_class}
    i = j = 0

    while i < len(data):
        value = data[i]
        lower_limit = q_class[j][0]
        upper_limit = q_class[j][1]
        if value in arange(lower_limit, upper_limit, 0.5) or j >= len(q_class) - 1:
            mapped[str(q_class[j])] = mapped.get(str(q_class[j])) + 1
            i += 1
        else:
            if j < len(q_class) - 1:
                j += 1
    return mapped
