from collections import deque

import pandas as pd
from logbook import Logger

from exceptions.candle import CandleTimeSizeExceeded
from indicators.core.candle.candle_time import CandleTime


class CandleContainer(object):
    """
    Candle container

    """
    CANDLE_TYPES = {
        'time': CandleTime
    }

    def __init__(self, candle_type, candle_size, metrics=None, max_len=5):
        self.max_len = max_len
        self.old_candles = deque(maxlen=self.max_len-1)
        self.candle_class = CandleContainer.CANDLE_TYPES[candle_type]
        self.candle_size = candle_size
        self.candle_metrics = metrics or dict()
        self.current_candle = None
        self.log = Logger("CandlesContainer")
        self.handlers = dict()

    @classmethod
    def from_empty(cls, c_type, c_size, max_len=5):
        """
        From empty

        """
        candle = CandleContainer(c_type, c_size, max_len=max_len)
        return candle

    @property
    def candles(self):
        """
        Return candles

        """
        return list(self.old_candles) + [self.current_candle]

    def clean(self):
        """
        Clean container

        """
        self.old_candles = deque(maxlen=self.max_len-1)
        self.current_candle = None

    def update(self, candle_element):
        """
        Update container

        """
        try:
            self.current_candle.update(candle_element)
        except AttributeError:
            self.create_new_candle()
            self.current_candle.update(candle_element)
        except CandleTimeSizeExceeded:
            self.callback("CANDLE_FULL", self.current_candle)
            self.old_candles.append(self.current_candle)
            # update candle
            self.create_new_candle()
            self.current_candle.update(candle_element)

    def create_new_candle(self):
        """
        Create new candle

        """
        self.current_candle = self.candle_class.from_empty(size=self.candle_size)

    def get_current(self):
        """
        Return current candle

        """
        return self.current_candle

    def get_sma(self, window):
        """
        Return SMA

        """
        if len(self.candles) < window:
            return
        else:
            candles = self.candles[-window:]
            close_prices = [c.container.get_close() for c in candles]
            sma = SMA(close_prices, window)
            return sma

    def get_rsi(self, window):
        """
        Return RSI

        """
        down = list()
        up = list()
        rsi = None
        # candles
        for candle in self.candles:
            diff = candle.container.get_diff()
            if candle.container.go_down():
                down.append(diff)
            elif candle.container.got_up():
                up.append(candle.diff)

        # create series
        up_series = pd.Series(up)
        down_series = pd.Series(down)
        roll_up = up_series.ewm(span=window, min_periods=window - 1).mean()
        roll_down = down_series.abs().ewm(span=window, min_periods=window - 1).mean()
        if not roll_up.empty and not roll_down.empty:
            rs = (roll_up.iloc[-1]) / (roll_down.iloc[-1])
            rsi = (100.0 - (100.0 / (1.0 + rs)))
        return rsi

    def get_candles(self):
        """
        Return all candles

        """
        return self.candles

    def get_index(self, index):
        """
        Return candle at certain index

        """
        return self.candles[index]

    def get_size(self):
        """
        Return candles length

        """
        return len(self.candles)

    def get_last(self, nbr_of_candles):
        """
        Return candles

        """
        return self.candles[-nbr_of_candles:]

    def callback(self, name, *args):
        """
        Execute signal

        """
        for handler in self.handlers.get(name, []):
            handler(*args)

    def on_event(self, event_type):
        """
        On event

        """

        def register_handler(handler):
            # signal executor handlers
            try:

                self.handlers[event_type].append(handler)
            except KeyError:
                self.handlers[event_type] = [handler]
            return handler

        return register_handler
