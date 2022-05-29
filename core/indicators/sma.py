

def run():
    if len(data) < window:
        return None
    return float(sum(data[-window:]) / float(window))