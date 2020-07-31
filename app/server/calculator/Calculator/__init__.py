from .StatsCalculator import StatsCalculator


def basicStatisic(values):
    sc = StatsCalculator()
    return {
        'mean' : sc.mean(values),
        'median': sc.median(values),
        'mode' : sc.mode(values),
        'stdev' : sc.stdev(values),
        'variance':sc.variance(values)
    }