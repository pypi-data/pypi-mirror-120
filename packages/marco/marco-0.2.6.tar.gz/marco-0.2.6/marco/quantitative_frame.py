"""Quantitative frame abstract class"""
from abc import ABCMeta, abstractmethod
from numbers import Real
from typing import List, Tuple

from pandas import DataFrame, Series
from six import add_metaclass


@add_metaclass(ABCMeta)
class QuantitativeFrame:
    """
    Quantitative Frame
    """

    def __init__(self, data: List[Real], dataframe: DataFrame) -> None:
        self.data = data
        self.dataframe = dataframe
        self._median_index: int = None
        self._trend_index: int = None

    def _find_trend_row(self) -> Tuple[int, Series]:
        index = self._trend_index = self.dataframe["ni"].argmax()
        return (index, self.dataframe.iloc[self._trend_index])

    @abstractmethod
    def arithmetic_mean(self) -> Real:
        """ """

    @abstractmethod
    def median(self) -> Real:
        """ """

    @abstractmethod
    def trend(self) -> Real:
        """ """

    @abstractmethod
    def median_row(self) -> DataFrame:
        """ """

    @abstractmethod
    def trend_row(self) -> DataFrame:
        """ """

    @abstractmethod
    def quantile(self) -> Series:
        """ """

    @abstractmethod
    def percentile(self, k: List[int]) -> List[Real]:
        """ """

    @abstractmethod
    def decile(self, k: List[int]) -> List[Real]:
        """ """
