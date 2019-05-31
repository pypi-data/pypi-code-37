import requests

DYNAMO_ENDPOINT = 'http://10.0.1.104:5000/scrap_book'


class ScrapBook(object):
    db_endpoint = DYNAMO_ENDPOINT

    def get(self, key):
        params = {
            'key': key
        }
        response = requests.get(self.db_endpoint, params=params)
        print(response.text, response.status_code)

        return response

    def save(self, key, content):
        data = {
            'key': key,
            'content': content,
        }
        response = requests.put(self.db_endpoint, data=data)
        print(response.text, response.status_code)

        return response

    def delete(self, key):
        data = {
            'key': key,
        }
        response = requests.delete(self.db_endpoint, data=data)
        print(response.text, response.status_code)

        return response
