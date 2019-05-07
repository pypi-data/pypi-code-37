# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
import random
import time
import math
import types
import operator
import numbers
from enum import Enum

from esrally import exceptions
from esrally.track import track
from esrally.utils import io

__PARAM_SOURCES_BY_OP = {}
__PARAM_SOURCES_BY_NAME = {}


def param_source_for_operation(op_type, track, params):
    try:
        # we know that this can only be a Rally core parameter source
        return __PARAM_SOURCES_BY_OP[op_type](track, params)
    except KeyError:
        return ParamSource(track, params)


def param_source_for_name(name, track, params):
    param_source = __PARAM_SOURCES_BY_NAME[name]

    # we'd rather use callable() but this will erroneously also classify a class as callable...
    if isinstance(param_source, types.FunctionType):
        return DelegatingParamSource(track, params, param_source)
    else:
        return param_source(track, params)


def register_param_source_for_operation(op_type, param_source_class):
    __PARAM_SOURCES_BY_OP[op_type.name] = param_source_class


def register_param_source_for_name(name, param_source_class):
    __PARAM_SOURCES_BY_NAME[name] = param_source_class


# only intended for tests
def _unregister_param_source_for_name(name):
    # We intentionally do not specify a default value if the key does not exist. If we try to remove a key that we didn't insert then
    # something is fishy with the test and we'd rather know early.
    __PARAM_SOURCES_BY_NAME.pop(name)


# Default
class ParamSource:
    """
    A `ParamSource` captures the parameters for a given operation. Rally will create one global ParamSource for each operation and will then
     invoke `#partition()` to get a `ParamSource` instance for each client. During the benchmark, `#params()` will be called repeatedly
     before Rally invokes the corresponding runner (that will actually execute the operation against Elasticsearch).
    """

    def __init__(self, track, params, **kwargs):
        """
        Creates a new ParamSource instance.

        :param track:  The current track definition
        :param params: A hash of all parameters that have been extracted for this operation.
        """
        self.track = track
        self._params = params
        self.kwargs = kwargs

    def partition(self, partition_index, total_partitions):
        """
        This method will be invoked by Rally at the beginning of the lifecycle. It splits a parameter source per client. If the
        corresponding operation is idempotent, return `self` (e.g. for queries). If the corresponding operation has side-effects and it
        matters which client executes which part (e.g. an index operation from a source file), return the relevant part.

        Do NOT assume that you can share state between ParamSource objects in different partitions (technical explanation: each client
        will be a dedicated process, so each object of a `ParamSource` lives in its own process and hence cannot share state with other
        instances).

        :param partition_index: The current partition for which a parameter source is needed. It is in the range [0, `total_partitions`).
        :param total_partitions: The total number of partitions (i.e. clients).
        :return: A parameter source for the current partition.
        """
        return self

    def size(self):
        """
        Rally has two modes in which it can run:

        * It will either run an operation for a pre-determined number of times or
        * It can run until the parameter source is exhausted.

        In the former case, you should determine the number of times that `#params()` will be invoked. With that number, Rally can show
        the progress made so far to the user. In the latter case, return ``None``.

        :return:  The "size" of this parameter source or ``None`` if should run eternally.
        """
        return None

    def params(self):
        """
        :return: A hash containing the parameters that will be provided to the corresponding operation runner (key: parameter name,
        value: parameter value).
        """
        return self._params


class DelegatingParamSource(ParamSource):
    def __init__(self, track, params, delegate, **kwargs):
        super().__init__(track, params, **kwargs)
        self.delegate = delegate

    def params(self):
        return self.delegate(self.track, self._params, **self.kwargs)


class SleepParamSource(ParamSource):
    def __init__(self, track, params, **kwargs):
        super().__init__(track, params, **kwargs)
        try:
            duration = params["duration"]
        except KeyError:
            raise exceptions.InvalidSyntax("parameter 'duration' is mandatory for sleep operation")

        if not isinstance(duration, numbers.Number):
            raise exceptions.InvalidSyntax("parameter 'duration' for sleep operation must be a number")
        if duration < 0:
            raise exceptions.InvalidSyntax("parameter 'duration' must be non-negative but was {}".format(duration))

    def params(self):
        return dict(self._params)


