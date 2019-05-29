VERSION = '1.0.5'


def get_payment_model():
    from django.apps import apps as django_apps
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured

    constant_name = 'PAYU_API_PAYMENT_MODEL'
    constant_value = getattr(settings, constant_name)

    try:
        return django_apps.get_model(constant_value)
    except AttributeError:
        raise ImproperlyConfigured("%s needs to be defined in settings as 'app_label.model_name'" % constant_name)
    except ValueError:
        raise ImproperlyConfigured("%s must be of the form 'app_label.model_name'" % constant_name)
    except LookupError:
        raise ImproperlyConfigured("%s refers to model '%s' that has not been installed" % (constant_name, constant_value))
