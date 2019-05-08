# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import numpy as np

from ..proto import onnx_proto
from ..common._apply_operation import (
    apply_abs, apply_add, apply_cast, apply_concat, apply_div, apply_exp,
    apply_mul, apply_reshape, apply_sub)
from ..common._topology import FloatTensorType
from ..common._registration import register_converter
from .._supported_operators import sklearn_operator_name_map


def _handle_zeros(scope, container, concatenated_prob_name,
                  reduced_prob_name, n_classes):
    """
    This function replaces 0s in concatenated_prob_name with 1s and
    0s in reduced_prob_name with n_classes.
    """
    cast_prob_name = scope.get_unique_variable_name('cast_prob')
    bool_not_cast_prob_name = scope.get_unique_variable_name(
        'bool_not_cast_prob')
    mask_name = scope.get_unique_variable_name('mask')
    masked_concatenated_prob_name = scope.get_unique_variable_name(
        'masked_concatenated_prob')
    n_classes_name = scope.get_unique_variable_name('n_classes')
    reduced_prob_mask_name = scope.get_unique_variable_name(
        'reduced_prob_mask')
    masked_reduced_prob_name = scope.get_unique_variable_name(
        'masked_reduced_prob')

    container.add_initializer(n_classes_name, onnx_proto.TensorProto.FLOAT,
                              [], [n_classes])

    apply_cast(scope, reduced_prob_name, cast_prob_name, container,
               to=onnx_proto.TensorProto.BOOL)
    container.add_node('Not', cast_prob_name,
                       bool_not_cast_prob_name,
                       name=scope.get_unique_operator_name('Not'))
    apply_cast(scope, bool_not_cast_prob_name, mask_name, container,
               to=onnx_proto.TensorProto.FLOAT)
    apply_add(scope, [concatenated_prob_name, mask_name],
              masked_concatenated_prob_name, container, broadcast=1)
    apply_mul(scope, [mask_name, n_classes_name], reduced_prob_mask_name,
              container, broadcast=1)
    apply_add(scope, [reduced_prob_name, reduced_prob_mask_name],
              masked_reduced_prob_name, container, broadcast=0)
    return masked_concatenated_prob_name, masked_reduced_prob_name


def _transform_sigmoid(scope, container, model, df_col_name, k):
    """
    Sigmoid Calibration method
    """
    a_name = scope.get_unique_variable_name('a')
    b_name = scope.get_unique_variable_name('b')
    a_df_prod_name = scope.get_unique_variable_name('a_df_prod')
    exp_parameter_name = scope.get_unique_variable_name(
        'exp_parameter')
    exp_result_name = scope.get_unique_variable_name('exp_result')
    unity_name = scope.get_unique_variable_name('unity')
    denominator_name = scope.get_unique_variable_name('denominator')
    sigmoid_predict_result_name = scope.get_unique_variable_name(
        'sigmoid_predict_result')

    container.add_initializer(a_name, onnx_proto.TensorProto.FLOAT,
                              [], [model.calibrators_[k].a_])
    container.add_initializer(b_name, onnx_proto.TensorProto.FLOAT,
                              [], [model.calibrators_[k].b_])
    container.add_initializer(unity_name, onnx_proto.TensorProto.FLOAT,
                              [], [1])

    apply_mul(scope, [a_name, df_col_name], a_df_prod_name, container,
              broadcast=0)
    apply_add(scope, [a_df_prod_name, b_name], exp_parameter_name,
              container, broadcast=0)
    apply_exp(scope, exp_parameter_name, exp_result_name, container)
    apply_add(scope, [unity_name, exp_result_name], denominator_name,
              container, broadcast=0)
    apply_div(scope, [unity_name, denominator_name],
              sigmoid_predict_result_name, container, broadcast=0)
    return sigmoid_predict_result_name