class CreateIndexParamSource(ParamSource):
    def __init__(self, track, params, **kwargs):
        super().__init__(track, params, **kwargs)
        self.request_params = params.get("request-params", {})
        self.index_definitions = []
        if track.indices:
            filter_idx = params.get("index")
            if isinstance(filter_idx, str):
                filter_idx = [filter_idx]
            settings = params.get("settings")
            for idx in track.indices:
                if not filter_idx or idx.name in filter_idx:
                    body = idx.body
                    if body and settings:
                        if "settings" in body:
                            # merge (and potentially override)
                            body["settings"].update(settings)
                        else:
                            body["settings"] = settings
                    elif not body and settings:
                        body = {
                            "settings": settings
                        }

                    self.index_definitions.append((idx.name, body))
        else:
            try:
                # only 'index' is mandatory, the body is optional (may be ok to create an index without a body)
                idx = params["index"]
                body = params.get("body")
                if isinstance(idx, str):
                    idx = [idx]
                for i in idx:
                    self.index_definitions.append((i, body))
            except KeyError:
                raise exceptions.InvalidSyntax("Please set the property 'index' for the create-index operation")

    def params(self):
        p = {}
        # ensure we pass all parameters...
        p.update(self._params)
        p.update({
            "indices": self.index_definitions,
            "request-params": self.request_params
        })
        return p


class DeleteIndexParamSource(ParamSource):
    def __init__(self, track, params, **kwargs):
        super().__init__(track, params, **kwargs)
        self.request_params = params.get("request-params", {})
        self.only_if_exists = params.get("only-if-exists", True)

        self.index_definitions = []
        target_index = params.get("index")
        if target_index:
            if isinstance(target_index, str):
                target_index = [target_index]
            for idx in target_index:
                self.index_definitions.append(idx)
        elif track.indices:
            for idx in track.indices:
                self.index_definitions.append(idx.name)
        else:
            raise exceptions.InvalidSyntax("delete-index operation targets no index")

    def params(self):
        p = {}
        # ensure we pass all parameters...
        p.update(self._params)
        p.update({
            "indices": self.index_definitions,
            "request-params": self.request_params,
            "only-if-exists": self.only_if_exists
        })
        return p


class CreateIndexTemplateParamSource(ParamSource):
    def __init__(self, track, params, **kwargs):
        super().__init__(track, params, **kwargs)
        self.request_params = params.get("request-params", {})
        self.template_definitions = []
        if track.templates:
            filter_template = params.get("template")
            settings = params.get("settings")
            for template in track.templates:
                if not filter_template or template.name == filter_template:
                    body = template.content
                    if body and settings:
                        if "settings" in body:
                            # merge (and potentially override)
                            body["settings"].update(settings)
                        else:
                            body["settings"] = settings

                    self.template_definitions.append((template.name, body))
        else:
            try:
                self.template_definitions.append((params["template"], params["body"]))
            except KeyError:
                raise exceptions.InvalidSyntax("Please set the properties 'template' and 'body' for the create-index-template operation")

    def params(self):
        p = {}
        # ensure we pass all parameters...
        p.update(self._params)
        p.update({
            "templates": self.template_definitions,
            "request-params": self.request_params
        })
        return p


class DeleteIndexTemplateParamSource(ParamSource):
    def __init__(self, track, params, **kwargs):
        super().__init__(track, params, **kwargs)
        self.only_if_exists = params.get("only-if-exists", True)
        self.request_params = params.get("request-params", {})
        self.template_definitions = []
        if track.templates:
            filter_template = params.get("template")
            for template in track.templates:
                if not filter_template or template.name == filter_template:
                    self.template_definitions.append((template.name, template.delete_matching_indices, template.pattern))
        else:
            try:
                template = params["template"]
            except KeyError:
                raise exceptions.InvalidSyntax("Please set the property 'template' for the delete-index-template operation")

            delete_matching = params.get("delete-matching-indices", False)
            try:
                index_pattern = params["index-pattern"] if delete_matching else None
            except KeyError:
                raise exceptions.InvalidSyntax("The property 'index-pattern' is required for delete-index-template if "
                                               "'delete-matching-indices' is true.")
            self.template_definitions.append((template, delete_matching, index_pattern))

    def params(self):
        p = {}
        # ensure we pass all parameters...
        p.update(self._params)
        p.update({
            "templates": self.template_definitions,
            "only-if-exists": self.only_if_exists,
            "request-params": self.request_params
        })
        return p


