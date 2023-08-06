from math import floor, modf
from numbers import Real
from typing import List

from pandas import DataFrame
from pandas.core.series import Series
from numpy import mean, median

from marco.quantitative_frame import QuantitativeFrame


class UngroupedFrame(QuantitativeFrame):
    """Quantitative ungrouped data entity"""

    def arithmetic_mean(self) -> Real:
        return mean(self.data)

    def median(self) -> Real:
        return median(self.data)

    def trend(self) -> Real:
        _, row = self._find_trend_row()
        return row["Clase"]

    def median_row(self) -> Series:
        middle = self.median()
        index = floor(len(self.dataframe) / 2)
        if len(self.dataframe) % 2 != 0:
            index = next(
                i for i, row in self.dataframe.iterrows() if row["Clase"] == middle
            )
        return self.dataframe.iloc[[index]]

    def trend_row(self) -> DataFrame:
        (index, _) = self._find_trend_row()
        return self.dataframe.iloc[[index]]

    def quantile(self) -> Series:
        return Series(self.data).quantile([.25, .5, .75])

    def _dispersion_bias_of(self, k: int, divisor: int) -> Real:
        n = len(self.data)
        frac, whole = modf((k * (n + 1)) / divisor)
        position = floor(whole)
        if position >= n:
            return self.data[n - 1]
        coeficient = (self.data[position + 1] - self.data[position]) * frac
        return self.data[position] + coeficient

    def decile(self, k: int) -> List[Real]:
        return [self._dispersion_bias_of(element, 10) for element in k]

    def percentile(self, k: List[int]) -> List[Real]:
        return [self._dispersion_bias_of(element, 100) for element in k]
