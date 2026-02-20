import statistics

from messages import Prompt, Response


def get_statistics(msg: Prompt) -> Response:
    return Response(
        mean=statistics.mean(msg.data),
        median=statistics.median(msg.data),
        median_low=statistics.median_low(msg.data),
        median_high=statistics.median_high(msg.data),
        mode=statistics.mode(msg.data),
        multi_mode=statistics.multimode(msg.data),
        population_variance=statistics.pvariance(msg.data),
        sample_variance=statistics.variance(msg.data),
        population_standard_deviation=statistics.pstdev(msg.data),
        sample_standard_deviation=statistics.stdev(msg.data),
    )