# TODO #365: This contains "body-params" as an undocumented feature. Get more experience and expand it to make it actually usable.
#
# Usage example:
#
#
# {
#     "name": "term",
#     "operation": {
#         "operation-type": "search",
#         "cache": false,
#         "body-params": {
#             "query.term.useragent": [
#                 "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
#                 "Mozilla/5.0 (IE 11.0; Windows NT 6.3; Trident/7.0; .NET4.0E; .NET4.0C; rv:11.0) like Gecko",
#                 "Mozilla/5.0 (IE 11.0; Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko"
#             ]
#         },
#         "index": "logs-*",
#         "body": {
#             "query": {
#                 "term": {
#                     "useragent": "Opera/5.11 (Windows 98; U) [en]"
#                 }
#             }
#         }
#     },
#     "clients": 1,
#     "target-throughput": 100,
#     "warmup-iterations": 100,
#     "iterations": 100
# }
#
#
class SearchParamSource(ParamSource):
    def __init__(self, track, params, **kwargs):
        super().__init__(track, params, **kwargs)
        if len(track.indices) == 1:
            default_index = track.indices[0].name
        else:
            default_index = None

        index_name = params.get("index", default_index)
        type_name = params.get("type")
        request_cache = params.get("cache", False)
        query_body = params.get("body", None)
        query_body_params = params.get("body-params", None)
        pages = params.get("pages", None)
        results_per_page = params.get("results-per-page", None)
        request_params = params.get("request-params", {})

        self.query_params = {
            "index": index_name,
            "type": type_name,
            "cache": request_cache,
            "request-params": request_params,
            "body": query_body
        }

        if not index_name:
            raise exceptions.InvalidSyntax("'index' is mandatory")

        if pages:
            self.query_params["pages"] = pages
        if results_per_page:
            self.query_params["results-per-page"] = results_per_page

        self.query_body_params = []
        if query_body_params:
            for param, data in query_body_params.items():
                # TODO #365: Strictly check for allowed syntax. Be lenient in the pre-release and only interpret what's safely possible.
                # build path based on param
                # if not isinstance(data, list):
                #    raise exceptions.RallyError("%s in body-params defines %s but only lists are allowed. This may be a new syntax "
                #                                "that is not recognized by this version. Please upgrade Rally." % (param, data))
                if isinstance(data, list):
                    query_body_path = param.split(".")
                    b = self.query_params["body"]
                    # check early to ensure this path is actually contained in the body
                    try:
                        self.get_from_dict(b, query_body_path)
                    except KeyError:
                        raise exceptions.RallyError("The path %s could not be found within the query body %s." % (param, b))

                    self.query_body_params.append((query_body_path, data))

    def get_from_dict(self, d, path):
        v = d
        for k in path:
            v = v[k]
        return v

    def set_in_dict(self, d, path, val):
        v = d
        # navigate to the next to last path
        for k in path[:-1]:
            v = v[k]
        # the value is now the inner-most dictionary and the last path element is its key
        v[path[-1]] = val

    def params(self, choice=random.choice):
        if self.query_body_params:
            # needs to replace params first
            for path, data in self.query_body_params:
                self.set_in_dict(self.query_params["body"], path, choice(data))
        return self.query_params


class IndexIdConflict(Enum):
    """
    Determines which id conflicts to simulate during indexing.

    * NoConflicts: Produce no id conflicts
    * SequentialConflicts: A document id is replaced with a document id with a sequentially increasing id
    * RandomConflicts: A document id is replaced with a document id with a random other id

    Note that this assumes that each document in the benchmark corpus has an id between [1, size_of(corpus)]
    """
    NoConflicts = 0,
    SequentialConflicts = 1,
    RandomConflicts = 2


