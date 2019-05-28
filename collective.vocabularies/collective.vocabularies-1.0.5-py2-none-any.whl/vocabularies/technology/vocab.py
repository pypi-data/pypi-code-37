import os
import json
import logging
from plone import api
from urllib2 import quote
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides
from zope.interface import provider
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from plone.app.vocabularies.catalog import KeywordsVocabulary

from collective.vocabularies.technology import (
    DATABASE_DIR,
    ALT_DATABASE_DIR
)


logger = logging.getLogger("Plone")
platform_types = ['Desktop', 'Mobile', 'Web']


@provider(IVocabularyFactory)
def platform_type_factory(context):
    items = [
        SimpleTerm(value=it, title=it)
        for it in platform_types
    ]
    return SimpleVocabulary(items)


@provider(IVocabularyFactory)
def programming_languages(context, query=None):
    items = []
    data_filename = 'programming_languages.json'
    db_path = os.path.join(DATABASE_DIR, data_filename)
    if not os.path.exists(db_path):
        db_path = os.path.join(ALT_DATABASE_DIR, data_filename)
        if not os.path.exists(db_path):
            db_path = None
    if db_path is not None:
        with open(db_path, 'r') as dp:
            data = json.load(dp)
    
        lang = api.portal.get_current_language()
        normalizer = getUtility(IIDNormalizer)
        for item in data["itemListElement"]:
            pln = item['item']['name']
            try:
                dpl = pln.decode('utf-8')
                pl = api.portal.translate(
                    pln,
                    lang=lang
                )
                items.append((pl, pl))
            except Exception as e:
                message = u"{} Progamming Language - {}".format(
                    quote(pln.encode('utf-8')), e
                )
                print message
                logger.info(message)
                continue
        items.sort(key=lambda it: normalizer.normalize(it[1], locale=lang))
    
    if query is None:
        items = [
            SimpleTerm(value=it[0], title=it[1])
            for it in items
        ]
    else:
        items = [
            SimpleTerm(value=it[0], title=it[1])
            for it in items if query.lower() in it[1].lower()
        ]
    return SimpleVocabulary(items)


