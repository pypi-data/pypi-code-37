# -*- coding: utf-8 -*-
import json
from payu_api.conf import settings
import requests
import ast
from django.http.response import Http404
from decimal import Decimal
from payu_api import get_payment_model
from django.utils import timezone

class PayuApiError(Exception):
    pass

class PayuApi(object):
    "Klasa odpowiedzialna za komunikację z PayU REST Api"

    def __init__(self, pos_id = settings.PAYU_API_POS_ID, client_secret = settings.PAYU_API_CLIENT_SECRET, grant_type = 'client_credentials'):
        self.payu_auth_url = settings.PAYU_API_AUTH_URL
        self.payu_delete_token_url = settings.PAYU_API_DELETE_TOKEN_URL
        self.payu_api_order_url = settings.PAYU_API_ORDER_URL
        self.payu_api_paymethods_url = settings.PAYU_API_PAYMETHODS_URL

        self.token = self.get_access_token(pos_id, client_secret, grant_type)
        self.pos_id = pos_id

    # Methods for authenticating our API connection (getting token)

    def get_access_token(self, client_id, client_secret, grant_type):
        "Metoda która pobiera access_token potrzebny do dalszej komunikacji z API"

        payu_auth_url = self.payu_auth_url
        data = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
        }
        headers = {
           'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(payu_auth_url, data = data, headers = headers)

        try:
            return json.loads(response.text)['access_token']
        except KeyError:
            raise PayuApiError(response.text)

    def delete_token(self):
        "Metoda która dezaktywuje access_token"

        payu_delete_token_url = self.payu_delete_token_url + self.token
        headers = {
          'Authorization': 'Bearer %s' % self.token,
        }

        response = requests.delete(payu_delete_token_url, headers = headers)
        self.token = None

        return (response.status_code == 204)

    # Close API instance if no longer needed

    def close(self):
        "Metoda wywoływana na instancji PayuApi zamykająca połączenie (usuwa token)"

        self.delete_token()

    # Method for sending an order (creates a Payment object, return redirectUrl)

    def create_order(self, payment_processor):
        "Metoda tworząca zamówienie i zwracająca link do przekierowania"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self.token,
        }

        payment = payment_processor.as_payment_obj()
        payment_processor.pos_id = self.pos_id

        response = requests.post(self.payu_api_order_url, data = payment_processor.as_json(), headers = headers, allow_redirects = False)
        response_dict = json.loads(response.text)



        self.close()

        try:
            payment.payu_order_id = response_dict['orderId']

            if response_dict['status']['statusCode'] == u'SUCCESS':
                payment.pay_link = response_dict['redirectUri']
                payment.save()
                return response_dict['redirectUri']
            else:
                raise PayuApiError(response.text)

        except KeyError:
            raise PayuApiError(response.text)


    # Method that returns all pay methods

    def get_paymethod_tokens(self):
        "Metoda pobierająca dostępne metody płatności dla POS'a"

        headers = {
          'Authorization': 'Bearer %s' % self.token
        }

        response = requests.get(self.payu_api_paymethods_url, headers = headers)
        return response

    # Method that rejects the order

    def reject_order(self, payu_order_id):
        "Metoda anulująca zamówienie"

        headers = {
            'Authorization': 'Bearer %s' % self.token,
        }

        url = self.payu_api_order_url
        if url.endswith('/'):
            url += payu_order_id
        else:
            url += '/'
            url += payu_order_id

        try:
            # Aby skutecznie zwrócić środki do płacącego, w przypadku zamówienia w statusie
            # WAITING_FOR_CONFIRMATION należy wykonać dwa żądania DELETE.
            # http://developers.payu.com/pl/restapi.html#cancellation
            response1 = json.loads(requests.delete(url, headers = headers).text)
            response2 = json.loads(requests.delete(url, headers = headers).text)

            if response1['status']['statusCode'] == response2['status']['statusCode'] == 'SUCCESS':
                model = get_payment_model()
                model.objects.get(payu_order_id = payu_order_id).change_status(model.REJECTED)

                return True
            else:
                raise PayuApiError(response1.text, response2.text)
        except:
            return False

