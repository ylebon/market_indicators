class MovingAverageIndicator(object):
    pass

    def run(self, elements, size):
        """Return Moving Average"""
        self.elements = None


def ema(data, window):
    if len(data) < 2 * window:
        return None
    c = 2.0 / (window + 1)
    current_ema = SMA(data[-window * 2:-window], window)
    for value in data[-window:]:
        current_ema = (c * value) + ((1 - c) * current_ema)
    return current_ema