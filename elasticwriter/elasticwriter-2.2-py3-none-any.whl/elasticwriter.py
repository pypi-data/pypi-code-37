# -*- coding: utf-8 -*-

from elastictools.doctools import DocTools

DEFAULT_SETTING = {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "mapping": {
                "total_fields": {
                    "limit": "1000"
                }
            },
        }
    }


def get_es(es_config=[]):
    es = DocTools(es_config)
    return es


def create_index(es, index_name, mapping={}, settings=DEFAULT_SETTING, overwrite=True):
    """
    Create index with default settings. 
    By default, overwrite=True, means that it will delete existed index.
    """
    esi = es.indextool()
    try:
        print(mapping)
        if overwrite or not esi.exists(index_name):
            esi.create(index_name, overwrite=True, settings=settings, mapping=mapping) 
        else:
            print('index: {} is existed. If you wanna overwrite it, set overwrite=True'.format(index_name))
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)


def create_index_if_not_existed(es, index_name, mapping={}, settings=DEFAULT_SETTING):
    """
    Create new index if it's not existed with default settings.
    Note:: Deprecated in 2.2 and will be removed in 3.0, use create_index instead.
    """
    esi = es.indextool()
    try:
        print(mapping)
        if not esi.exists(index_name):
            esi.create(index_name, overwrite=True, settings=settings, mapping=mapping) 
        else:
            print('index: {} is existed'.format(index_name))
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def remake_items(items, key_field='es_id'):
    return [{
        '_op_type': 'update',
        '_id': p[key_field],
        'doc': p,
        'doc_as_upsert' : True
    } for p in items]


def push_df_to_index(es, index_name, df, mode='overwrite', append_key='es_id', chunk_size = 60000, thread_count=4, request_timeout=20):
    collected = df.collect()
    chunk_data = [row.asDict() for row in collected]
    push_list_dict_to_index(es, index_name, chunk_data, mode, append_key, chunk_size, thread_count, request_timeout)


def push_list_dict_to_index(es, index_name, list_dict, mode='overwrite', append_key='es_id', chunk_size = 60000, thread_count=4, request_timeout=20):
    for items in chunks(list_dict, chunk_size):
        if mode == 'append':
            res = es.bulk(index_name, items, chunk_size=chunk_size//thread_count, thread_count=thread_count, doctype='', check_index_existed=False)
        else:
            print("items len: {}".format(len(items)))
            res = es.bulk(index_name, remake_items(items, append_key), chunk_size=chunk_size//thread_count, thread_count=thread_count, 
                          doctype='', check_index_existed=False, request_timeout=request_timeout)
