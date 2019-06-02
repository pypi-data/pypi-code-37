# @Vendors
from collections import Counter

def tuple_word_list_to_counter(tuple_list):
    counter = Counter()
    if not tuple_list:
        return counter
    for word, count in tuple_list:
        counter[word.lower()] += count
    return counter
