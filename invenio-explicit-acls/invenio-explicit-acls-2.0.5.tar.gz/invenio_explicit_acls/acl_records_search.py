#
# Copyright (c) 2019 UCT Prague.
# 
# acl_records_search.py is part of Invenio Explicit ACLs 
# (see https://github.com/oarepo/invenio-explicit-acls).
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Implementation of acl-enabled RecordSearch."""
import json
import logging

from elasticsearch_dsl.query import Bool, Nested, Q, Term
from flask_login import current_user
from invenio_search import RecordsSearch
from invenio_search.api import MinShouldMatch

from invenio_explicit_acls.models import Actor
from invenio_explicit_acls.proxies import current_explicit_acls

logger = logging.getLogger(__name__)

ACL_MATCHED_QUERY = 'invenio_explicit_acls_match'


def _make_list_default(value, defval):
    """
    Converts value into a list and uses default if the value is not passed.

    :param value: a single value (that will be converted into a list with one item) or a list or tuple of values
    :param defval:    the default that is used if value is empty
    :return: list of values
    """
    if value and not isinstance(value, tuple) and not isinstance(value, list):
        value = (value,)
    return list(value or defval)


class ACLDefaultFilter:
    """Default filter for explicit ACLs."""

    operations = ('get',)

    def __init__(self, operation=None):
        """
        Creates a new filter.

        :param operation: either a single string or multiple strings in a list or tuple.
                          if not filled in, 'get' will be used
        """
        self.operations = _make_list_default(operation, ACLDefaultFilter.operations)

    def create_query(self, operation=None):
        """
        Creates a ES query that matches current user against ACL Actors cached on the resource having the given operation.

        :param operation:   same meaning as in the constructor, if not used value from the constructor is taken
        :return:            ES "bool" query
        """
        actor_query_part = []
        operations = _make_list_default(operation, self.operations)

        # for each registered Actor class get its ES query
        assert current_user is not None, 'Current_user must be set in order to create ACL query'
        for actor_model in current_explicit_acls.actor_models:  # type: Actor
            q = actor_model.get_elasticsearch_query(current_user)
            if q:
                actor_query_part.append(q)

        if not actor_query_part:        # pragma no cover
            # no actor means to always return an empty set. Should not get here as SystemRoleActor in invenio
            # always returns any_user or authenticated_user
            logger.error('Should not get here, do you have invenio-access enabled?')
            return ~Q('match_all')

        # combine actor queries into a single bool query if needed
        queries = []
        if len(actor_query_part) == 1:
            actor_query_part = actor_query_part[0]
        else:
            actor_query_part = Bool(
                minimum_should_match=1,
                should=actor_query_part
            )

        # create ES query composed from the operation and actor part
        for operation in operations:
            queries.append(
                Nested(
                    path='_invenio_explicit_acls',
                    _name=f'{ACL_MATCHED_QUERY}_{operation}',
                    query=Bool(
                        must=[
                            Term(_invenio_explicit_acls__operation=operation),
                            actor_query_part
                        ]
                    )
                )
            )
        query = Bool(should=queries, minimum_should_match=1)

        if logger.isEnabledFor(logging.DEBUG):      # pragma no cover
            logger.debug('Query: %s', query.to_dict())
        return query


class ACLRecordsSearch(RecordsSearch):
    """ACL enabled RecordsSearch."""

    def __init__(self, operation=None, **kwargs):
        """
        Creates a new instance.

        :param operation: the operation that should be checked
        :param kwargs:    the rest of args for RecordsSearch
        """
        super().__init__(**kwargs)
        self.acl_operation = operation
        acl_filter = self._get_acl_filter()
        self.query = Bool(minimum_should_match=MinShouldMatch("100%"),
                          filter=acl_filter.create_query(operation=operation))

    def _get_acl_filter(self) -> ACLDefaultFilter:
        """
        Gets implementation of ACL enabled DefaultFilter.

        internal

        :return: returns either configured acl_filter from Meta
                (in case user needs to customize it) or the default ACL Filter.
        """
        acl_filter = getattr(self.Meta, 'acl_filter', None) or ACLDefaultFilter()
        return acl_filter

    def acl_return_all(self, operation=None):
        """
        Returns all the matched results regardless of their acls (the default is to return only those resources for which ACLs match).

        For each returned record marks if it matched ACLs.
        Internally uses ES named query with name "invenio_explicit_acls_match", so the records with matched ACLs
        will contain the following element in "hits":

        "matched_queries": [
            "invenio_explicit_acls_match_{operation}"
        ]
        :param operation:   optional operation; if not specified the one passed to the constructor is used
        :return:    self so that it can be used in pipes.

        Sample usage:

        resp = ACLRecordsSearch(...).acl_return_all(operation='get').query(Term(a=1)).execute()
        """
        acl_filter = self._get_acl_filter()
        self.query = Bool(minimum_should_match=MinShouldMatch(0),
                          should=acl_filter.create_query(operation=operation or self.acl_operation))
        return self