class PaymentProcessor(object):
    "Klasa która służy za pośrednika między API a modelem zamówienia głównego projektu."

    def __init__(self, **kwargs):
        self.order = kwargs.get('order')
        self.notify_url = kwargs.get('notify_url', settings.PAYU_API_NOTIFY_URL)
        self.currency = kwargs.get('currency', settings.PAYU_API_CURRENCY)
        self.description = kwargs.get('description')
        self.customer_ip = kwargs.get('customer_ip')
        self.order_items = []
        self.external_id = None
        self.pos_id = None
        self.total = None

    def add_order_items(self, obj):
        "Dodaj pozycje zamówienia, przyjmuje instancje klasy OrderItem"
        if isinstance(obj, OrderItem):
            self.order_items.append(obj)
        elif isinstance(obj, type([])):
            self.order_items.extend(obj)
        else:
            raise PayuApiError("Zły format order_item. Funkcja add_order_items przyjmuje obiekt OrderItem lub listę złożoną z instancji klasy OrderItem.")

    def set_paymethod(self, value, type = "PBL"):
        "Ustaw metodę płatności, przy przezroczystej integracji. Na podstawie PayuApi.get_paymethod_tokens()"
        if not hasattr(self, 'paymethods'):
            self.paymethods = {}
            self.paymethods['payMethod'] = {'type': type, 'value': value}

    def set_buyer_data(self, first_name, last_name, email, phone, lang_code = 'pl'):
        "Ustaw dane kupującego"
        if not hasattr(self, 'buyer'):
            self.buyer = {
                'email': email,
                'phone': phone,
                'firstName': first_name,
                'lastName': last_name,
                'language': lang_code
            }

    def set_continue_url(self, continue_url):
        "Ustaw link na który użytkownik zostanie przekierowany po płatności"
        if not hasattr(self, 'continueUrl'):
            self.continueUrl = continue_url

    def set_validity_time(self, validity_time = 60 * 60 * 24 * 5):
        # 5 days
        "Ustaw czas wygaśnięcia linku do płatności (przy PayUbyLink)"
        if not hasattr(self, 'validityTime'):
            self.validityTime = int(validity_time)

    def get_total(self):
        "Pobierz wartość zamówienia"
        total = Decimal(0)
        for i in self.order_items:
            total += i.unit_price * Decimal(i.quantity)

        return total

    def as_json(self):
        "Zwraca zawartość obiektu do formatu json w formacie przyjmowanym przez PayU"
        total = 0
        products = []


        for i in self.order_items:
            total += i.unit_price * i.quantity
            i.sub_unit = settings.PAYU_API_CURRENCY_DATA[self.currency]['sub_unit']
            products.append(i.as_dict())

        self.total = int(total * settings.PAYU_API_CURRENCY_DATA[self.currency]['sub_unit'])

        json_dict = {
            'notifyUrl': self.notify_url,
            'customerIp': self.customer_ip,
#            'extOrderId': self.external_id,
            'merchantPosId': self.pos_id,
            'description': self.description,
            'currencyCode': self.currency,
            'totalAmount': self.total,
            'products': products,
        }

        # additional data
        if hasattr(self, 'paymethods'):
            json_dict['payMethods'] = self.paymethods

        if hasattr(self, 'buyer'):
            json_dict['buyer'] = self.buyer

        if hasattr(self, 'continueUrl'):
            json_dict['continueUrl'] = self.continueUrl

        if hasattr(self, 'validityTime'):
            json_dict['validityTime'] = self.validityTime

        return json.dumps(json_dict)

    def as_payment_obj(self):
        "Tworzy i zwraca obiekt Payment"
        model = get_payment_model()
        payment = model(amount = self.get_total(), currency = self.currency, order = self.order)
        if hasattr(self, 'validityTime'):
            payment.pay_link_valid_until = timezone.now() + timezone.timedelta(seconds = self.validityTime)
        payment.save()
        payment.change_status(model.NEW)
        return payment

class OrderItem(object):
    "Klasa która służy jako pośrednik między pozycjami zamówienia a PaymentProcessorem"

    def __init__(self, *args, **kwargs):
        super(OrderItem, self)
        self.quantity = 1
        if kwargs:
            if 'name' in kwargs:
                self.name = kwargs['name']

            if 'unit_price' in kwargs:
                self.unit_price = Decimal(kwargs['unit_price'])

            if 'quantity' in kwargs:
                self.quantity = int(kwargs['quantity'])

    def as_dict(self):
        return {
           'name': self.name,
           'unitPrice': str(int(self.unit_price * self.sub_unit)),
           'quantity': str(self.quantity)
        }
