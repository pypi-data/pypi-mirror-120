from collections import defaultdict
from typing import Callable, Dict, List, TypeVar, Tuple
from toolz.functoolz import curry
import pandas as pd
from . import legacy

T = TypeVar("T")
PartitionNestedDict = Dict[str, Dict[str, T]]
Partitions = PartitionNestedDict[Tuple[int,int]]
TimePeriodGetter = PartitionNestedDict[Callable[[pd.DataFrame],pd.DataFrame]]

get_time_period_from_dataframe = curry(lambda start, end, data: data.loc[start:end, :])

class DataPartitioner():
    def __init__(self, partitions: Partitions):
        self.partitions = partitions
        self._data_partition_getters: TimePeriodGetter = defaultdict(dict)
        for partition_name, time_periods in self.partitions.items():
            for time_period_name, time_period in time_periods.items():
                start, end = time_period
                self._data_partition_getters[partition_name].update({
                    time_period_name: get_time_period_from_dataframe(
                        start,end)})

    def __call__(self,
            partition_name: str,
            time_period_name: str,
            data: pd.DataFrame)-> pd.DataFrame:
        return self._data_partition_getters[partition_name][time_period_name](data)

    @classmethod
    def from_legacy_periods(cls, periods: List[legacy.Period]):
        for p in periods:
            try:
                legacy.period_object_is_valid(p)
            except AssertionError:
                raise ValueError(f"Period {p} is not a valid time period object")

        partitions = {}
        for period in periods:
            partitions[period.name] = {
                    "train": (period.train_start, period.train_end),
                    "predict": (period.predict_start, period.predict_end),
                    }

        return cls(partitions)
