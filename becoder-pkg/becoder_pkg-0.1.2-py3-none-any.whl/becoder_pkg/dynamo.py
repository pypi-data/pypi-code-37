import requests
import json

DYNAMO_ENDPOINT = 'http://52.78.142.161:5000/scrap_book'


class ScrapBook(object):
    db_endpoint = DYNAMO_ENDPOINT

    def __init__(self, user_email):
        self.user_email = user_email

    def user_key(self, key):
        return '_'.join([self.user_email, key])

    def get(self, key):
        user_key = self.user_key(key)
        params = {
            'key': user_key
        }
        response = requests.get(self.db_endpoint, params=params)

        if response.status_code == 200:
            result = json.loads(response.text)['response']
            return result
        else:
            return None

        # return response

    def save(self, key, content):
        user_key = self.user_key(key)
        if not content:
            content = 'NULL'

        data = {
            'key': user_key,
            'content': str(content),
        }
        response = requests.put(self.db_endpoint, data=data)
        # print(response.text, response.status_code)

        return response.status_code

    def delete(self, key):
        user_key = self.user_key(key)
        data = {
            'key': user_key,
        }
        response = requests.delete(self.db_endpoint, data=data)
        # print(response.text, response.status_code)

        return response.status_code
