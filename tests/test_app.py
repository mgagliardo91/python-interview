from app import __version__
from app.controllers.facility import get_facility_spend_rollup, get_meters
from app.controllers.meters import get_energy_spend
from app.services.meters import Meter
from app.services.metrics import Metric, get_energy_rate, get_energy_usage

facility_id = "123"
start_date = "2020-08-01"
end_date = "2020-08-02"


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
    rate = get_energy_rate(facility_id, start_date, end_date)
    usage = get_energy_usage(facility_id, start_date, end_date)

    def assert_metric(index: int, metric: Metric):
        assert metric.label == "energy_spend"
        assert metric.timestamp == rate[index].timestamp
        assert metric.value == rate[index].value * usage[index].value

    [
        assert_metric(i, m)
        for (i, m) in enumerate(get_energy_spend(facility_id, start_date, end_date))
    ]


def test_facility_rollup():
    facility_spend = get_facility_spend_rollup(facility_id, start_date, end_date)
    assert facility_spend is not None
