import channel_access.common as ca



def test_datetime_to_epics():
    assert ca.datetime_to_epics(ca.EPICS_EPOCH) == (0, 0)

def test_epics_to_datetime():
    assert ca.epics_to_datetime((0, 0)) == ca.EPICS_EPOCH
