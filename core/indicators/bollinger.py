




def calculate_bollinger(data, window=None, num_of_std=2):
    if window and len(data) < window:
        return None
    elif window:
        rolling_mean = sum(data[-window:]) / window
        stddev_num = sum(map(lambda x: (x - rolling_mean) ** 2, data[-window:]))
        stddev = sqrt(stddev_num / window)
        upper_band = rolling_mean + (num_of_std * stddev)
        lower_band = rolling_mean - (num_of_std * stddev)
        return rolling_mean, upper_band, lower_band
    elif len(data):
        rolling_mean = sum(data) / len(data)
        stddev_num = sum(map(lambda x: (x - rolling_mean) ** 2, data))
        stddev = sqrt(stddev_num / window)
        upper_band = rolling_mean + (num_of_std * stddev)
        lower_band = rolling_mean - (num_of_std * stddev)
        return rolling_mean, upper_band, lower_band
    else:
        return None