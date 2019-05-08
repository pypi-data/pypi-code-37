# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import numpy as np

from sklearn import pipeline
from sklearn.base import ClassifierMixin, ClusterMixin
from sklearn.neighbors import NearestNeighbors
from sklearn.svm import LinearSVC, NuSVC, SVC
try:
    from sklearn.compose import ColumnTransformer
except ModuleNotFoundError:
    # ColumnTransformer was introduced in 0.20.
    ColumnTransformer = None

from ._supported_operators import _get_sklearn_operator_name, cluster_list
from ._supported_operators import sklearn_classifier_list
from .common._container import SklearnModelContainerNode
from .common._topology import Topology
from .common.data_types import DictionaryType, FloatTensorType
from .common.data_types import Int64TensorType, SequenceType
from .common.data_types import Int64Type, StringType, TensorType
from .common.utils import get_column_indices


def _fetch_input_slice(scope, inputs, column_indices):
    if not isinstance(inputs, list):
        raise TypeError("inputs must be a list of 1 input.")
    if len(inputs) == 0:
        raise RuntimeError("Operator ArrayFeatureExtractor requires at "
                           "least one inputs.")
    if len(inputs) != 1:
        raise RuntimeError("Operator ArrayFeatureExtractor does not support "
                           "multiple input tensors.")
    if (isinstance(inputs[0].type, TensorType) and
            inputs[0].type.shape[1] == len(column_indices)):
        # No need to extract.
        return inputs
    array_feature_extractor_operator = scope.declare_local_operator(
                                            'SklearnArrayFeatureExtractor')
    array_feature_extractor_operator.inputs = inputs
    array_feature_extractor_operator.column_indices = column_indices
    output_variable_name = scope.declare_local_variable(
                            'extracted_feature_columns', inputs[0].type)
    array_feature_extractor_operator.outputs.append(output_variable_name)
    return array_feature_extractor_operator.outputs


def _parse_sklearn_simple_model(scope, model, inputs, custom_parsers=None):
    """
    This function handles all non-pipeline models.

    :param scope: Scope object
    :param model: A scikit-learn object (e.g., *OneHotEncoder*
        or *LogisticRegression*)
    :param inputs: A list of variables
    :return: A list of output variables which will be passed to next
        stage
    """
    # alias can be None
    alias = _get_sklearn_operator_name(type(model))
    this_operator = scope.declare_local_operator(alias, model)
    this_operator.inputs = inputs

    if (type(model) in sklearn_classifier_list
            or isinstance(model, ClassifierMixin)):
        # For classifiers, we may have two outputs, one for label and
        # the other one for probabilities of all classes. Notice that
        # their types here are not necessarily correct and they will
        # be fixed in shape inference phase
        label_variable = scope.declare_local_variable('label',
                                                      FloatTensorType())
        probability_tensor_variable = scope.declare_local_variable(
                                    'probabilities', FloatTensorType())
        this_operator.outputs.append(label_variable)
        this_operator.outputs.append(probability_tensor_variable)
    elif type(model) in cluster_list or isinstance(model, ClusterMixin):
        # For clustering, we may have two outputs, one for label and
        # the other one for scores of all classes. Notice that their
        # types here are not necessarily correct and they will be fixed
        # in shape inference phase
        label_variable = scope.declare_local_variable('label',
                                                      Int64TensorType())
        score_tensor_variable = scope.declare_local_variable('scores',
                                                             FloatTensorType())
        this_operator.outputs.append(label_variable)
        this_operator.outputs.append(score_tensor_variable)
    elif type(model) == NearestNeighbors:
        # For Nearest Neighbours, we have two outputs, one for nearest
        # neighbours' indices and the other one for distances
        index_variable = scope.declare_local_variable('index',
                                                      Int64TensorType())
        distance_variable = scope.declare_local_variable('distance',
                                                         FloatTensorType())
        this_operator.outputs.append(index_variable)
        this_operator.outputs.append(distance_variable)
    else:
        # We assume that all scikit-learn operator produce a single output.
        variable = scope.declare_local_variable('variable', FloatTensorType())
        this_operator.outputs.append(variable)

    return this_operator.outputs


def _parse_sklearn_pipeline(scope, model, inputs, custom_parsers=None):
    """
    The basic ideas of scikit-learn parsing:
        1. Sequentially go though all stages defined in the considered
           scikit-learn pipeline
        2. The output variables of one stage will be fed into its next
           stage as the inputs.

    :param scope: Scope object defined in _topology.py
    :param model: scikit-learn pipeline object
    :param inputs: A list of Variable objects
    :return: A list of output variables produced by the input pipeline
    """
    for step in model.steps:
        inputs = parse_sklearn(scope, step[1], inputs,
                               custom_parsers=custom_parsers)
    return inputs


