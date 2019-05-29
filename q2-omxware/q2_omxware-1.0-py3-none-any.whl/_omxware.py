

import omxware
import numpy as np
import pandas as pd
import qiime2

from typing import List, Optional
from q2_types.feature_data import FeatureData, Sequence
from ._util import connect_to_omxware

# Get gene sequences from OMXWare based on query gene name, list of genome ids, list of genus names or/and list of go terms
# 		- Make sure at least one of the input parameter is not empty
# 		- If all input parameters are empty throw a ValueError
#		- Connect to OMXWare and retrieve genes based on input parameters
#		- Create a pandas Series object with sequences as data and genes description as index
#		- And return that pandas Series object, it will be converted to a fasta file by Qiime2 interfaces
def genes(gene_names: str = "",
                genome_ids: List[str] = None,
                genus_names: List[str] = None,
                go_terms: List[str] = None,
                max_results: int = 10000) -> pd.Series:

    if gene_names or genome_ids or genus_names or go_terms:
        pass
    else:
        raise ValueError("At least one input parameter among gene_names/genome_ids/genus_names/go_terms is required.")

    omx = connect_to_omxware()

    total_results = min(omx.genes(gene_name=gene_names, 
                                  genome_ids=genome_ids, 
                                  genus_names=genus_names, 
                                  go_terms=go_terms, 
                                  page_size=0).total_results(), max_results)
    all_responses = []
    page_number = 0
    while total_results > 0:
        page_size = 1000 if total_results >= 1000 else total_results
        total_results -= page_size
        page_number += 1
        all_responses += omx.genes(gene_name=gene_names,
                                   genome_ids=genome_ids,
                                   go_terms=go_terms,
                                   page_size=page_size,
                                   page_number=page_number).results()

    gene_names = [gene.id() + ' ' + gene.name() for gene in all_responses]
    gene_sequences = [gene.sequence() for gene in all_responses]
    df_genes = pd.Series(index = gene_names, data = gene_sequences)
    df_genes = df_genes.drop_duplicates()
    return df_genes
