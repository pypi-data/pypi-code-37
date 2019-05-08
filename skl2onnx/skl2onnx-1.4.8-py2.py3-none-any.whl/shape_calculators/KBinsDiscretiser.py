# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from ..common.data_types import FloatTensorType, Int64TensorType
from ..common._registration import register_shape_calculator
from ..common.utils import check_input_and_output_numbers
from ..common.utils import check_input_and_output_types


def calculate_sklearn_k_bins_discretiser(operator):
    check_input_and_output_numbers(operator, output_count_range=1)
    check_input_and_output_types(operator, good_input_types=[
                                 FloatTensorType, Int64TensorType])

    M = operator.inputs[0].type.shape[0]
    model = operator.raw_operator
    N = len(model.n_bins_) if model.encode == 'ordinal' else sum(model.n_bins_)
    operator.outputs[0].type = FloatTensorType([M, N])


register_shape_calculator('SklearnKBinsDiscretizer',
                          calculate_sklearn_k_bins_discretiser)
