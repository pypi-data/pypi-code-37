import re
import sys

import numpy as np
import nvector as nv
from geopy.distance import distance
from unidecode import unidecode

try:
    import redis
    redis_support = True
    from .prepare import load_lookup_redis
    try:
        import ujson as json
    except ImportError:
        import json
except ImportError:
    pass

from . import config
from .prepare import create_resources
from .prepare import load_resource


class Locator(object):
    """
    Map strings to locations.
    
    At the first run, around 200 MB of necessary data will be downloaded and processed.
    In the runs thereafter the locally cached data is used.
    """

    resources_dir = config.resources_dir.absolute()
    resources_cache_dir = config.resources_cache_dir.absolute()

    def __init__(self, refresh=False, server=False, refresh_server=False):
        """
        Set up Locator

        For server applications using multiprocess / threading the redis subsystem is recommended.
        The server variable can be set to a dictionary containing settings for the redis server.
        Setting server to True will use the redis-py defaults.

        server = {'host': 'localhost', 'port': 6379, 'db': 0}

        Args:
            refresh (bool): if True force a refresh of the lookup tables
            server (bool, dict): settings for server use
            refresh_server (bool): reload the lookup tables into redis
        """

        create_resources(refresh=refresh)
        if server:
            if not redis_support:
                print(f"PinPoint: please install redis and hiredis to use this subsystem", file=sys.stderr)
                raise ImportError
            server_config = config.server_default
            if type(server) is dict:
                server_config.update(server)
            self.redis_connection = redis.Redis(decode_responses=True, **server_config)
            load_lookup_redis(self.redis_connection, refresh_server=refresh_server)
            self.find_country = self.find_country_server
            self.find_region = self.find_region_server
            self.find_city = self.find_city_server

        else:
            self.lookup = load_resource(config.resources_dir / 'lookup.gzip')
            self.country_data = load_resource(config.resources_dir / 'country_data.gzip')
            self.city_data = load_resource(config.resources_dir / f'city_data_{config.city_resolution}.gzip')
            self.region_data = load_resource(config.resources_dir / f'region_data.gzip')

    def find_country(self, raw_string):
        """
        Extract country from a string.
        
        Args:
            raw_string (str): string to be analyzed

        Returns:
            (dict): country dictionary
        """

        raw_string = raw_string.strip()

        words = re.split(r'[,.!;&?0-9]+', raw_string.lower())
        words = list(map(lambda w: w.strip(), words))
        single_words = re.split(r'[,!;&?0-9()\s\\/\-]+', raw_string.lower())
        grow_words = [' '.join(single_words[-2:]), ' '.join(single_words[-3:]), ' '.join(single_words[-4:])]

        for parameter in ('country_full', 'country_alternate'):
            for phrase in (words[-1], single_words[-1], grow_words[0]):
                if phrase in self.lookup[parameter]:
                    return self.country_data[self.lookup[parameter][phrase]]

        for parameter in ('country_full', 'country_alternate'):
            for phrases in (words[:-1], grow_words[1:], single_words[:-1]):
                for phrase in reversed(phrases):
                    if phrase in self.lookup[parameter]:
                        return self.country_data[self.lookup[parameter][phrase]]

        return None

    def find_country_server(self, raw_string):
        """
        Extract country from a string. (redis version)

        Args:
            raw_string (str): string to be analyzed

        Returns:
            (dict): country dictionary
        """

        raw_string = raw_string.strip()

        words = re.split(r'[,.!;&?0-9]+', raw_string.lower())
        words = list(map(lambda w: w.strip(), words))
        single_words = re.split(r'[,!;&?0-9()\s\\/\-]+', raw_string.lower())
        grow_words = [' '.join(single_words[-2:]), ' '.join(single_words[-3:]), ' '.join(single_words[-4:])]

        quick_keys = []
        full_keys = []
        for parameter in ('country_full', 'country_alternate'):
            quick_keys += [f'{config.redis_prefix}:lu:{parameter}:{phrase}' for phrase in (words[-1], single_words[-1], grow_words[0])]
            full_keys += [f'{config.redis_prefix}:lu:{parameter}:{phrase}' for phrase in (words[:-1][::-1] + grow_words[1:][::-1] + single_words[:-1][::-1])]

        quick_test = self.redis_connection.mget(*quick_keys)

        try:
            country_code = next(item for item in quick_test if item is not None)
        except StopIteration:
            full_test = self.redis_connection.mget(*full_keys)
            try:
                country_code = next(item for item in full_test if item is not None)
            except StopIteration:
                return None

        country_data = self.redis_connection.get(f'{config.redis_prefix}:db:country:{country_code}')
        return json.loads(country_data)

    def find_region(self, raw_string, country):
        """
        Extract region from a string.
        
        Just helpful for USA and Canada at the moment. 
        
        Args:
            raw_string (str): string to be analysed 
            country (dict): country dictionary

        Returns:
            (dict): region dictionary
        """

        raw_string = raw_string.strip()

        words = re.split(r'[,.!;&?0-9]+', raw_string.lower())
        words = list(map(lambda w: w.strip(), words))
        single_words = re.split(r'[,.!;&?0-9()\s\\/\-]+', raw_string.lower())

        for parameter in ('region_full', 'region_alternate'):
            for phrases in (words, single_words):
                for phrase in reversed(phrases):
                    if phrase in self.lookup[parameter][country['a2']]:
                        return self.region_data[country['a2']][self.lookup[parameter][country['a2']][phrase]]

        return None

    def find_region_server(self, raw_string, country):
        """
        Extract region from a string. (redis version)

        Just helpful for USA and Canada at the moment.

        Args:
            raw_string (str): string to be analysed
            country (dict): country dictionary

        Returns:
            (dict): region dictionary
        """

        raw_string = raw_string.strip()

        words = re.split(r'[,.!;&?0-9]+', raw_string.lower())
        words = list(map(lambda w: w.strip(), words))
        single_words = re.split(r'[,.!;&?0-9()\s\\/\-]+', raw_string.lower())

        keys = []
        for parameter in ('region_full', 'region_alternate'):
            keys += [f'{config.redis_prefix}:lu:{parameter}:{country["a2"]}:{phrase}' for phrase in (words[::-1] + single_words[::-1])]

        quick_test = self.redis_connection.mget(*keys)

        try:
            region_code = next(item for item in quick_test if item is not None)
        except StopIteration:
                return None

        region_data = self.redis_connection.get(f'{config.redis_prefix}:db:region:{region_code}')
        return json.loads(region_data)

    def find_city(self, raw_string,  country, region=None):
        """
        Extract city from a string.
        
        Args:
            raw_string: string to be analysed 
            country: country dictionary
            region: region dictionary (optional - useful for USA and Canada) 

        Returns:
            (dict): city dictionary
        """

        raw_string = raw_string.strip()

        words = re.split(r'[,.!;&?0-9]+', raw_string.lower())
        words = list(map(lambda w: w.strip(), words))
        single_words = re.split(r'[,.!;&?0-9()\s\\/\-]+', raw_string.lower())

        if region:
            for parameter in ('city_region_quick', 'city_region_full', 'city_region_alternate'):
                for phrases in (words, single_words):
                    for phrase in reversed(phrases):
                        try:
                            if phrase in self.lookup[parameter][country['a2']][region['region_code']]:
                                return self.city_data[
                                    country['a2']][self.lookup[parameter][country['a2']][region['region_code']][phrase]]
                        except KeyError:
                            pass
        else:
            for parameter in ('city_quick', 'city_full', 'city_alternate'):
                for phrases in (words, single_words):
                    for phrase in reversed(phrases):
                        try:
                            if phrase in self.lookup[parameter][country['a2']]:
                                return self.city_data[country['a2']][self.lookup[parameter][country['a2']][phrase]]
                        except KeyError:
                            pass
        words = re.split(r'[,.!;&?0-9]+', unidecode(raw_string.lower()))
        words = list(map(lambda w: w.strip(), words))
        single_words = re.split(r'[,.!;&?0-9()\s\\/\-]+', unidecode(raw_string.lower()))

        if region:
            for parameter in ('city_region_quick', 'city_region_full', 'city_region_alternate'):
                for phrases in (words, single_words):
                    for phrase in reversed(phrases):
                        try:
                            if phrase in self.lookup[parameter][country['a2']][region['region_code']]:
                                return self.city_data[country['a2']][self.lookup[parameter][country['a2']][region['region_code']][phrase]]
                        except KeyError:
                            pass
        else:
            for parameter in ('city_quick', 'city_full', 'city_alternate'):
                for phrases in (words, single_words):
                    for phrase in reversed(phrases):
                        try:
                            if phrase in self.lookup[parameter][country['a2']]:
                                return self.city_data[country['a2']][self.lookup[parameter][country['a2']][phrase]]
                        except KeyError:
                            pass

        if region:
            for post_code in self.lookup['city_region_post_code'][country['a2']][region['region_code']]:
                if post_code in raw_string:
                    try:
                        return self.city_data[country['a2']][
                            self.lookup['city_region_post_code'][country['a2']][region['region_code']][post_code]]
                    except KeyError:
                        pass
        else:
            try:
                for post_code in self.lookup['city_post_code'][country['a2']]:
                    if post_code in raw_string:
                        return self.city_data[country['a2']][
                            self.lookup['city_post_code'][country['a2']][post_code]]
            except KeyError:
                pass
        return None

    def find_city_server(self, raw_string, country, region=None):
        """
        Extract city from a string. (redis version)

        Args:
            raw_string: string to be analysed
            country: country dictionary
            region: region dictionary (optional - useful for USA and Canada)

        Returns:
            (dict): city dictionary
        """

        raw_string = raw_string.strip()

        words = re.split(r'[,.!;&?0-9]+', raw_string.lower())
        words = list(map(lambda w: w.strip(), words))
        single_words = re.split(r'[,.!;&?0-9()\s\\/\-]+', raw_string.lower())
        if region:
            parameter_list = ('city_region_quick', 'city_region_full', 'city_region_alternate')
            parameter_postcode = 'city_region_post_code'
            region_key = f':{region["region_code"]}'
        else:
            parameter_list = ('city_quick', 'city_full', 'city_alternate')
            region_key = ''
            parameter_postcode = 'city_post_code'
        quick_keys = []
        for parameter in parameter_list:
                quick_keys += [f'{config.redis_prefix}:lu:{parameter}:{country["a2"]}{region_key}:{phrase}' for phrase in (words[::-1] + single_words[::-1])]

        quick_test = self.redis_connection.mget(*quick_keys)
        try:
            city_code = next(item for item in quick_test if item is not None)
            city_data = self.redis_connection.get(f'{config.redis_prefix}:db:city:{city_code}')
            return json.loads(city_data)
        except StopIteration:
            pass


        words = re.split(r'[,.!;&?0-9]+', unidecode(raw_string.lower()))
        words = list(map(lambda w: w.strip(), words))
        single_words = re.split(r'[,.!;&?0-9()\s\\/\-]+', unidecode(raw_string.lower()))
        quick_unicode_keys = []

        for parameter in parameter_list:
            quick_unicode_keys += [f'{config.redis_prefix}:lu:{parameter}:{country["a2"]}{region_key}:{phrase}' for phrase in
                          (words[::-1] + single_words[::-1])]

        quick_unicode_test = self.redis_connection.mget(*quick_unicode_keys)
        try:
            city_code = next(item for item in quick_unicode_test if item is not None)
            city_data = self.redis_connection.get(f'{config.redis_prefix}:db:city:{city_code}')
            return json.loads(city_data)
        except StopIteration:
            pass

        for post_code in json.loads(self.redis_connection.get(f'{config.redis_prefix}:lu:{parameter_postcode}_list:{country["a2"]}{region_key}')):
            if post_code in raw_string:
                city_code = self.redis_connection.get(f'{config.redis_prefix}:lu:{parameter_postcode}:{country["a2"]}{region_key}:{post_code}')
                if city_code:
                    city_data = self.redis_connection.get(f'{config.redis_prefix}:db:city:{city_code}')
                    return json.loads(city_data)

    def find(self, raw_string):
        """
        Extract location information from a string.
        
        Args:
            raw_string: string to be analyzed

        Returns:
            (dict or None,dict or None, dict or None): country, region, city

        """
        if not raw_string:
            return None, None, None
        if len(raw_string) < 4:
            return None, None, None

        country = self.find_country(raw_string)

        if country is None:
            return None, None, None

        # Giving region codes is most common in United States and Canada
        if country['a2'] in ('US', 'CA'):
            region = self.find_region(raw_string, country)
        else:
            region = None

        city = self.find_city(raw_string, country, region)

        return country, region, city

    def calculate_str(self, weighted_strings):
        """
        Calculate the apparent location and cooperation distance for a set of weighted location strings.

        Args:
            weighted_strings (dict):  (location: weight, ...)

        Returns:
            cooperation_distance, apparent_location
        """

        if not weighted_strings:
            return None, None

        weighted_coordinates = []
        for location_string, weight in weighted_strings.items():
            country, region, city = self.find(location_string)
            if city:
                weighted_coordinates.append((weight, (city["latitude"], city["longitude"])))

        return self.calculate_coordinates(weighted_coordinates)

    @staticmethod
    def calculate_coordinates(weighted_coordinates):
        """

        Args:
            weighted_coordinates (list OR Tuple): ((weight, (latitude, longitude)), ...)

        Returns:
            cooperation_distance, apparent_location
        """

        if not weighted_coordinates:
            return None, None

        city_lat = []
        city_lon = []
        city_weight = []
        distances = []
        for weight, location in weighted_coordinates:
            city_lat.append(location[0])
            city_lon.append(location[1])
            city_weight.append(weight)

        if sum(city_weight) == 0:
            return None, None

        city_points = nv.GeoPoint(latitude=city_lat, longitude=city_lon, degrees=True)
        city_vector = city_points.to_nvector()
        city_normals = city_vector.normal

        apparent_normal = np.sum(city_normals * city_weight, axis=1)
        apparent_normal /= np.linalg.norm(apparent_normal)
        apparent_vector = nv.Nvector(apparent_normal.reshape((3, 1)))
        apparent_point = apparent_vector.to_geo_point()
        apparent_location = (apparent_point.latitude_deg[0], apparent_point.longitude_deg[0])

        for weight, location in weighted_coordinates:
            distances.append(weight / sum(city_weight) * distance(location, apparent_location).kilometers)
        try:
            cooperation_distance = round(sum(distances) * 2.0)
        except ValueError:
            cooperation_distance = None
            apparent_location = None

        return cooperation_distance, apparent_location