class BulkIndexParamSource(ParamSource):
    def __init__(self, track, params, **kwargs):
        super().__init__(track, params, **kwargs)
        id_conflicts = params.get("conflicts", None)
        if not id_conflicts:
            self.id_conflicts = IndexIdConflict.NoConflicts
        elif id_conflicts == "sequential":
            self.id_conflicts = IndexIdConflict.SequentialConflicts
        elif id_conflicts == "random":
            self.id_conflicts = IndexIdConflict.RandomConflicts
        else:
            raise exceptions.InvalidSyntax("Unknown 'conflicts' setting [%s]" % id_conflicts)

        if self.id_conflicts != IndexIdConflict.NoConflicts:
            self.conflict_probability = self.float_param(params, name="conflict-probability", default_value=25, min_value=0, max_value=100,
                                                         min_operator=operator.lt)
            self.on_conflict = params.get("on-conflict", "index")
            if self.on_conflict not in ["index", "update"]:
                raise exceptions.InvalidSyntax("Unknown 'on-conflict' setting [{}]".format(self.on_conflict))
            self.recency = self.float_param(params, name="recency", default_value=0, min_value=0, max_value=1, min_operator=operator.lt)

        else:
            self.conflict_probability = None
            self.on_conflict = None
            self.recency = None

        self.corpora = self.used_corpora(track, params)

        for corpus in self.corpora:
            for document_set in corpus.documents:
                if document_set.includes_action_and_meta_data and self.id_conflicts != IndexIdConflict.NoConflicts:
                    file_name = document_set.document_archive if document_set.has_compressed_corpus() else document_set.document_file

                    raise exceptions.InvalidSyntax("Cannot generate id conflicts [%s] as [%s] in document corpus [%s] already contains an "
                                                   "action and meta-data line." % (id_conflicts, file_name, corpus))

        self.pipeline = params.get("pipeline", None)
        try:
            self.bulk_size = int(params["bulk-size"])
            if self.bulk_size <= 0:
                raise exceptions.InvalidSyntax("'bulk-size' must be positive but was %d" % self.bulk_size)
        except KeyError:
            raise exceptions.InvalidSyntax("Mandatory parameter 'bulk-size' is missing")
        except ValueError:
            raise exceptions.InvalidSyntax("'bulk-size' must be numeric")

        try:
            self.batch_size = int(params.get("batch-size", self.bulk_size))
            if self.batch_size <= 0:
                raise exceptions.InvalidSyntax("'batch-size' must be positive but was %d" % self.batch_size)
            if self.batch_size < self.bulk_size:
                raise exceptions.InvalidSyntax("'batch-size' must be greater than or equal to 'bulk-size'")
            if self.batch_size % self.bulk_size != 0:
                raise exceptions.InvalidSyntax("'batch-size' must be a multiple of 'bulk-size'")
        except ValueError:
            raise exceptions.InvalidSyntax("'batch-size' must be numeric")

        self.ingest_percentage = self.float_param(params, name="ingest-percentage", default_value=100, min_value=0, max_value=100)

    def float_param(self, params, name, default_value, min_value, max_value, min_operator=operator.le):
        try:
            value = float(params.get(name, default_value))
            if min_operator(value, min_value) or value > max_value:
                interval_min = "(" if min_operator is operator.le else "["
                raise exceptions.InvalidSyntax(
                    "'{}' must be in the range {}{:.1f}, {:.1f}] but was {:.1f}".format(name, interval_min, min_value, max_value, value))
            return value
        except ValueError:
            raise exceptions.InvalidSyntax("'{}' must be numeric".format(name))

    def used_corpora(self, t, params):
        corpora = []
        track_corpora_names = [corpus.name for corpus in t.corpora]
        corpora_names = params.get("corpora", track_corpora_names)
        if isinstance(corpora_names, str):
            corpora_names = [corpora_names]

        for corpus in t.corpora:
            if corpus.name in corpora_names:
                filtered_corpus = corpus.filter(source_format=track.Documents.SOURCE_FORMAT_BULK, target_indices=params.get("indices"))
                if filtered_corpus.number_of_documents(source_format=track.Documents.SOURCE_FORMAT_BULK) > 0:
                    corpora.append(filtered_corpus)

        # the track has corpora but none of them match
        if t.corpora and not corpora:
            raise exceptions.RallyAssertionError("The provided corpus %s does not match any of the corpora %s." %
                                                 (corpora_names, track_corpora_names))

        return corpora

    def partition(self, partition_index, total_partitions):
        return PartitionBulkIndexParamSource(self.corpora, partition_index, total_partitions, self.batch_size, self.bulk_size,
                                             self.ingest_percentage, self.id_conflicts, self.conflict_probability, self.on_conflict,
                                             self.recency, self.pipeline, self._params)

    def params(self):
        raise exceptions.RallyError("Do not use a BulkIndexParamSource without partitioning")

    def size(self):
        raise exceptions.RallyError("Do not use a BulkIndexParamSource without partitioning")


