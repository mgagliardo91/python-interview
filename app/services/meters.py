import uuid
from dataclasses import dataclass
from typing import Dict, List

from faker import Faker

fake = Faker()


@dataclass
class Meter:
    id: str
    name: str
    facility_id: str


facilityCache: Dict[str, List[Meter]] = {}


def get_meters_for_facility(facility_id: str) -> List[Meter]:
    if facility_id not in facilityCache:
        meters = [
            Meter(id=str(uuid.uuid4()), name=fake.company(), facility_id=facility_id)
            for i in range(20)
        ]
        facilityCache[facility_id] = meters

    return facilityCache[facility_id]
