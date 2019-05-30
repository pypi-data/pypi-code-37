from datetime import datetime, timedelta, date
from os import environ
from pprint import pprint
from urllib import request
from urllib.parse import urlencode
from default_http_client import DefaultHttpClient
from abc import ABCMeta, abstractmethod
import sys
import json
import threading


def getEnv(varName, defaultValue=None):
    return environ.get(varName) if environ.get(varName) else defaultValue


class GenericSportsDataIOClient:
    def __init__(self, customHttpClient=None):
        self.baseUrl = getEnv('SPORT_RADAR_BASE_URL',
                              'https://api.sportsdata.io/v3')
        self.secretKey = None
        self.authHeader = 'Ocp-Apim-Subscription-Key'
        self.httpClient = customHttpClient if customHttpClient \
            else DefaultHttpClient()
        self.maxThreads = 15
        self.threadArgs = {}
        self.threads = []

    def __getAuthHeaders(self, headers={}):
        alteredHeaders = headers.copy()
        alteredHeaders[self.authHeader] = self.secretKey
        return alteredHeaders

    def __buildFuncURL(self, funcURL, **placeHolders):
        try:
            return self.baseUrl + funcURL % placeHolders
        except Exception as e:
            sys.stderr.write(repr(e) + "\n")
            return self.baseUrl

    def __doApiCall(self, fullURL, headers={}):
        authHeaders = self.__getAuthHeaders(headers)
        response = self.httpClient.get(fullURL, authHeaders)
        return json.loads(response) if response else None

    def __dateRange(self, startDate, endDate):
        for n in range(int((endDate - startDate).days)+1):
            yield startDate + timedelta(n)

    @abstractmethod
    def getLeague(self):
        return None

    def getTeams(self):
        leagueName = self.getLeague()
        current_secretKey = self.secretKey
        self.secretKey = getEnv('SD_FREE_SUBS_KEY')
        fullURL = \
            self.__buildFuncURL('/%(league)s/scores/json/'
                                'teams',
                                league=leagueName)
        response = self.__doApiCall(fullURL)
        self.secretKey = current_secretKey
        return response

    def getPreGameOddsByDate(self, date=None):
        now = date if date else datetime.now().date()
        nowIso = now.isoformat()
        leagueName = self.getLeague()
        fullURL = \
            self.__buildFuncURL('/%(league)s/odds/json/'
                                'GameOddsByDate/%(date)s',
                                date=nowIso, league=leagueName)
        response = self.__doApiCall(fullURL)
        return response

    def __getPreGameOddsByDates(self, dates, responseHash, thId):
        leagueName = self.getLeague()
        oddsForDates = []
        for now in dates:
            odds = self.getPreGameOddsByDate(now)
            oddsForDates.append(odds)
        responseHash[thId] = oddsForDates

    def __spreadDates(self, startDate, endDate):
        self.threadArgs = {}
        index = 0
        for d in self.__dateRange(startDate, endDate):
            try:
                self.threadArgs[index].append(d.date())
            except Exception as e:
                self.threadArgs[index] = []
                self.threadArgs[index].append(d.date())
                index = (index + 1) % self.maxThreads

    def __createThreads(self, responseHash):
        self.threads = []
        index = 0
        for (k, dates) in self.threadArgs.items():
            self.threads.append(
                threading.Thread(
                    target=self.__getPreGameOddsByDates,
                    args=(dates, responseHash, index)))
            index = index + 1

    # startDate and endDate are strings %Y-%m-%d (isodate)
    def getPreGameOdds(self, startDate=None, endDate=None):
        preGames = []
        threadsData = {}

        sdate = datetime.strptime(startDate, '%Y-%m-%d') if startDate else \
            datetime.now()
        edate = datetime.strptime(endDate, '%Y-%m-%d') if endDate else \
            sdate + timedelta(days=15)

        self.__spreadDates(sdate, edate)
        self.__createThreads(threadsData)

        for th in self.threads:
            th.start()

        for th in self.threads:
            th.join()

        for (i, threadOdds) in threadsData.items():
            for thOdds in threadOdds:
                if thOdds:
                    for odds in thOdds:
                        preGames.append(odds)
        return preGames
