from typing import List

from ..services.meters import Meter, get_meters_for_facility
from .meters import get_energy_spend


def get_meters(facility_id: str) -> List[Meter]:
    return get_meters_for_facility(facility_id)


def get_facility_spend_rollup(facility_id: str, start_date: str, end_date: str) -> float:
    meters = get_meters_for_facility(facility_id)
    return sum([_get_meter_spend_rollup(meter.id, start_date, end_date) for meter in meters])


def _get_meter_spend_rollup(meter_id: str, start_date: str, end_date: str) -> float:
    meter_spend = [spend.value for spend in get_energy_spend(meter_id, start_date, end_date)]
    return sum(meter_spend)