def _transform_isotonic(scope, container, model, T, k):
    """
    Isotonic calibration method
    This function can only handle one instance at a time because
    ArrayFeatureExtractor can only extract based on the last axis,
    so we can't fetch different columns for different rows.
    """
    if model.calibrators_[k].out_of_bounds == 'clip':
        clipped_df_name = scope.get_unique_variable_name('clipped_df')

        container.add_node(
            'Clip', T, clipped_df_name,
            name=scope.get_unique_operator_name('Clip'),
            min=model.calibrators_[k].X_min_,
            max=model.calibrators_[k].X_max_)
        T = clipped_df_name

    reshaped_df_name = scope.get_unique_variable_name('reshaped_df')
    calibrator_x_name = scope.get_unique_variable_name('calibrator_x')
    calibrator_y_name = scope.get_unique_variable_name('calibrator_y')
    distance_name = scope.get_unique_variable_name('distance')
    absolute_distance_name = scope.get_unique_variable_name(
        'absolute_distance')
    nearest_x_index_name = scope.get_unique_variable_name(
        'nearest_x_index')
    nearest_y_name = scope.get_unique_variable_name('nearest_y')

    container.add_initializer(
        calibrator_x_name, onnx_proto.TensorProto.FLOAT,
        [len(model.calibrators_[k]._X_)], model.calibrators_[k]._X_)
    container.add_initializer(
        calibrator_y_name, onnx_proto.TensorProto.FLOAT,
        [len(model.calibrators_[k]._y_)], model.calibrators_[k]._y_)

    apply_reshape(scope, T, reshaped_df_name, container,
                  desired_shape=(-1, 1))
    apply_sub(scope, [reshaped_df_name, calibrator_x_name],
              distance_name, container, broadcast=1)
    apply_abs(scope, distance_name, absolute_distance_name, container)
    container.add_node('ArgMin', absolute_distance_name,
                       nearest_x_index_name, axis=1,
                       name=scope.get_unique_operator_name('ArgMin'))
    container.add_node(
        'ArrayFeatureExtractor',
        [calibrator_y_name, nearest_x_index_name],
        nearest_y_name, op_domain='ai.onnx.ml',
        name=scope.get_unique_operator_name('ArrayFeatureExtractor'))
    return nearest_y_name


