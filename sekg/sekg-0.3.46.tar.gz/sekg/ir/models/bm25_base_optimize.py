#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""This module contains function of computing rank scores for documents in
corpus and helper class `BM25` used in calculations. Original algorithm
descibed in [1]_, also you may check Wikipedia page [2]_.


.. [1] Robertson, Stephen; Zaragoza, Hugo (2009).  The Probabilistic Relevance Framework: BM25 and Beyond,
       http://www.staff.city.ac.uk/~sb317/papers/foundations_bm25_review.pdf
.. [2] Okapi BM25 on Wikipedia, https://en.wikipedia.org/wiki/Okapi_BM25



Examples
--------

.. sourcecode:: pycon

    # >>> from gensim.summarization.bm25 import get_bm25_weights
    # >>> corpus = [
    # ...     ["black", "cat", "white", "cat"],
    # ...     ["cat", "outer", "space"],
    # ...     ["wag", "dog"]
    # ... ]
    # >>> result = get_bm25_weights(corpus, n_jobs=-1)


Data:
-----
.. data:: PARAM_K1 - Free smoothing parameter for BM25.
.. data:: PARAM_B - Free smoothing parameter for BM25.
.. data:: EPSILON - Constant used for negative idf of document in corpus.

"""

import math
from six import iteritems
from six.moves import range
from functools import partial
from multiprocessing import Pool
from gensim.utils import effective_n_jobs
import numpy as np

# from ..utils import effective_n_jobs

PARAM_K1 = 1.5
PARAM_B = 0.75
EPSILON = 0.25


class BM25(object):
    """Implementation of Best Matching 25 ranking function.

    Attributes
    ----------
    corpus_size : int
        Size of corpus (number of documents).
    avgdl : float
        Average length of document in `corpus`.
    doc_freqs : list of dicts of int
        Dictionary with terms frequencies for each document in `corpus`. Words used as keys and frequencies as values.
    idf : dict
        Dictionary with inversed documents frequencies for whole `corpus`. Words used as keys and frequencies as values.
    doc_len : list of int
        List of document lengths.
    """

    def __init__(self, corpus):
        """
        Parameters
        ----------
        corpus : list of list of str
            Given corpus.

        """
        self.corpus_size = len(corpus)
        self.avgdl = 0
        self.doc_freqs = []
        self.idf = {}
        self.wf = {}
        self.doc_len = []
        self._initialize(corpus)
        self.word2score = {}
        self.K = PARAM_K1 * (1 - PARAM_B + PARAM_B * np.array(self.doc_len) / self.avgdl)  # document*1
        self.k1 = PARAM_K1 + 1

    def _initialize(self, corpus):
        """Calculates frequencies of terms in documents and in corpus. Also computes inverse document frequencies."""
        # words = list(set([y for x in corpus for y in x]))
        nd = {}  # word -> number of documents with word
        num_doc = 0
        for index, document in enumerate(corpus):
            self.doc_len.append(len(document))
            num_doc += len(document)
            # all_frequencies = dict(zip(words, [0] * len(words)))

            frequencies = {}
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
                # all_frequencies[word] += 1
            self.doc_freqs.append(frequencies)

            for word in frequencies:
                if word not in self.wf.keys():
                    self.wf[word] = [0] * self.corpus_size
                self.wf[word][index] = frequencies[word]
                if word not in nd:
                    nd[word] = 0
                nd[word] += 1
        self.avgdl = float(num_doc) / self.corpus_size
        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in iteritems(nd):
            idf = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = float(idf_sum) / len(self.idf)

        eps = EPSILON * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps

    def _initialize_with_bow(self, corpus):
        """Calculates frequencies of terms in documents and in corpus. Also computes inverse document frequencies."""
        nd = {}  # word -> number of documents with word
        num_doc = 0
        for index, document in enumerate(corpus):
            self.doc_len.append(len(document))
            frequencies = {}
            for word, fre in document:
                num_doc += fre
                frequencies[word] += fre
                if word not in nd:
                    nd[word] = 0
                nd[word] += 1
                if word not in self.wf.keys():
                    self.wf[word] = [0] * self.corpus_size
                self.wf[word][index] = frequencies[word]
            self.doc_freqs.append(frequencies)
        self.avgdl = float(num_doc) / self.corpus_size
        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in iteritems(nd):
            idf = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = float(idf_sum) / len(self.idf)
        eps = EPSILON * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps

    def get_score_for_one_word(self, word_one):
        """Calculates score for one word."""
        if word_one not in self.idf.keys():
            return np.zeros(self.corpus_size)
        idf = self.idf[word_one]  # 1*1
        fre_arrry = np.array(self.wf.get(word_one, [0] * self.corpus_size))  # document*1
        corups_arry = fre_arrry * self.k1 / (fre_arrry + self.K) * idf
        return corups_arry

    def calculate_scores(self, document):
        """Calculates scores for the whole query."""
        idf_array = np.empty(len(document))  # query_word * 1
        fre_arrry = np.empty((len(document), self.corpus_size))  # query_word * corpus_size
        for index, word in enumerate(document):
            idf_array[index] = self.idf.get(word, 0)
            fre_arrry[index] = self.wf.get(word, [0] * self.corpus_size)
        fre_arrry = fre_arrry.T  # corpus_size * query_word
        K = self.K.repeat(idf_array.size).reshape((self.corpus_size, idf_array.size))  # extend to corpus_size * word
        all_score = np.sum(fre_arrry * self.k1 / (fre_arrry + K) * idf_array, 1)  # corpus_size * 1
        return all_score

    def get_scores(self, document):
        """Computes and returns BM25 scores of given `document` in relation to
        every item in corpus.

        Parameters
        ----------
        document : list of str
            Document to be scored.

        Returns
        -------
        list of float
            BM25 scores.

        """
        # score_array = np.zeros(self.corpus_size)
        # for word in document:
        #     if word not in self.word2score.keys():
        #         # score_word_1 = self.get_scores_ori([word])
        #         score_word = self.get_score_for_one_word(word)
        #         score_array = score_array + score_word
        #         self.word2score[word] = score_word
        #     else:
        #         score_array = score_array + self.word2score[word]
        # return score_array
        return self.calculate_scores(document)

    def get_score(self, document, index):
        """Computes BM25 score of given `document` in relation to item of corpus selected by `index`.

        Parameters
        ----------
        document : list of str
            Document to be scored.
        index : int
            Index of document in corpus selected to score with `document`.

        Returns
        -------
        float
            BM25 score.

        """
        score = 0
        doc_freqs = self.doc_freqs[index]
        for word in document:
            if word not in doc_freqs:
                continue
            score += (self.idf[word] * doc_freqs[word] * self.k1
                      / (doc_freqs[word] + self.K[index]))
        return score

    def get_scores_ori(self, document):
        """Computes and returns BM25 scores of given `document` in relation to
        every item in corpus.

        Parameters
        ----------
        document : list of str
            Document to be scored.

        Returns
        -------
        list of float
            BM25 scores.

        """
        scores = np.array([self.get_score(document, index) for index in range(self.corpus_size)])
        return scores

    def get_scores_bow(self, document):
        """Computes and returns BM25 scores of given `document` in relation to
        every item in corpus.

        Parameters
        ----------
        document : list of str
            Document to be scored.

        Returns
        -------
        list of float
            BM25 scores.

        """
        scores = []
        for index in range(self.corpus_size):
            score = self.get_score(document, index)
            if score > 0:
                scores.append((index, score))
        return scores


def _get_scores_bow(bm25, document):
    """Helper function for retrieving bm25 scores of given `document` in parallel
    in relation to every item in corpus.

    Parameters
    ----------
    bm25 : BM25 object
        BM25 object fitted on the corpus where documents are retrieved.
    document : list of str
        Document to be scored.

    Returns
    -------
    list of (index, float)
        BM25 scores in a bag of weights format.

    """
    return bm25.get_scores_bow(document)


def _get_scores(bm25, document):
    """Helper function for retrieving bm25 scores of given `document` in parallel
    in relation to every item in corpus.

    Parameters
    ----------
    bm25 : BM25 object
        BM25 object fitted on the corpus where documents are retrieved.
    document : list of str
        Document to be scored.

    Returns
    -------
    list of float
        BM25 scores.

    """
    return bm25.get_scores(document)


def iter_bm25_bow(corpus, n_jobs=1):
    """Yield BM25 scores (weights) of documents in corpus.
    Each document has to be weighted with every document in given corpus.

    Parameters
    ----------
    corpus : list of list of str
        Corpus of documents.
    n_jobs : int
        The number of processes to use for computing bm25.

    Yields
    -------
    list of (index, float)
        BM25 scores in bag of weights format.

    Examples
    --------
    .. sourcecode:: pycon

        # >>> from gensim.summarization.bm25 import iter_bm25_weights
        # >>> corpus = [
        # ...     ["black", "cat", "white", "cat"],
        # ...     ["cat", "outer", "space"],
        # ...     ["wag", "dog"]
        # ... ]
        # >>> result = iter_bm25_weights(corpus, n_jobs=-1)

    """
    bm25 = BM25(corpus)

    n_processes = effective_n_jobs(n_jobs)
    if n_processes == 1:
        for doc in corpus:
            yield bm25.get_scores_bow(doc)
        return

    get_score = partial(_get_scores_bow, bm25)
    pool = Pool(n_processes)

    for bow in pool.imap(get_score, corpus):
        yield bow
    pool.close()
    pool.join()


def get_bm25_weights(corpus, n_jobs=1):
    """Returns BM25 scores (weights) of documents in corpus.
    Each document has to be weighted with every document in given corpus.

    Parameters
    ----------
    corpus : list of list of str
        Corpus of documents.
    n_jobs : int
        The number of processes to use for computing bm25.

    Returns
    -------
    list of list of float
        BM25 scores.

    Examples
    --------
    .. sourcecode:: pycon

        # >>> from gensim.summarization.bm25 import get_bm25_weights
        # >>> corpus = [
        # ...     ["black", "cat", "white", "cat"],
        # ...     ["cat", "outer", "space"],
        # ...     ["wag", "dog"]
        # ... ]
        # >>> result = get_bm25_weights(corpus, n_jobs=-1)

    """
    bm25 = BM25(corpus)

    n_processes = effective_n_jobs(n_jobs)
    if n_processes == 1:
        weights = [bm25.get_scores(doc) for doc in corpus]
        return weights

    get_score = partial(_get_scores, bm25)
    pool = Pool(n_processes)
    weights = pool.map(get_score, corpus)
    pool.close()
    pool.join()
    return weights
