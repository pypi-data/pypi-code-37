# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import q2_omxware
from ._omxware import genes

from q2_types.feature_data import FeatureData, Sequence
from qiime2.plugin import Int, Plugin, Range, Str, List


plugin = Plugin(
    name='omxware',
    version=q2_omxware.__version__,
    website='http://omxware.sl.cloud9.ibm.com/discovery',
    package='q2_omxware',
    description=('This QIIME 2 plugin wraps OMXWare SDK.'
                 'Retrieves -omics data from OMXWare and'
                 'export it as Qiime2 artifact.'),
    short_description='Plugin for accessing OMXWare'
)

plugin.methods.register_function(
    function=genes,
    inputs={},
    parameters={'gene_names': Str,
                'genome_ids': List[Str],
                'genus_names': List[Str],
                'go_terms': List[Str],
                'max_results': Int % Range(0, 1000000, inclusive_end=True),
               },
    outputs=[('genes', FeatureData[Sequence])],
    input_descriptions={},
    parameter_descriptions={
        'gene_names': 'keyword describing genes',
        'genome_ids': 'list of omxware genome ids',
        'genus_names': 'list of genus names',
        'go_terms': 'list of go terms',
        'max_results': 'maximun number of genes',
        },
    output_descriptions={
        'genes': 'Gene sequences for the genes matching gene_names'},
    name='genes',
    description='Retrieve genes from OMXWare based on gene_names/genome_ids/genus_names/go_terms'
)