def convert_calibrated_classifier_base_estimator(scope, operator, container,
                                                 model):
    # Computational graph:
    #
    # In the following graph, variable names are in lower case characters only
    # and operator names are in upper case characters. We borrow operator names
    # from the official ONNX spec:
    # https://github.com/onnx/onnx/blob/master/docs/Operators.md
    # All variables are followed by their shape in [].
    #
    # Symbols:
    # M: Number of instances
    # N: Number of features
    # C: Number of classes
    # CLASSIFIERCONVERTER: classifier converter corresponding to the op_type
    # a: slope in sigmoid model
    # b: intercept in sigmoid model
    # k: variable in the range [0, C)
    # input: input
    # class_prob_tensor: tensor with class probabilities(function output)
    #
    # Graph:
    #
    #   input [M, N] -> CLASSIFIERCONVERTER -> label [M]
    #                          |
    #                          V
    #                    probability_tensor [M, C]
    #                          |
    #         .----------------'---------.
    #         |                          |
    #         V                          V
    # ARRAYFEATUREEXTRACTOR <- k [1] -> ARRAYFEATUREEXTRACTOR
    #         |                          |
    #         V                          V
    #  transposed_df_col[M, 1] transposed_df_col[M, 1]
    #       |--------------------------|----------.--------------------------.
    #       |                          |          |                          |
    #       |if model.method='sigmoid' |          |if model.method='isotonic'|
    #       |                          |          |                          |
    #       V                          V          |if out_of_bounds='clip'   |
    #      MUL <-------- a -------->  MUL         V                          V
    #       |                          |          CLIP     ...             CLIP
    #       V                          V          |                          |
    #  a_df_prod [M, 1]  ... a_df_prod [M, 1]     V                          V
    #       |                          |  clipped_df [M, 1]...clipped_df [M, 1]
    #       V                          V          |                          |
    #      ADD <--------- b ---------> ADD        '-------------------.------'
    #         |                          |                            |
    #         V                          V                            |
    #  exp_parameter [M, 1] ...   exp_parameter [M, 1]                |
    #         |                          |                            |
    #         V                          V                            |
    #        EXP        ...             EXP                           |
    #         |                          |                            |
    #         V                          V                            |
    #  exp_result [M, 1]  ...    exp_result [M, 1]                    |
    #         |                          |                            |
    #         V                          V                            |
    #       ADD <------- unity -------> ADD                           |
    #         |                          |                            |
    #         V                          V                            |
    #  denominator [M, 1]  ...   denominator [M, 1]                   |
    #         |                          |                            |
    #         V                          V                            |
    #        DIV <------- unity ------> DIV                           |
    #         |                          |                            |
    #         V                          V                            |
    # sigmoid_predict_result [M, 1] ... sigmoid_predict_result [M, 1] |
    #         |                          |                            |
    #         '-----.--------------------'                            |
    #               |-------------------------------------------------'
    #               |
    #               V
    #            CONCAT -> concatenated_prob [M, C]
    #                          |
    #        if  C = 2         |  if C != 2
    #      .-------------------'---------------------------.---------.
    #      |                                               |         |
    #      V                                               |         V
    # ARRAYFEATUREEXTRACTOR <- col_number [1]              |    REDUCESUM
    #                   |                                  |         |
    #                   '--------------------------------. |         |
    # unit_float_tensor [1] -> SUB <- first_col [M, 1] <-' |         |
    #                           |                         /          |
    #                           V                        V           V
    #                         CONCAT                    DIV <- reduced_prob [M]
    #                           |                        |
    #                           V                        |
    #                        class_prob_tensor [M, C] <--'

    base_model = model.base_estimator
    op_type = sklearn_operator_name_map[type(base_model)]
    n_classes = len(model.classes_)
    prob_name = [None] * n_classes

    this_operator = scope.declare_local_operator(op_type)
    this_operator.raw_operator = base_model
    this_operator.inputs = operator.inputs
    label_name = scope.declare_local_variable('label')
    df_name = scope.declare_local_variable('probability_tensor',
                                           FloatTensorType())
    this_operator.outputs.append(label_name)
    this_operator.outputs.append(df_name)
    df_inp = df_name.full_name

    for k in range(n_classes):
        cur_k = k
        if n_classes == 2:
            cur_k += 1
            # In case of binary classification, SVMs only return
            # scores for the positive class. We concat the same
            # column twice as we just use the second column.
            if op_type in ('SklearnLinearSVC', 'SklearnSVC'):
                df_input_name = scope.get_unique_variable_name('df_input')
                merged_input_name = scope.get_unique_variable_name(
                    'merged_input')

                apply_reshape(scope, df_inp,
                              df_input_name, container,
                              desired_shape=(-1, 1))
                apply_concat(scope, [df_input_name, df_input_name],
                             merged_input_name, container, axis=1)
                df_inp = merged_input_name
        k_name = scope.get_unique_variable_name('k')
        df_col_name = scope.get_unique_variable_name('transposed_df_col')
        prob_name[k] = scope.get_unique_variable_name('prob_{}'.format(k))

        container.add_initializer(k_name, onnx_proto.TensorProto.INT64,
                                  [], [cur_k])

        container.add_node(
            'ArrayFeatureExtractor', [df_inp, k_name], df_col_name,
            name=scope.get_unique_operator_name('ArrayFeatureExtractor'),
            op_domain='ai.onnx.ml')
        T = (_transform_sigmoid(scope, container, model, df_col_name, k)
             if model.method == 'sigmoid' else
             _transform_isotonic(scope, container, model, df_col_name, k))

        prob_name[k] = T
        if n_classes == 2:
            break

    if n_classes == 2:
        zeroth_col_name = scope.get_unique_variable_name('zeroth_col')
        merged_prob_name = scope.get_unique_variable_name('merged_prob')
        unit_float_tensor_name = scope.get_unique_variable_name(
            'unit_float_tensor')

        container.add_initializer(unit_float_tensor_name,
                                  onnx_proto.TensorProto.FLOAT, [], [1.0])

        apply_sub(scope, [unit_float_tensor_name, prob_name[0]],
                  zeroth_col_name, container, broadcast=1)
        apply_concat(scope, [zeroth_col_name, prob_name[0]],
                     merged_prob_name, container, axis=1)
        class_prob_tensor_name = merged_prob_name
    else:
        concatenated_prob_name = scope.get_unique_variable_name(
            'concatenated_prob')
        reduced_prob_name = scope.get_unique_variable_name('reduced_prob')
        calc_prob_name = scope.get_unique_variable_name('calc_prob')

        apply_concat(scope, prob_name, concatenated_prob_name,
                     container, axis=1)
        container.add_node('ReduceSum', concatenated_prob_name,
                           reduced_prob_name, axes=[1],
                           name=scope.get_unique_operator_name('ReduceSum'))
        num, deno = _handle_zeros(scope, container, concatenated_prob_name,
                                  reduced_prob_name, n_classes)
        apply_div(scope, [num, deno],
                  calc_prob_name, container, broadcast=1)
        class_prob_tensor_name = calc_prob_name
    return class_prob_tensor_name


