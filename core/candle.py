import numpy as np
import pandas as pd
from dataclasses import dataclass
from datetime import datetime
from scipy import stats


@dataclass
class CandleElement:
    date: datetime
    value: float


@dataclass
class Candle:
    size: int
    elements: list
    metrics: dict()

    def add(self, element):
        """Add element"""
        self.elements.append(element)
        self.execute_metrics()

    def execute_metrics(self):
        """Execute metrics"""
        for name, metric in self.metrics:
            metric(self.elements)

    def get_value(self, name):
        """Return metric value"""

    #     self._count += 1
    #     # update low
    #     try:
    #         if element.value < self.low.value:
    #             self.low = element
    #         elif self.high.value < element.value:
    #             self.high = element
    #     except AttributeError:
    #         if len(self._elements) == 1:
    #             self._low = element
    #             self._high = element
    #             self._open = element
    #             self._close = element
    #     # update close
    #     self._close = element
    #     # update sum
    #     self._sum += element.value
    #     # update mean
    #     self._mean = self._sum / self._count
    #     # sum stddev
    #     self._sum_std += (element.value - self._mean) ** 2
    #     # var
    #     self._var = self._sum_std / self._count
    #     # std
    #     self._std = self._var ** 0.5
    #     # diff
    #     try:
    #         self._diff.append(self._elements[-1].value - self._elements[-2].value)
    #     except IndexError:
    #         pass
    #
    # def __init__(self, size, pip=None):
    #     self._elements = []
    #     self._size = size
    #     self._pip = pip
    #     self._close = None
    #     self._open = None
    #     self._high = None
    #     self._low = None
    #     self._sum = 0
    #     self._std = None
    #     self._sum_std = 0
    #     self._std = None
    #     self._var = None
    #     self._mean = None
    #     self._count = 0
    #     self._closed = False
    #     self._diff = []
    #
    # def is_bullish(self):
    #     """
    #     Is candle going up
    #     :return:
    #     """
    #     return self._open.value < self._close.value
    #
    # def is_bearish(self):
    #     """
    #     Is candle going down
    #     :return:
    #     """
    #     return self._open.value > self._close.value
    #
    # def __str__(self):
    #     """
    #     Str
    #     :return:
    #     """
    #     return str(self.get_value())
    #
    # def _process_price(self, element):
    #     """
    #     Process price
    #     :return:
    #     """
    #     # add price
    #     self._elements.append(element)
    #     # increment count
    #     self._count += 1
    #     # update low
    #     try:
    #         if element.value < self.low.value:
    #             self.low = element
    #         elif self.high.value < element.value:
    #             self.high = element
    #     except AttributeError:
    #         if len(self._elements) == 1:
    #             self._low = element
    #             self._high = element
    #             self._open = element
    #             self._close = element
    #     # update close
    #     self._close = element
    #     # update sum
    #     self._sum += element.value
    #     # update mean
    #     self._mean = self._sum / self._count
    #     # sum stddev
    #     self._sum_std += (element.value - self._mean) ** 2
    #     # var
    #     self._var = self._sum_std / self._count
    #     # std
    #     self._std = self._var ** 0.5
    #     # diff
    #     try:
    #         self._diff.append(self._elements[-1].value - self._elements[-2].value)
    #     except IndexError:
    #         pass
    #
    # def __repr__(self):
    #     """
    #     Repr
    #     :return:
    #     """
    #     return str(self.get_value())
    #
    # def get_value(self):
    #     """
    #     Get value
    #     :return:
    #     """
    #     return dict(open=self._open.value, close=self._close.value, high=self._high.value, low=self._low.value,
    #                 change=self.change, elapse_time=self.elapse_time,
    #                 change_perc=self.pct_change, profit_pips=self.profit_pips, pivot=self.pivot['Pivot'],
    #                 s1=self.pivot['S1'], s2=self.pivot['S2'], r1=self.pivot['R1'], r2=self.pivot['R2'])
    #
    # def get_size(self):
    #     """
    #     Get size
    #     :return:
    #     """
    #     return len(self._elements)
    #
    # @property
    # def profit_pips(self):
    #     if self._pip is not None:
    #         return self.change / self._pip
    #
    # @property
    # def value(self):
    #     return self.get_value()
    #
    # @property
    # def median_value(self):
    #     return (self._high.value + self._low.value) / 2
    #
    # @property
    # def volume(self):
    #     return len(self._elements)
    #
    # @property
    # def elapse_time(self):
    #     return (self._close.datetime - self._open.datetime).total_seconds()
    #
    # @property
    # def pct_change(self):
    #     return ((float(self._close.value) - float(self._open.value)) / float(self._open.value)) * 100.0
    #
    # @property
    # def pivot(self):
    #     c = self._close.value
    #     h = self._high.value
    #     l = self._low.value
    #     P = (h + l + c) / 3
    #     S1 = (2 * P) - h
    #     S2 = P - (h - l)
    #     R1 = (2 * P) - l
    #     R2 = P + (h - l)
    #     return {'Pivot': P, 'R1': R1, 'R2': R2, 'S1': S1, 'S2': S2}
    #
    # @property
    # def std(self):
    #     return self._std
    #
    # @property
    # def change(self):
    #     return self._close.value - self._open.value
    #
    # @property
    # def open_value(self):
    #     return self._open.value
    #
    # @property
    # def low_value(self):
    #     return self._low.value
    #
    # @property
    # def high_value(self):
    #     return self._high.value
    #
    # @property
    # def close_value(self):
    #     return self._close.value
    #
    # def set_closed(self):
    #     """
    #     Set status to closed
    #     :return:
    #     """
    #     self._closed = True
    #
    # def is_closed(self):
    #     """
    #     Check of candle is closed
    #     :return:
    #     """
    #     return self._closed
    #
    # def get_zscore(self):
    #     """
    #     Get zscore
    #     :return:
    #     """
    #     diff = np.array(self._diff)
    #     zscore = stats.zscore(diff)
    #     try:
    #         return zscore[-1]
    #     except:
    #         return 0




class CandlePips(Candle):
    """
    Candle Time
    """

    def __init__(self, size, pip):
        Candle.__init__(self, size, pip)

    def update(self, element):
        """Update price
        """
        # check closed
        if self.is_closed():
            raise CandlePipsSizeExceeded()
        # process price
        self._process_price(element)
        # calculate pips
        distance = abs(self._close.value - self._open.value)
        pips = distance / self._pip
        # raise size exceeded if max is reached
        if pips > self._size:
            self.set_closed()


