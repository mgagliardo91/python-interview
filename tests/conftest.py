from app.__main__ import run


def pytest_configure(config):
    pass


def pytest_sessionstart(session):
    run()


def pytest_sessionfinish(session, exitstatus):
    pass


def pytest_unconfigure(config):
    pass
