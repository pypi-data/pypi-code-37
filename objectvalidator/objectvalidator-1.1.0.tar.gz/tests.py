
import copy
import os

import pytest

from objectvalidator import option, OptionsContainer

SETTINGS = {
    'NAME': 'ExampleApp',
    'DATABASE': {
        'db': 'exampleapp_db',
        'host': 'localhost',
        'port': 3306,
        'user': 'exampleapp-rw',
        'password': 'a8RnU43A',
    },
}


class Config(OptionsContainer):

    def initialize(self, settings):
        self._settings = settings

    @option(required=True, attrtype=str)
    def name(self):
        return self._settings['NAME']

    @option
    def database(self):
        return DatabaseConfig(self._settings['DATABASE'])


class DatabaseConfig(OptionsContainer):

    def initialize(self, database_settings):
        self._database_settings = database_settings

    @option(required=True, attrtype=str)
    def db(self):
        db = os.environ.get('DATABASE_DB')
        if db is not None:
            return db
        return self._database_settings['db']

    @option(required=True, attrtype=str)
    def host(self):
        host = os.environ.get('DATABASE_HOST')
        if host is not None:
            return host
        return self._database_settings['host']

    @option(required=True, attrtype=int)
    def port(self):
        port = os.environ.get('DATABASE_PORT')
        if port is not None:
            return int(port)
        return self._database_settings.get('port', 3306)

    @option(required=True, attrtype=str)
    def user(self):
        user = os.environ.get('DATABASE_USER')
        if user is not None:
            return user
        return self._database_settings['user']

    @option(required=False, attrtype=str)
    def password(self):
        password = os.environ.get('DATABASE_PASSWORD')
        if password is not None:
            return password
        return self._database_settings.get('password')


def test_validate():
    config = Config(SETTINGS)
    assert config.name == 'ExampleApp'
    assert isinstance(config.database, DatabaseConfig)
    assert config.database.db == 'exampleapp_db'
    assert config.database.host == 'localhost'
    assert config.database.port == 3306
    assert config.database.user == 'exampleapp-rw'
    assert config.database.password == 'a8RnU43A'


def test_pass_when_missing_optional_value():
    SETTINGS_NEW = copy.deepcopy(SETTINGS)
    del SETTINGS_NEW['DATABASE']['password']
    config = Config(SETTINGS_NEW)
    assert config.database.password is None


def test_fail_when_invalid_str_type():
    SETTINGS_BAD = copy.deepcopy(SETTINGS)
    SETTINGS_BAD['NAME'] = 123
    with pytest.raises(
            ValueError, match=r'Config.name: str type is expected'):
        Config(SETTINGS_BAD)


def test_fail_when_invalid_int_type():
    SETTINGS_BAD = copy.deepcopy(SETTINGS)
    SETTINGS_BAD['DATABASE']['port'] = '3306'
    with pytest.raises(
            ValueError, match=r'DatabaseConfig.port: int type is expected'):
        Config(SETTINGS_BAD)


def test_fail_when_missing_required_value():
    SETTINGS_BAD = copy.deepcopy(SETTINGS)
    del SETTINGS_BAD['DATABASE']['user']
    with pytest.raises(
            ValueError, match=r"Config.database: DatabaseConfig.user: 'user'"):
        Config(SETTINGS_BAD)


def test_fail_when_empty_required_value():
    SETTINGS_BAD = copy.deepcopy(SETTINGS)
    SETTINGS_BAD['DATABASE']['user'] = None
    with pytest.raises(
            ValueError, match=(
                r'Config.database: DatabaseConfig.user: '
                r'Option value is required')):
        Config(SETTINGS_BAD)


def test_fail_when_setting_attribute():
    config = Config(SETTINGS)
    with pytest.raises(
            TypeError, match=r'Object does not support item assignment'):
        config.database.host = '127.0.0.1'