def _parse_sklearn_feature_union(scope, model, inputs, custom_parsers=None):
    """
    :param scope: Scope object
    :param model: A scikit-learn FeatureUnion object
    :param inputs: A list of Variable objects
    :return: A list of output variables produced by feature union
    """
    # Output variable name of each transform. It's a list of string.
    transformed_result_names = []
    # Encode each transform as our IR object
    for name, transform in model.transformer_list:
        transformed_result_names.append(
            _parse_sklearn_simple_model(
                scope, transform, inputs,
                custom_parsers=custom_parsers)[0])
    # Create a Concat ONNX node
    concat_operator = scope.declare_local_operator('SklearnConcat')
    concat_operator.inputs = transformed_result_names

    # Declare output name of scikit-learn FeatureUnion
    union_name = scope.declare_local_variable('union', FloatTensorType())
    concat_operator.outputs.append(union_name)

    return concat_operator.outputs


def _parse_sklearn_column_transformer(scope, model, inputs,
                                      custom_parsers=None):
    """
    :param scope: Scope object
    :param model: A scikit-learn ColumnTransformer object
    :param inputs: A list of Variable objects
    :return: A list of output variables produced by column transformer
    """
    # Output variable name of each transform. It's a list of string.
    transformed_result_names = []
    # Encode each transform as our IR object
    for name, transform, column_indices in model.transformers:
        if isinstance(column_indices, slice):
            column_indices = list(range(
                column_indices.start
                if column_indices.start is not None else 0,
                column_indices.stop, column_indices.step
                if column_indices.step is not None else 1))
        elif isinstance(column_indices, (int, str)):
            column_indices = [column_indices]
        names = get_column_indices(column_indices, inputs, multiple=True)
        transform_inputs = []
        for onnx_var, onnx_is in names.items():
            tr_inputs = _fetch_input_slice(scope, [inputs[onnx_var]], onnx_is)
            transform_inputs.extend(tr_inputs)

        if len(transform_inputs) > 1:
            # Many ONNX operators expect one input vector,
            # the default behaviour is to merge columns.
            ty = transform_inputs[0].type.__class__([1, 'None'])

            conc_op = scope.declare_local_operator('SklearnConcat')
            conc_op.inputs = transform_inputs
            conc_names = scope.declare_local_variable('merged_columns', ty)
            conc_op.outputs.append(conc_names)
            transform_inputs = [conc_names]

        var_out = parse_sklearn(
            scope, model.named_transformers_[name],
            transform_inputs, custom_parsers=custom_parsers)[0]
        transformed_result_names.append(var_out)

    # Create a Concat ONNX node
    if len(transformed_result_names) > 1:
        ty = transformed_result_names[0].type.__class__([1, 'None'])
        concat_operator = scope.declare_local_operator('SklearnConcat')
        concat_operator.inputs = transformed_result_names

        # Declare output name of scikit-learn ColumnTransformer
        transformed_column_name = scope.declare_local_variable(
                                            'transformed_column', ty)
        concat_operator.outputs.append(transformed_column_name)

        return concat_operator.outputs
    else:
        return transformed_result_names


def _parse_sklearn_classifier(scope, model, inputs, custom_parsers=None):
    probability_tensor = _parse_sklearn_simple_model(
            scope, model, inputs, custom_parsers=custom_parsers)
    this_operator = scope.declare_local_operator('SklearnZipMap')
    this_operator.inputs = probability_tensor
    classes = model.classes_
    label_type = Int64Type()

    if np.issubdtype(model.classes_.dtype, np.floating):
        classes = np.array(list(map(lambda x: int(x), classes)))
        this_operator.classlabels_int64s = classes
    elif np.issubdtype(model.classes_.dtype, np.signedinteger):
        this_operator.classlabels_int64s = classes
    else:
        classes = np.array([s.encode('utf-8') for s in classes])
        this_operator.classlabels_strings = classes
        label_type = StringType()

    output_label = scope.declare_local_variable('output_label', label_type)
    output_probability = scope.declare_local_variable(
        'output_probability',
        SequenceType(DictionaryType(label_type, FloatTensorType())))
    this_operator.outputs.append(output_label)
    this_operator.outputs.append(output_probability)
    return this_operator.outputs


