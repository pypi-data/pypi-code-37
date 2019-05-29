from django.dispatch import Signal

rest_new_payment = Signal(providing_args = ['order', 'payment'])
rest_new_payment.__doc__ = """Sent after creating new payment."""


rest_payment_status_changed = Signal(providing_args = ['old_status', 'new_status'])
rest_payment_status_changed.__doc__ = """Sent when Payment status changes."""


rest_order_additional_validation = Signal(providing_args = ['request',
                                                     'order',
                                                     'backend'])
rest_order_additional_validation.__doc__ = """
A hook for additional validation of an order.
Sent after PaymentMethodForm is submitted but before
Payment is created and before user is redirected to payment gateway.
Backend views can also sent it.
It is expected for this signal to raise ValidationError.
"""


rest_redirecting_to_payment_gateway_signal = Signal(providing_args = ['request', 'order', 'payment', 'backend'])
rest_redirecting_to_payment_gateway_signal.__doc__ = """
Sent just a moment before redirecting. A hook for analytics tools.
"""
