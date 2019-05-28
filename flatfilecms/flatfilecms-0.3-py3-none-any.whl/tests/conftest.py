import pytest


@pytest.fixture
def current_directory():
    from pathlib import Path
    return Path(__file__).parent


@pytest.fixture
def config(current_directory):
    from pyramid.testing import testConfig
    settings = {
        'data_path': current_directory / 'data',
        'jinja2.filters': 'join_url = flatfilecms.filters.join_url'
    }
    with testConfig(settings=settings) as config:
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('tests:templates')
        config.add_jinja2_search_path('flatfilecms:templates')
        yield config


@pytest.fixture
def fake_request():
    from pyramid.testing import DummyRequest
    return DummyRequest()
