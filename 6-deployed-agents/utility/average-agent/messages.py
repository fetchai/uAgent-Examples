from typing import List, Union

from uagents import Model


class Prompt(Model):
    data: List[Union[int, float]]


class Response(Model):
    mean: float
    median: float
    median_low: float
    median_high: float
    mode: float
    multi_mode: List[Union[int, float]]
    population_variance: float
    sample_variance: float
    population_standard_deviation: float
    sample_standard_deviation: float