class PartitionBulkIndexParamSource:
    def __init__(self, corpora, partition_index, total_partitions, batch_size, bulk_size, ingest_percentage,
                 id_conflicts, conflict_probability, on_conflict, recency, pipeline=None, original_params=None):
        """

        :param corpora: Specification of affected document corpora.
        :param partition_index: The current partition index.  Must be in the range [0, `total_partitions`).
        :param total_partitions: The total number of partitions (i.e. clients) for bulk index operations.
        :param batch_size: The number of documents to read in one go.
        :param bulk_size: The size of bulk index operations (number of documents per bulk).
        :param ingest_percentage: A number between (0.0, 100.0] that defines how much of the whole corpus should be ingested.
        :param id_conflicts: The type of id conflicts.
        :param conflict_probability: A number between (0.0, 100.0] that defines the probability that a document is replaced by another one.
        :param on_conflict: A string indicating which action should be taken on id conflicts (either "index" or "update").
        :param recency: A number between [0.0, 1.0] indicating whether to bias generation of conflicting ids towards more recent ones.
                        May be None.
        :param pipeline: The name of the ingest pipeline to run.
        :param original_params: The original dict passed to the parent parameter source.
        """
        self.corpora = corpora
        self.partition_index = partition_index
        self.total_partitions = total_partitions
        self.batch_size = batch_size
        self.bulk_size = bulk_size
        self.ingest_percentage = ingest_percentage
        self.id_conflicts = id_conflicts
        self.pipeline = pipeline
        self.internal_params = bulk_data_based(total_partitions, partition_index, corpora, batch_size,
                                               bulk_size, id_conflicts, conflict_probability, on_conflict, recency,
                                               pipeline, original_params)

    def partition(self, partition_index, total_partitions):
        raise exceptions.RallyError("Cannot partition a PartitionBulkIndexParamSource further")

    def params(self):
        return next(self.internal_params)

    def size(self):
        all_bulks = number_of_bulks(self.corpora, self.partition_index, self.total_partitions, self.bulk_size)
        return math.ceil((all_bulks * self.ingest_percentage) / 100)


