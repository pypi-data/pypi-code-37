# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
from django.http.response import HttpResponse
from django.views.generic.base import View
from payu_api.classes import PayuApiError
from payu_api.conf import settings
import hashlib
import json
import logging
from payu_api import get_payment_model

class NotifyView(View):

    def post(self, request, *args, **kwargs):
        assert 'application/json' in request.META['CONTENT_TYPE']
        model = get_payment_model()

        try:
            data = json.loads(request.body)
            header = request.META['HTTP_OPENPAYU_SIGNATURE']
        except KeyError:
            raise PayuApiError('Malformed POST')

        header_data_raw = header.split(';')
        header_data = {}
        for x in header_data_raw:
            key, value = x.split('=')[0], x.split('=')[1]
            header_data[key] = value

        try:
            payment = model.objects.get(payu_order_id = data['order']['orderId'])
        except model.DoesNotExist:
            raise PayuApiError('PaymentDoesNotExist (local?)')

        incoming_signature = header_data['signature']
        algorithm = header_data['algorithm']

        if algorithm == 'MD5':
            m = hashlib.md5()
            key = settings.PAYU_API_SECOND_KEY
            signature = request.body + str(key)
            m.update(signature)
            signature = m.hexdigest()
            if incoming_signature == signature and not payment.status == model.COMPLETED:
                status = data['order']['status']
                payment.change_status(new_status = getattr(model, status))
                payment.save()
                return HttpResponse("ok", status = 200)
        else:
            return HttpResponse("not ok", status = 500)

    def get(self, request, *args, **kwargs):
        return HttpResponse("Forbidden", status = 403)
