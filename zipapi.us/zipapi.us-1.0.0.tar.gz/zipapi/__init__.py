import requests
from requests.auth import HTTPBasicAuth
import json
from enum import Enum


class DistanceUnit(Enum):

    Miles = 'mi'
    Kilometers = 'km'


class ZipAPI:

    def __init__(self, apikey="", username="", password=""):
        self.apikey = apikey
        self.username = username
        self.password = password

    def GetZipInfo(self, zipcode):
        zipcode_json = requests.get(
            'https://service.zipapi.us/zipcode/' + str(zipcode),
            params={
                'X-API-KEY': self.apikey,
                'fields': 'geolocation,population'
            },
            auth=
            HTTPBasicAuth(
                self.username,
                self.password
            )
        ).content.decode()
        zipcode_json = json.loads(zipcode_json)['data']
        return ZipCode(
            zipcode=zipcode,
            city=zipcode_json['city'],
            state=zipcode_json['state'],
            lat=zipcode_json['latitude'],
            long=zipcode_json['longitude'],
            population=zipcode_json['population']
        )

    def GetZipsForCityAndState(self, city, state):
        zips_json = requests.get(
            'https://service.zipapi.us/zipcode/zips/',
            params={
                'X-API-KEY': self.apikey,
                'city': city,
                'state': state
            },
            auth=
            HTTPBasicAuth(
                self.username,
                self.password
            )
        ).content.decode()
        zips_json = json.loads(zips_json)
        return zips_json['data']

    def GetDistance(self, zip1, zip2, distanceUnit=DistanceUnit.Miles):
        distanceUnit = distanceUnit.value
        zips_json = requests.get(
            'https://service.zipapi.us/zipcode/distance',
            params={
                'X-API-KEY': self.apikey,
                'zip1': str(zip1),
                'zip2': str(zip2),
                'unit': distanceUnit
            },
            auth=
            HTTPBasicAuth(
                self.username,
                self.password
            )
        ).content.decode()
        zips_json = json.loads(zips_json)['data']
        return zips_json['distance']

    def GetZipCodesFromRadius(self, zipcode, radius):
        zips = []
        zips_json = requests.get(
            'https://service.zipapi.us/zipcode/radius/' + str(zipcode),
            params={
                'X-API-KEY': self.apikey,
                'radius': str(radius)
            },
            auth=
            HTTPBasicAuth(
                self.username,
                self.password
            )
        ).content.decode()
        zips_json = json.loads(zips_json)['data']
        for zipData in zips_json:
            zips.append(
                ZipCodeFromRadius(
                    zipcode=zipData['ZipCode'],
                    distance=zipData['distance']
                )
            )
        return zips

    def GetPopulationDataForZip(self, zip):
        population_json = requests.get(
            'https://service.zipapi.us/population/zipcode/' + str(zip),
            params={
                'X-API-KEY': self.apikey,
                'fields': 'male_population,female_population'
            },
            auth=
            HTTPBasicAuth(
                self.username,
                self.password
            )
        ).content.decode()
        population_json = json.loads(population_json)['data']
        return Population(
            population=population_json['population'],
            male_population=population_json['male_population'],
            female_population=population_json['female_population']
        )

    def GetAverageAgeForZip(self, zip):
        age_json = requests.get(
            'https://service.zipapi.us/age/zipcode/' + str(zip),
            params={
                'X-API-KEY': self.apikey,
                'fields': 'male_age,female_age'
            },
            auth=
            HTTPBasicAuth(
                self.username,
                self.password
            )
        ).content.decode()
        age_json = json.loads(age_json)['data']
        return Age(
            median_age=age_json['median_age'],
            male_age=age_json['male_age'],
            female_age=age_json['female_age']
        )


class Age:

    def __init__(self, median_age, male_age, female_age):
        self.median_age = median_age
        self.male_age = male_age
        self.female_age = female_age

class Population:

    def __init__(self, population, male_population, female_population):
        self.population = population
        self.male_population = male_population
        self.female_population = female_population


class ZipCodeFromRadius:

    def __init__(self, zipcode, distance):
        self.zipcode = zipcode
        self.distance = distance


class ZipCode:

    def __init__(self, zipcode, city, state, lat, long, population):
        self.zipcode = zipcode
        self.city = city
        self.state = state
        self.lat = lat
        self.long = long
        self.population = population

    def GetFullStateName(self):
        return {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
        }[self.state]
