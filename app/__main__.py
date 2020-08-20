from os.path import dirname, join

from yaml import FullLoader, load

from .services.meters import initialize as initialize_meters
from .services.metrics import initialize as initialize_metrics


def run():
    cache_file = open(join(dirname(__file__), "../fixtures", "cache.yaml"), "r")
    cache = load(cache_file, Loader=FullLoader)
    initialize_meters(cache["meters"])
    initialize_metrics(cache["rate"], cache["usage"])


if __name__ == "__main__":
    run()
