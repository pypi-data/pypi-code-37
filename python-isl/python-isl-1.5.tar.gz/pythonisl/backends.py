from django.contrib.auth import get_user_model

User = get_user_model()


class ISLAuthBackend(object):

    def authenticate(self, email):

        (username, domain) = email.split('@')

        try:
            try:
                user = User.objects.get(email=email)
            except User.MultipleObjectsReturned:
                user = User.objects.get(username=username, email=email)
        except User.DoesNotExist:
            user = User.objects.create(username=username, email=email)
            user.set_unusable_password()
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass
