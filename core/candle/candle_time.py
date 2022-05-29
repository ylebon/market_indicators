from dataclasses import dataclass

from exceptions.candle import CandleTimeSizeExceeded
from indicators.core.containers.ts_container import TimeSeriesContainer


@dataclass
class CandleTime(object):
    """
    Candle Time
    """

    size: int
    container: TimeSeriesContainer = None

    def clean(self):
        """
        Clean candle

        """
        self.container = TimeSeriesContainer()

    def update(self, element):
        """Update price
        """
        try:
            date, value = self.container.get_index(0)
        except IndexError:
            self.container.update(element.date, element.value)
        else:
            elapsed_time = (element.date - date).total_seconds()
            if elapsed_time > self.size:
                raise CandleTimeSizeExceeded()
            else:
                self.container.update(element.date, element.value)

    @classmethod
    def from_empty(cls, size):
        """From empty"""
        candle = CandleTime(size=size, container=TimeSeriesContainer())
        return candle

    def is_bullish(self):
        """
        Check candle is bullish

        """
        return self.container.go_up()

    def is_bearish(self):
        """
        Check candle is bearish

        """
        return self.container.go_down()

    def open(self):
        """
        Candle open price

        """
        return self.container.get_open()

    def close(self):
        """
        Candle close price

        """
        return self.container.get_close()

    def high(self):
        """
        Candle high price

        """
        return self.container.get_high()

    def low(self):
        """
        Candle low price

        """
        return self.container.get_low()
