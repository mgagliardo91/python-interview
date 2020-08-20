import uuid
from dataclasses import dataclass
from typing import List

from ..services.metrics import Metric, get_energy_rate, get_energy_usage


@dataclass
class EnergySpend(Metric):
    label: str = "energy_spend"


def get_energy_spend(meter_id: str, start_date: str, end_date: str) -> List[EnergySpend]:
    rates = get_energy_rate(meter_id, start_date, end_date)
    usages = get_energy_usage(meter_id, start_date, end_date)
    return [
        EnergySpend(str(uuid.uuid4()), x.meter_id, x.timestamp, x.value * y.value)
        for (x, y) in zip(rates, usages)
    ]