def parse_sklearn(scope, model, inputs, custom_parsers=None):
    """
    This is a delegate function. It does nothing but invokes the
    correct parsing function according to the input model's type.

    :param scope: Scope object
    :param model: A scikit-learn object (e.g., OneHotEncoder
        and LogisticRegression)
    :param inputs: A list of variables
    :param custom_parsers: parsers determines which outputs is expected
        for which particular task, default parsers are defined for
        classifiers, regressors, pipeline but they can be rewritten,
        *custom_parsers* is a dictionary ``{ type: fct_parser(scope,
        model, inputs, custom_parsers=None) }``
    :return: The output variables produced by the input model
    """
    tmodel = type(model)
    if custom_parsers is not None and tmodel in custom_parsers:
        outputs = custom_parsers[tmodel](scope, model, inputs,
                                         custom_parsers=custom_parsers)
    elif tmodel in sklearn_parsers_map:
        outputs = sklearn_parsers_map[tmodel](scope, model, inputs,
                                              custom_parsers=custom_parsers)
    else:
        outputs = _parse_sklearn_simple_model(scope, model, inputs,
                                              custom_parsers=custom_parsers)
    return outputs


def parse_sklearn_model(model, initial_types=None, target_opset=None,
                        custom_conversion_functions=None,
                        custom_shape_calculators=None,
                        custom_parsers=None):
    """
    Puts *scikit-learn* object into an abstract container so that
    our framework can work seamlessly on models created
    with different machine learning tools.

    :param model: A scikit-learn model
    :param initial_types: a python list. Each element is a tuple of a
        variable name and a type defined in data_types.py
    :param target_opset: number, for example, 7 for ONNX 1.2,
        and 8 for ONNX 1.3.
    :param custom_conversion_functions: a dictionary for specifying
        the user customized conversion function if not registered
    :param custom_shape_calculators: a dictionary for specifying the
        user customized shape calculator if not registered
    :param custom_parsers: parsers determines which outputs is expected
        for which particular task, default parsers are defined for
        classifiers, regressors, pipeline but they can be rewritten,
        *custom_parsers* is a dictionary
        ``{ type: fct_parser(scope, model, inputs, custom_parsers=None) }``
    :return: :class:`Topology <skl2onnx.common._topology.Topology>`
    """
    raw_model_container = SklearnModelContainerNode(model)

    # Declare a computational graph. It will become a representation of
    # the input scikit-learn model after parsing.
    topology = Topology(
            raw_model_container, initial_types=initial_types,
            target_opset=target_opset,
            custom_conversion_functions=custom_conversion_functions,
            custom_shape_calculators=custom_shape_calculators)

    # Declare an object to provide variables' and operators' naming mechanism.
    # In contrast to CoreML, one global scope
    # is enough for parsing scikit-learn models.
    scope = topology.declare_scope('__root__')

    # Declare input variables. They should be the inputs of the scikit-learn
    # model you want to convert into ONNX.
    inputs = []
    for var_name, initial_type in initial_types:
        inputs.append(scope.declare_local_variable(var_name, initial_type))

    # The object raw_model_container is a part of the topology
    # we're going to return. We use it to store the inputs of
    # the scikit-learn's computational graph.
    for variable in inputs:
        raw_model_container.add_input(variable)

    # Parse the input scikit-learn model as a Topology object.
    outputs = parse_sklearn(scope, model, inputs,
                            custom_parsers=custom_parsers)

    # The object raw_model_container is a part of the topology we're
    # going to return. We use it to store the outputs of the
    # scikit-learn's computational graph.
    for variable in outputs:
        raw_model_container.add_output(variable)

    return topology


def build_sklearn_parsers_map():
    map_parser = {
        pipeline.Pipeline: _parse_sklearn_pipeline,
        pipeline.FeatureUnion: _parse_sklearn_feature_union,
    }
    if ColumnTransformer is not None:
        map_parser[ColumnTransformer] = _parse_sklearn_column_transformer

    for tmodel in sklearn_classifier_list:
        if tmodel not in [LinearSVC, SVC, NuSVC]:
            map_parser[tmodel] = _parse_sklearn_classifier
    return map_parser


def update_registered_parser(model, parser_fct):
    """
    Registers or updates a parser for a new model.
    A parser returns the expected output of a model.

    :param model: model class
    :param parser_fct: parser, signature is the same as
        :func:`parse_sklearn <skl2onnx._parse.parse_sklearn>`
    """
    sklearn_parsers_map[model] = parser_fct


# registered parsers
sklearn_parsers_map = build_sklearn_parsers_map()
