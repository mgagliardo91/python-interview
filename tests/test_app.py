from os.path import dirname, join
from typing import List

from yaml import FullLoader, load

from app import __version__
from app.controllers.facility import get_facility_spend_rollup, get_meters
from app.controllers.meters import get_energy_spend
from app.services.meters import Meter, get_meters_for_facility
from app.services.metrics import Metric

facility_id = "123"
start_date = "2020-08-01"
end_date = "2020-08-03"

output_file = open(join(dirname(__file__), "../fixtures", "output.yaml"), "r")
output = load(output_file, Loader=FullLoader)


def test_version():
    assert __version__ == "0.1.0"


def test_facility_meters():
    meters = get_meters(facility_id)

    def assert_meter(meter: Meter):
        assert meter.id is not None
        assert len(meter.name) > 0
        assert meter.facility_id == facility_id

    [assert_meter(m) for m in meters]


def test_meter_energy_spend():
    meters = get_meters_for_facility(facility_id)

    def assert_metrics(meterId: str, metrics: List[Metric]):
        cached = output["meter_spend"][meterId]
        assert len(metrics) == len(cached)
        for i, m in enumerate(metrics):
            assert m.value == cached[i]["value"]

    meter_spends = {meter.id: get_energy_spend(meter.id, start_date, end_date) for meter in meters}

    [assert_metrics(meterId, metrics) for (meterId, metrics) in meter_spends.items()]


def test_facility_rollup():
    facility_spend = get_facility_spend_rollup(facility_id, start_date, end_date)
    assert facility_spend is not None
    assert facility_spend == output["facility_spend"]
