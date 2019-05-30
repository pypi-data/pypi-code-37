from generic_sports_dataio_client import GenericSportsDataIOClient
from generic_sports_dataio_client import getEnv


class SportsClientNBA (GenericSportsDataIOClient):
    def __init__(self, sd_subs_key_nba=None, customHttpClient=None):
        super().__init__(customHttpClient)
        if sd_subs_key_nba is None:
            self.secretKey = getEnv('SD_SUBS_KEY_NBA')
        else:
            self.secretKey = sd_subs_key_nba

    def getLeague(self):
        return 'nba'