def number_of_bulks(corpora, partition_index, total_partitions, bulk_size):
    """
    :return: The number of bulk operations that the given client will issue.
    """
    bulks = 0
    for corpus in corpora:
        for docs in corpus.documents:
            _, num_docs, _ = bounds(docs.number_of_documents, partition_index, total_partitions,
                                    docs.includes_action_and_meta_data)
            complete_bulks, rest = (num_docs // bulk_size, num_docs % bulk_size)
            bulks += complete_bulks
            if rest > 0:
                bulks += 1
    return bulks


def build_conflicting_ids(conflicts, docs_to_index, offset, shuffle=random.shuffle):
    if conflicts is None or conflicts == IndexIdConflict.NoConflicts:
        return None
    all_ids = [0] * docs_to_index
    for i in range(docs_to_index):
        # always consider the offset as each client will index its own range and we don't want uncontrolled conflicts across clients
        all_ids[i] = "%10d" % (offset + i)
    if conflicts == IndexIdConflict.RandomConflicts:
        shuffle(all_ids)
    return all_ids


def chain(*iterables):
    """
    Chains the given iterables similar to `itertools.chain` except that it also respects the context manager contract.

    :param iterables: A number of iterable that should be chained.
    :return: An iterable that will delegate to all provided iterables in turn.
    """
    for it in iterables:
        # execute within a context
        with it:
            for element in it:
                yield element


def create_default_reader(docs, offset, num_lines, num_docs, batch_size, bulk_size, id_conflicts, conflict_probability,
                          on_conflict, recency):
    source = Slice(io.FileSource, offset, num_lines)

    if docs.includes_action_and_meta_data:
        am_handler = SourceActionMetaData(source)
    else:
        am_handler = GenerateActionMetaData(docs.target_index, docs.target_type,
                                            build_conflicting_ids(id_conflicts, num_docs, offset), conflict_probability,
                                            on_conflict, recency)

    return IndexDataReader(docs.document_file, batch_size, bulk_size, source, am_handler, docs.target_index, docs.target_type)


def create_readers(num_clients, client_index, corpora, batch_size, bulk_size, id_conflicts, conflict_probability, on_conflict, recency,
                   create_reader):
    logger = logging.getLogger(__name__)
    readers = []
    for corpus in corpora:
        for docs in corpus.documents:
            offset, num_docs, num_lines = bounds(docs.number_of_documents, client_index, num_clients,
                                                 docs.includes_action_and_meta_data)
            if num_docs > 0:
                logger.info("Task-relative client at index [%d] will bulk index [%d] docs starting from line offset [%d] for [%s/%s] "
                            "from corpus [%s]." % (client_index, num_docs, offset, docs.target_index, docs.target_type, corpus.name))
                readers.append(create_reader(docs, offset, num_lines, num_docs, batch_size, bulk_size, id_conflicts, conflict_probability,
                                             on_conflict, recency))
            else:
                logger.info("Task-relative client at index [%d] skips [%s] (no documents to read).", client_index, corpus.name)
    return readers


def bounds(total_docs, client_index, num_clients, includes_action_and_meta_data):
    """

    Calculates the start offset and number of documents for each client.

    :param total_docs: The total number of documents to index.
    :param client_index: The current client index.  Must be in the range [0, `num_clients').
    :param num_clients: The total number of clients that will run bulk index operations.
    :param includes_action_and_meta_data: Whether the source file already includes the action and meta-data line.
    :return: A tuple containing: the start offset (in lines) for the document corpus, the number documents that the client should index,
    and the number of lines that the client should read.
    """
    source_lines_per_doc = 2 if includes_action_and_meta_data else 1

    docs_per_client = total_docs / num_clients

    start_offset_docs = round(docs_per_client * client_index)
    end_offset_docs = round(docs_per_client * (client_index + 1))

    offset_lines = start_offset_docs * source_lines_per_doc
    docs = end_offset_docs - start_offset_docs
    lines = docs * source_lines_per_doc

    return offset_lines, docs, lines


def bulk_generator(readers, client_index, pipeline, original_params):
    bulk_id = 0
    for index, type, batch in readers:
        # each batch can contain of one or more bulks
        for docs_in_bulk, bulk in batch:
            bulk_id += 1
            bulk_params = {
                "index": index,
                "type": type,
                # For our implementation it's always present. Either the original source file already contains this line or the generator
                # has added it.
                "action-metadata-present": True,
                "body": bulk,
                # This is not always equal to the bulk_size we get as parameter. The last bulk may be less than the bulk size.
                "bulk-size": docs_in_bulk,
                # a globally unique id for this bulk
                "bulk-id": "%d-%d" % (client_index, bulk_id)
            }
            if pipeline:
                bulk_params["pipeline"] = pipeline

            params = original_params.copy()
            params.update(bulk_params)
            yield params


def bulk_data_based(num_clients, client_index, corpora, batch_size, bulk_size, id_conflicts, conflict_probability, on_conflict, recency,
                    pipeline, original_params, create_reader=create_default_reader):
    """
    Calculates the necessary schedule for bulk operations.

    :param num_clients: The total number of clients that will run the bulk operation.
    :param client_index: The current client for which we calculated the schedule. Must be in the range [0, `num_clients').
    :param corpora: Specification of affected document corpora.
    :param batch_size: The number of documents to read in one go.
    :param bulk_size: The size of bulk index operations (number of documents per bulk).
    :param id_conflicts: The type of id conflicts to simulate.
    :param conflict_probability: A number between (0.0, 100.0] that defines the probability that a document is replaced by another one.
    :param on_conflict: A string indicating which action should be taken on id conflicts (either "index" or "update").
    :param recency: A number between [0.0, 1.0] indicating whether to bias generation of conflicting ids towards more recent ones.
                    May be None.
    :param pipeline: Name of the ingest pipeline to use. May be None.
    :param original_params: A dict of original parameters that were passed from the track. They will be merged into the returned parameters.
    :param create_reader: A function to create the index reader. By default a file based index reader will be created. This parameter is
                      intended for testing only.
    :return: A generator for the bulk operations of the given client.
    """
    readers = create_readers(num_clients, client_index, corpora, batch_size, bulk_size, id_conflicts, conflict_probability, on_conflict,
                             recency, create_reader)
    return bulk_generator(chain(*readers), client_index, pipeline, original_params)


class GenerateActionMetaData:
    RECENCY_SLOPE = 30

    def __init__(self, index_name, type_name, conflicting_ids=None, conflict_probability=None, on_conflict=None,
                 recency=None, rand=random.random, randint=random.randint, randexp=random.expovariate):
        if type_name:
            self.meta_data_index_with_id = '{"index": {"_index": "%s", "_type": "%s", "_id": "%s"}}' % \
                                           (index_name, type_name, "%s")
            self.meta_data_update_with_id = '{"update": {"_index": "%s", "_type": "%s", "_id": "%s"}}' % \
                                            (index_name, type_name, "%s")
            self.meta_data_index_no_id = '{"index": {"_index": "%s", "_type": "%s"}}' % (index_name, type_name)
        else:
            self.meta_data_index_with_id = '{"index": {"_index": "%s", "_id": "%s"}}' % (index_name, "%s")
            self.meta_data_update_with_id = '{"update": {"_index": "%s", "_id": "%s"}}' % (index_name, "%s")
            self.meta_data_index_no_id = '{"index": {"_index": "%s"}}' % index_name

        self.conflicting_ids = conflicting_ids
        self.on_conflict = on_conflict
        # random() produces numbers between 0 and 1 and the user denotes the probability in percentage between 0 and 100
        self.conflict_probability = conflict_probability / 100.0 if conflict_probability is not None else 0
        self.recency = recency if recency is not None else 0

        self.rand = rand
        self.randint = randint
        self.randexp = randexp
        self.id_up_to = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.conflicting_ids is not None:
            if self.conflict_probability and self.id_up_to > 0 and self.rand() <= self.conflict_probability:
                # a recency of zero means that we don't care about recency and just take a random number
                # within the whole interval.
                if self.recency == 0:
                    idx = self.randint(0, self.id_up_to - 1)
                else:
                    # A recency > 0 biases id selection towards more recent ids. The recency parameter decides
                    # by how much we bias. See docs for the resulting curve.
                    #
                    # idx_range is in the interval [0, 1].
                    idx_range = min(self.randexp(GenerateActionMetaData.RECENCY_SLOPE * self.recency), 1)
                    # the resulting index is in the range [0, self.id_up_to). Note that a smaller idx_range
                    # biases towards more recently used ids (higher indexes).
                    idx = round((self.id_up_to - 1) * (1 - idx_range))

                doc_id = self.conflicting_ids[idx]
                action = self.on_conflict
            else:
                if self.id_up_to >= len(self.conflicting_ids):
                    raise StopIteration()
                doc_id = self.conflicting_ids[self.id_up_to]
                self.id_up_to += 1
                action = "index"

            if action == "index":
                return "index", self.meta_data_index_with_id % doc_id
            elif action == "update":
                return "update", self.meta_data_update_with_id % doc_id
            else:
                raise exceptions.RallyAssertionError("Unknown action [{}]".format(action))
        else:
            return "index", self.meta_data_index_no_id


class SourceActionMetaData:
    def __init__(self, source):
        self.source = source

    def __iter__(self):
        return self

    def __next__(self):
        return "source", next(self.source)


class Slice:
    def __init__(self, source_class, offset, number_of_lines):
        self.source_class = source_class
        self.source = None
        self.offset = offset
        self.number_of_lines = number_of_lines
        self.current_line = 0

    def open(self, file_name, mode):
        logger = logging.getLogger(__name__)
        self.source = self.source_class(file_name, mode).open()
        # skip offset number of lines
        logger.info("Skipping %d lines in [%s].", self.offset, file_name)
        start = time.perf_counter()
        io.skip_lines(file_name, self.source, self.offset)
        end = time.perf_counter()
        logger.info("Skipping %d lines took %f s.", self.offset, end - start)
        return self

    def close(self):
        self.source.close()
        self.source = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_line >= self.number_of_lines:
            raise StopIteration()
        else:
            self.current_line += 1
            line = self.source.readline()
            if len(line) == 0:
                raise StopIteration()
            return line.strip()

    def __str__(self):
        return "%s[%d;%d]" % (self.source, self.offset, self.offset + self.number_of_lines)


class IndexDataReader:
    """
    Reads a file in bulks into an array and also adds a meta-data line before each document if necessary.

    This implementation also supports batching. This means that you can specify batch_size = N * bulk_size, where N is any natural
    number >= 1. This makes file reading more efficient for small bulk sizes.
    """

    def __init__(self, data_file, batch_size, bulk_size, file_source, action_metadata, index_name, type_name):
        self.data_file = data_file
        self.batch_size = batch_size
        self.bulk_size = bulk_size
        self.file_source = file_source
        self.action_metadata = action_metadata
        self.index_name = index_name
        self.type_name = type_name

    def __enter__(self):
        self.file_source.open(self.data_file, 'rt')
        return self

    def __iter__(self):
        return self

    def __next__(self):
        """
        Returns lines for N bulk requests (where N is bulk_size / batch_size)
        """
        batch = []
        try:
            docs_in_batch = 0
            while docs_in_batch < self.batch_size:
                docs_in_bulk, bulk = self.read_bulk()
                if docs_in_bulk == 0:
                    break
                docs_in_batch += docs_in_bulk
                batch.append((docs_in_bulk, bulk))
            if docs_in_batch == 0:
                raise StopIteration()
            return self.index_name, self.type_name, batch
        except IOError:
            logging.getLogger(__name__).exception("Could not read [%s]", self.data_file)

    def read_bulk(self):
        docs_in_bulk = 0
        current_bulk = []
        for action_metadata_item, document in zip(self.action_metadata, self.file_source):
            if action_metadata_item:
                action_type, action_metadata_line = action_metadata_item
                current_bulk.append(action_metadata_line)
                if action_type == "update":
                    current_bulk.append("{\"doc\":%s}" % document)
                else:
                    current_bulk.append(document)
            else:
                current_bulk.append(document)
            docs_in_bulk += 1
            if docs_in_bulk == self.bulk_size:
                break
        return docs_in_bulk, current_bulk

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_source.close()
        return False


register_param_source_for_operation(track.OperationType.Bulk, BulkIndexParamSource)
register_param_source_for_operation(track.OperationType.Search, SearchParamSource)
register_param_source_for_operation(track.OperationType.CreateIndex, CreateIndexParamSource)
register_param_source_for_operation(track.OperationType.DeleteIndex, DeleteIndexParamSource)
register_param_source_for_operation(track.OperationType.CreateIndexTemplate, CreateIndexTemplateParamSource)
register_param_source_for_operation(track.OperationType.DeleteIndexTemplate, DeleteIndexTemplateParamSource)
register_param_source_for_operation(track.OperationType.Sleep, SleepParamSource)

# Also register by name, so users can use it too
register_param_source_for_name("file-reader", BulkIndexParamSource)
