import uuid
from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from random import randint, uniform
from typing import Dict, Iterator, List

import pendulum


@dataclass
class Metric(ABC):
    id: str
    meter_id: str
    timestamp: datetime
    value: float
    label: str


@dataclass
class BlendedRateMetric(Metric):
    label: str = "blended_rate"


@dataclass
class ElectricUsageMetric(Metric):
    label: str = "electric_usage"


energyRateCache: Dict[str, List[BlendedRateMetric]] = {}
energyUsageCache: Dict[str, List[ElectricUsageMetric]] = {}


def initialize(rateCache, usageCache):
    for meter_id, metrics in rateCache.items():
        energyRateCache[meter_id] = [BlendedRateMetric(**m) for m in metrics]

    for meter_id, metrics in usageCache.items():
        energyUsageCache[meter_id] = [ElectricUsageMetric(**m) for m in metrics]


def get_energy_rate(meter_id: str, start_date: str, end_date: str) -> List[BlendedRateMetric]:
    if meter_id not in energyRateCache:
        metrics = [
            BlendedRateMetric(
                id=str(uuid.uuid4()),
                meter_id=meter_id,
                timestamp=timestamp,
                value=round(uniform(5.0, 7.0), 1),
            )
            for timestamp in _on_the_hour(start_date, end_date)
        ]
        energyRateCache[meter_id] = metrics

    return energyRateCache[meter_id]


def get_energy_usage(meter_id: str, start_date: str, end_date: str) -> List[ElectricUsageMetric]:
    if meter_id not in energyUsageCache:
        metrics = [
            ElectricUsageMetric(
                id=str(uuid.uuid4()),
                meter_id=meter_id,
                timestamp=timestamp,
                value=randint(450, 600),
            )
            for timestamp in _on_the_hour(start_date, end_date)
        ]
        energyUsageCache[meter_id] = metrics

    return energyUsageCache[meter_id]


def _on_the_hour(start_date: str, end_date: str) -> Iterator[datetime]:
    start = pendulum.parse(start_date).start_of("hour")  # type:ignore
    end = pendulum.parse(end_date).end_of("hour")  # type:ignore
    period = pendulum.period(start, end)
    for dt in period.range("hours"):
        yield datetime.utcfromtimestamp(dt.timestamp())