def convert_sklearn_calibrated_classifier_cv(scope, operator, container):
    # Computational graph:
    #
    # In the following graph, variable names are in lower case characters only
    # and operator names are in upper case characters. We borrow operator names
    # from the official ONNX spec:
    # https://github.com/onnx/onnx/blob/master/docs/Operators.md
    # All variables are followed by their shape in [].
    #
    # Symbols:
    # M: Number of instances
    # N: Number of features
    # C: Number of classes
    # CONVERT_BASE_ESTIMATOR: base estimator convert function defined above
    # clf_length: number of calibrated classifiers
    # input: input
    # output: output
    # class_prob: class probabilities
    #
    # Graph:
    #
    #                         input [M, N]
    #                               |
    #           .-------------------|--------------------------.
    #           |                   |                          |
    #           V                   V                          V
    # CONVERT_BASE_ESTIMATOR  CONVERT_BASE_ESTIMATOR ... CONVERT_BASE_ESTIMATOR
    #           |                   |                          |
    #           V                   V                          V
    #  prob_scores_0 [M, C] prob_scores_1 [M, C] ... prob_scores_(clf_length-1)
    #           |                   |                          |  [M, C]
    #           '-------------------|--------------------------'
    #                               V
    #       add_result [M, C] <--- SUM
    #           |
    #           '--> DIV <- clf_length [1]
    #                 |
    #                 V
    #            class_prob [M, C] -> ARGMAX -> argmax_output [M, 1]
    #                                                   |
    #             classes -> ARRAYFEATUREEXTRACTOR  <---'
    #                               |
    #                               V
    #                            output [1]

    op = operator.raw_operator
    classes = op.classes_
    output_shape = (-1,)
    class_type = onnx_proto.TensorProto.STRING

    if np.issubdtype(op.classes_.dtype, np.floating):
        class_type = onnx_proto.TensorProto.INT32
        classes = classes.astype(np.int32)
    elif np.issubdtype(op.classes_.dtype, np.signedinteger):
        class_type = onnx_proto.TensorProto.INT32
    else:
        classes = np.array([s.encode('utf-8') for s in classes])

    clf_length = len(op.calibrated_classifiers_)
    prob_scores_name = []

    clf_length_name = scope.get_unique_variable_name('clf_length')
    classes_name = scope.get_unique_variable_name('classes')
    reshaped_result_name = scope.get_unique_variable_name('reshaped_result')
    argmax_output_name = scope.get_unique_variable_name('argmax_output')
    array_feature_extractor_result_name = scope.get_unique_variable_name(
        'array_feature_extractor_result')
    add_result_name = scope.get_unique_variable_name('add_result')

    container.add_initializer(classes_name, class_type, classes.shape, classes)
    container.add_initializer(clf_length_name, onnx_proto.TensorProto.FLOAT,
                              [], [clf_length])

    for clf in op.calibrated_classifiers_:
        prob_scores_name.append(convert_calibrated_classifier_base_estimator(
            scope, operator, container, clf))

    container.add_node('Sum', [s for s in prob_scores_name],
                       add_result_name, op_version=7,
                       name=scope.get_unique_operator_name('Sum'))
    apply_div(scope, [add_result_name, clf_length_name],
              operator.outputs[1].full_name, container, broadcast=1)
    class_prob_name = operator.outputs[1].full_name
    container.add_node('ArgMax', class_prob_name,
                       argmax_output_name,
                       name=scope.get_unique_operator_name('ArgMax'), axis=1)
    container.add_node(
        'ArrayFeatureExtractor', [classes_name, argmax_output_name],
        array_feature_extractor_result_name, op_domain='ai.onnx.ml',
        name=scope.get_unique_operator_name('ArrayFeatureExtractor'))

    if class_type == onnx_proto.TensorProto.INT32:
        apply_reshape(scope, array_feature_extractor_result_name,
                      reshaped_result_name, container,
                      desired_shape=output_shape)
        apply_cast(scope, reshaped_result_name, operator.outputs[0].full_name,
                   container, to=onnx_proto.TensorProto.INT64)
    else:
        apply_reshape(scope, array_feature_extractor_result_name,
                      operator.outputs[0].full_name, container,
                      desired_shape=output_shape)


register_converter('SklearnCalibratedClassifierCV',
                   convert_sklearn_calibrated_classifier_cv)
