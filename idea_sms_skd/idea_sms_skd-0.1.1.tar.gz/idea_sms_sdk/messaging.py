import requests

from idea_sms_sdk.utils import CleanPhoneNumber


class SMS(object):
    def __init__(self, partner_id=None, api_key=None, sender_id='IDEASMS',
                 base_url='https://org.ideasms.co.ke'):
        self._partner_id = partner_id
        self._api_key = api_key
        self._base_url = base_url
        self._sender_id = sender_id

        if self._api_key is None or self._api_key.strip() == '':
            raise ValueError("api_key cannot be empty")

        if self._partner_id is None or self._partner_id.strip() == '':
            raise ValueError("partner_id cannot be empty")

        if type(self._partner_id) is not str:
            raise TypeError("partner_id must be a string")

        if type(self._api_key) is not str:
            raise TypeError("api_key must be a string")

        if self._sender_id is not None:
            if type(sender_id) is not str:
                raise TypeError('sender_id must be a string')

    def send_sms(self, phone_numbers=None, message_text=None):

        """
        :param phone_numbers: list of recipients phone numbers eg phone_numbers=['994340340934, '39303409340']
        :param message_text: a text messages you want to send
        :returns json object:

      """

        if type(phone_numbers) is not list:
            raise TypeError("phone_numbers must be a list")
        if len(phone_numbers) == 0:
            raise ValueError('phone_numbers cannot be an empty list')
        if message_text is None or message_text.strip() == '':
            raise ValueError('message_text cannot be empty string')

        payload = {
            'partnerID': self._partner_id,
            'apikey': self._api_key,
            'mobile': ",".join([CleanPhoneNumber(phone).sanitize_phone_number() for phone in phone_numbers]),
            'message': message_text,
            'shortcode': self._sender_id,
            'pass_type': 'plain'
        }

        api_endpoint = "{0}{1}".format(self._base_url, "/api/services/sendsms/")
        headers = {
            'Content-Type': 'application/json'
        }

        r = requests.post(url=api_endpoint, headers=headers, json=payload)
        return r.json()

    def delivery_report(self, message_id):
        """
        :param message_id: str
        :return: json response
        example of response
            {'response-code': 200,
            'message-id': 11757374,
            'response-description': 'Success',
            'delivery-status': 1,
            'delivery-description': 'DeliveredToTerminal',
            'delivery-time': '2019-05-30 16:44:28'
         }
        """
        if type(message_id) is not str:
            raise TypeError('message_id must be a string')
        if message_id is None or message_id.strip() == '':
            raise ValueError('message_id cannot be empty')

        payload = {
            'partnerID': self._partner_id,
            'apikey': self._api_key,
            'messageID': message_id
        }

        api_endpoint = "{0}{1}".format(self._base_url, '/api/services/getdlr/')

        headers = {
            'Content-Type': 'application/json'
        }

        r = requests.post(url=api_endpoint, headers=headers, json=payload)
        return r.json()

    def account_balance(self):
        payload = {
            'partnerID': self._partner_id,
            'apikey': self._api_key
        }

        api_endpoint = "{0}{1}".format(self._base_url, '/api/services/getbalance/')

        headers = {
            'Content-Type': 'application/json'
        }

        r = requests.post(url=api_endpoint, headers=headers, json=payload)
        return r.json()



