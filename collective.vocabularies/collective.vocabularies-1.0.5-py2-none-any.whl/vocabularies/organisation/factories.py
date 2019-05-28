from plone import api
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides
from zope.interface import provider
from plone.app.vocabularies.catalog import KeywordsVocabulary

from . import vocab
from collective.vocabularies.utils import vocab_query


@provider(IVocabularyFactory)
def organisation_type_factory(context):
    return SimpleVocabulary.fromValues(vocab.organisation_types)


@provider(IVocabularyFactory)
def organisation_sizes_factory(context):
    return SimpleVocabulary(
        [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in vocab.organisation_sizes ]
    )


@provider(IVocabularyFactory)
def industry_factory(context, query=None):
    return vocab_query(vocab.industries, query)