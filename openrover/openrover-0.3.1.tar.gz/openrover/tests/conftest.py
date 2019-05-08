import pytest
import pytest_trio.plugin

BOOTLOAD_OPT = '--bootloadok'
MOTOR_OPT = '--motorok'


def pytest_addoption(parser):
    parser.addoption(BOOTLOAD_OPT, action='store_true', default=False,
                     help='enable tests that may erase the rover\'s firmware')
    parser.addoption(MOTOR_OPT, action='store_true', default=False,
                     help='enable tests that may activate the motors. '
                          'The wheels should be able to spin freely during this test, '
                          'so the rover should be untethered or raised on a jackstand.')


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "motor: this test uses the rover motors"
    )
    config.addinivalue_line(
        "markers",
        "bootload: this test may reprogram the rover"
    )


def pytest_fixture_setup(fixturedef, request):
    return pytest_trio.plugin.handle_fixture(fixturedef, request, force_trio_mode=True)


def pytest_collection_modifyitems(config, items):
    pytest_trio.plugin.automark(items)

    if not config.getoption(MOTOR_OPT):
        skip_motors = pytest.mark.skip(reason="Motor tests are disabled by default.")
        for item in items:
            if "motor" in item.keywords:
                item.add_marker(skip_motors)

    if not config.getoption(BOOTLOAD_OPT):
        skip_bootload = pytest.mark.skip(reason="Need {} option to run".format(BOOTLOAD_OPT))
        for item in items:
            if "bootload" in item.keywords:
                item.add_marker(skip_bootload)
