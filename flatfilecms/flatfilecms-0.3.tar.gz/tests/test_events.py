def test_globals(fake_request):
    from flatfilecms.events import add_global
    event = {'request': fake_request}
    add_global(event)
    assert 'globals' in event
    assert 'format_date' in event['globals']
    assert 'format_datetime' in event['globals']


def test_data(config):
    from flatfilecms.events import add_data
    event = {}
    add_data(event)
    assert 'data' in event
    assert event['data']['base_url'] == 'https://flatfilecms.test/'
