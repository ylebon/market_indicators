def Pivot(close, low, high):
    """
    Calculate Pivot
    :param close:
    :param low:
    :param high:
    :return:
    """
    Pivot = (high + low + close) / 3
    S1 = (2 * Pivot) - high
    S2 = Pivot - (high - low)
    R1 = (2 * Pivot) - low
    R2 = Pivot + (high - low)
    return {'Pivot': Pivot, 'R1': R1, 'R2': R2, 'S1': S1, 'S2': S2}