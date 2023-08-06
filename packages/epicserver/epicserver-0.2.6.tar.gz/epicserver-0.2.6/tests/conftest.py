from epicman.logging import log, Level

# ensure debug logging is enabled
def pytest_runtestloop(session):
    log.log_level = Level.DEBUG
