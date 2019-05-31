import hashlib
import urllib
from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Patch
from .resource import Update
from .resource import Delete


class User(List, Find, Create, Post, Update, Delete, Patch):
    """User class wrapping the REST nodes endpoint
    """
    path = "users"

    def gravatar(self, size=64):
        """Deprecated: return the Gravatar URL.

        .. deprecated::
            Use of Gravatar is deprecated, in favour of our self-hosted avatars.
            See pillar.api.users.avatar.url(user).
        """
        parameters = {'s':str(size), 'd':'mm'}
        return "https://www.gravatar.com/avatar/" + \
            hashlib.md5(self.email.lower()).hexdigest() + \
            "?" + urllib.urlencode(parameters)

    @classmethod
    def me(cls, params=None, api=None):
        """Returns info about the current user, identified by auth token."""

        return cls.find_from_endpoint('/users/me', params=params, api=api)

    def set_username(self, new_username: str, api):
        """PATCH the user to set the new username."""

        self.username = new_username
        return self.patch({'op': 'set-username', 'username': new_username},
                          api=api)
