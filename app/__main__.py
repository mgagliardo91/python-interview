from controllers.facility import get_facility_spend_rollup


def run():
    print(get_facility_spend_rollup("123", "2020-08-01", "2020-08-02"))


if __name__ == "__main__":
    run()
