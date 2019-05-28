from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def vocab_query(terms, query=None):
    if query is None:
        return SimpleVocabulary([
            SimpleTerm(value=term, title=term) for term in terms
        ])
    return SimpleVocabulary([
        SimpleTerm(value=term, title=term) for term in terms if query.lower() in term.lower()
    ])