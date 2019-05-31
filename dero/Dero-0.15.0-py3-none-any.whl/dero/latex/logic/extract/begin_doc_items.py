from dero.latex.typing import ListOrDictOrItem, StrListOrNone, AnyItem
from dero.latex.logic.extract.docitems import is_latex_item


def get_begin_doc_items_from_items(content: ListOrDictOrItem) -> StrListOrNone:
    begin_doc_items = []
    if isinstance(content, (list, tuple)):
        for item in content:
            if _has_begin_doc_items(item):
                begin_doc_items += item.begin_doc_items
    elif isinstance(content, dict):
        for name, item in content.items():
            if _has_begin_doc_items(item):
                begin_doc_items += item.begin_doc_items
    elif is_latex_item(content):
        if _has_begin_doc_items(content):
            begin_doc_items += content.begin_doc_items

    if begin_doc_items == []:
        return None

    return begin_doc_items

def _has_begin_doc_items(item: AnyItem) -> bool:
    return is_latex_item(item) and hasattr(item, 'begin_doc_items') and item.begin_doc_items is not None