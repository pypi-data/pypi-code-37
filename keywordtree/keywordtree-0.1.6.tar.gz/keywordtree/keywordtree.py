def _tokenizer(query):
    return query.lower().split()


class KeywordTree:
    """
    Data structure that maps arbitrary text to values by using a
    decision-tree-like algorithm based on counting keyword occurrences.

    Each node contains a list of keywords and a value if it's a leaf.
    A query is given as a string and is broken into tokens by a
    tokenizer. Starting from the root, the query follows the child with
    the most keywords present in the query token list. When a leaf is
    reached, its value is returned. If there are multiple nodes with
    the most keywords in the token list, the query follows all of them
    and the results are merged at the end into a list.

    Parameters:
        - keywords: List of keywords (strings).
        - children: List of immediate children of root node in the form
        of (keywords, children, value) tuples.
        - value: Value of node (must be None for all non-leaf nodes).
        - tokenizer: Function that will be used in queries to convert
        the query text to a list of tokens, unless overridden (see
        `query` method). The default tokenizer converts the query text
        to lowercase and then splits it using whitespace as separator.

    Example:
        Let's say we have the following tree:
                           ┌────────────┐
                           │   kw: []   │
                           └────────────┘
                   ┌──────────────┴─────────────┐
        ┌─────────────────────┐       ┌─────────────────────┐
        │ kw: ['dog', 'woof'] │       │ kw: ['cat', 'meow'] │
        │     value: '🐶'     │       │      value: '🐱'    │
        └─────────────────────┘       └─────────────────────┘

        The corresponding KeywordTree is:
        >>> kt = KeywordTree([], [
        ...     (['dog', 'woof'], [], '🐶'),
        ...     (['cat', 'meow'], [], '🐱'),
        ... ], None)
        >>> kt.query('Cat goes meow')
        ['🐱']
    """
    def __init__(self, keywords, children, value, tokenizer=_tokenizer):
        self.root = KeywordTreeNode(keywords, children, value)
        self.tokenizer = tokenizer

    def query(self, q, *, tokenizer=None, include_node=False):
        """
        Performs a query.

        Args:
            - q: The query text.
            - tokenizer: If provided, it will be used instead of the
            default tokenizer given in the constructor.
            - include_node: If true, the returned list will consist
            of (node value, node) tuples instead of the default list of
            plain values.

        Returns:
            List of values from nodes that were matched. If
            include_node is set to true, the list will consist of
            (node value, node) tuples instead.
        """
        if tokenizer is None:
            tokenizer = self.tokenizer
        return self.root.query(
            tokenizer(q),
            include_node=include_node
        )


class KeywordTreeNode:
    """
    Node of the keyword tree containing keywords to match,
    pointers to children nodes and a value if it's a leaf.
    """
    def __init__(self, keywords, children, value):
        if len(children) > 0 and value is not None:
            raise ValueError('Only leaf nodes can be assigned a value')

        self.keywords = keywords
        self.children = [
            KeywordTreeNode(kws, ch, val)
            for kws, ch, val in children
        ]
        self.value = value

        # Lookup table to speed up queries
        self._kwmap = {}
        for index, child in enumerate(children):
            for kw in child[0]:
                if kw in self._kwmap:
                    self._kwmap[kw].append(index)
                else:
                    self._kwmap[kw] = [index]

    def query(self, tokens, *, include_node=False):
        """
        Chooses child whose keywords match most tokens and
        continues recursively until a leaf node is found.

        Args:
            - tokens: List of tokens that consist the query.
            - include_node: If true, the returned list will consist
            of (node value, node) tuples instead of the default list of
            plain values. 

        Returns:
            List of values from nodes that were matched. If
            include_node is set to true, the list will consist of
            (node value, node) tuples instead.
        """
        if self.value is not None:
            # Leaf node
            if include_node:
                return [(self.value, self)]
            else:
                return [self.value]

        max_matches = 0
        max_index = []
        matches = [0 for child in self.children]

        for token in tokens:
            if token in self._kwmap:
                for index in self._kwmap[token]:
                    matches[index] += 1

        for index, m in enumerate(matches):
            if m > max_matches:
                max_matches = m
                max_index = [index]
            elif m == max_matches:
                max_index.append(index)

        result = []
        for index in max_index:
            result += self.children[index].query(tokens)

        return result
