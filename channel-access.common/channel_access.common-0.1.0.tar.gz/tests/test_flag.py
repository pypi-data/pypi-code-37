import channel_access.common as ca



def test_flag_or():
    ored = ca.Events.VALUE | ca.Events.PROPERTY
    assert ored.value == (ca.Events.VALUE.value | ca.Events.PROPERTY.value)
