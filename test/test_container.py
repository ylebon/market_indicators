import time

import numpy as np

from indicators.core.containers.ts_container import TimeSeriesContainer


class TestClass(object):

    def test_one(self):
        ts = TimeSeriesContainer()
        ts.x = np.random.uniform(low=1, high=2, size=(43200))
        for i in range(100):
            start_time = time.time()
            bollinger = ts.get_bollinger()
            mean = ts.get_mean()
            stop_time = time.time()
            print(stop_time - start_time)

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')


if __name__ == "__main__":
    tc = TestClass()
    tc.test_one()
