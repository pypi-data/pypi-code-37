from . import bac, cha, cyb, cza, hjc, joa, kab, kka, kta, kyi, kza, sed, skb, srb, tyb, ukc
from . import ot, ou, ow, oz

schema_list = {
    'bac': bac.schema,
    'cha': cha.schema,
    'cyb': cyb.schema,
    'cza': cza.schema,
    'hjc': hjc.schema,
    'joa': joa.schema,
    'kab': kab.schema,
    'kka': kka.schema,
    'kta': kta.schema,
    'kyi': kyi.schema,
    'kza': kza.schema,
    'ot': ot.schema,
    'ou': ou.schema,
    'ow': ow.schema,
    'oz': oz.schema,
    'sed': sed.schema,
    'skb': skb.schema,
    'srb': srb.schema,
    'tyb': tyb.schema,
    'ukc': ukc.schema,
    'zed': sed.schema,
    'zkb': skb.schema
}


def has(schema_type):
    return True if schema_type in schema_list else False


def get(schema_type):
    return schema_list[schema_type]
