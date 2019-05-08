#    This script is part of navis (http://www.github.com/schlegelp/navis).
#    Copyright (C) 2018 Philipp Schlegel
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.


""" This module contains functions to analyse and manipulate neuron morphology.
"""

import math
import itertools

import pandas as pd
import numpy as np
import scipy.spatial.distance
import networkx as nx

from .. import core, graph, utils, config, sampling
from . import metrics

# Set up logging
logger = config.logger

__all__ = sorted(['prune_by_strahler', 'stitch_neurons', 'split_axon_dendrite',
                  'average_neurons', 'despike_neuron', 'guess_radius',
                  'smooth_neuron', 'heal_fragmented_neuron',
                  'break_fragments'])


def prune_by_strahler(x, to_prune, reroot_soma=True, inplace=False,
                      force_strahler_update=False, relocate_connectors=False):
    """ Prune neuron based on `Strahler order
    <https://en.wikipedia.org/wiki/Strahler_number>`_.

    Parameters
    ----------
    x :             TreeNeuron | NeuronList
    to_prune :      int | list | range | slice
                    Strahler indices (SI) to prune. For example:

                    1. ``to_prune=1`` removes all leaf branches
                    2. ``to_prune=[1, 2]`` removes SI 1 and 2
                    3. ``to_prune=range(1, 4)`` removes SI 1, 2 and 3
                    4. ``to_prune=slice(0, -1)`` removes everything but the
                       highest SI
                    5. ``to_prune=slice(-1, None)`` removes only the highest
                       SI

    reroot_soma :   bool, optional
                    If True, neuron will be rerooted to its soma.
    inplace :       bool, optional
                    If False, pruning is performed on copy of original neuron
                    which is then returned.
    relocate_connectors : bool, optional
                          If True, connectors on removed treenodes will be
                          reconnected to the closest still existing treenode.
                          Works only in child->parent direction.

    Returns
    -------
    TreeNeuron/List
                    Pruned neuron(s).

    """

    if isinstance(x, core.TreeNeuron):
        neuron = x
    elif isinstance(x, core.NeuronList):
        temp = [prune_by_strahler(
            n, to_prune=to_prune, inplace=inplace) for n in x]
        if not inplace:
            return core.NeuronList(temp, x._remote_instance)
        else:
            return

    # Make a copy if necessary before making any changes
    if not inplace:
        neuron = neuron.copy()

    if reroot_soma and neuron.soma:
        neuron.reroot(neuron.soma)

    if 'strahler_index' not in neuron.nodes or force_strahler_update:
        strahler_index(neuron)

    # Prepare indices
    if isinstance(to_prune, int) and to_prune < 0:
        to_prune = range(1, neuron.nodes.strahler_index.max() + (to_prune + 1))

    if isinstance(to_prune, int):
        if to_prune < 1:
            raise ValueError('SI to prune must be positive. Please see help'
                             'for additional options.')
        to_prune = [to_prune]
    elif isinstance(to_prune, range):
        to_prune = list(to_prune)
    elif isinstance(to_prune, slice):
        SI_range = range(1, neuron.nodes.strahler_index.max() + 1)
        to_prune = list(SI_range)[to_prune]

    # Prepare parent dict if needed later
    if relocate_connectors:
        parent_dict = {
            tn.node_id: tn.parent_id for tn in neuron.nodes.itertuples()}

    neuron.nodes = neuron.nodes[
        ~neuron.nodes.strahler_index.isin(to_prune)].reset_index(drop=True)

    if not relocate_connectors:
        neuron.connectors = neuron.connectors[neuron.connectors.node_id.isin(
            neuron.nodes.node_id.values)].reset_index(drop=True)
    else:
        remaining_tns = set(neuron.nodes.node_id.values)
        for cn in neuron.connectors[~neuron.connectors.node_id.isin(neuron.nodes.node_id.values)].itertuples():
            this_tn = parent_dict[cn.node_id]
            while True:
                if this_tn in remaining_tns:
                    break
                this_tn = parent_dict[this_tn]
            neuron.connectors.loc[cn.Index, 'node_id'] = this_tn

    # Reset indices of node and connector tables (important for igraph!)
    neuron.nodes.reset_index(inplace=True, drop=True)
    neuron.connectors.reset_index(inplace=True, drop=True)

    # Theoretically we can end up with disconnected pieces, i.e. with more
    # than 1 root node -> we have to fix the nodes that lost their parents
    neuron.nodes.loc[~neuron.nodes.parent_id.isin(
        neuron.nodes.node_id.values), 'parent_id'] = None

    # Remove temporary attributes
    neuron._clear_temp_attr()

    if not inplace:
        return neuron
    else:
        return


def split_axon_dendrite(x, method='bending', primary_neurite=True,
                        reroot_soma=True, return_point=False):
    """ Split a neuron into axon, dendrite and primary neurite.

    The result is highly dependent on the method and on your neuron's
    morphology and works best for "typical" neurons, i.e. those where the
    primary neurite branches into axon and dendrites.

    Parameters
    ----------
    x :                 TreeNeuron | NeuronList
                        Neuron(s) to split into axon, dendrite (and primary
                        neurite).
    method :            'centrifugal' | 'centripetal' | 'sum' | 'bending', optional
                        Type of flow centrality to use to split the neuron.
                        There are four flavors: the first three refer to
                        :func:`~navis.flow_centrality`, the last
                        refers to :func:`~navis.bending_flow`.

                        Will try using stored centrality, if possible.
    primary_neurite :   bool, optional
                        If True and the split point is at a branch point, will
                        try splittig into axon, dendrite and primary neurite.
                        Works only with ``method=bending``!
    reroot_soma :       bool, optional
                        If True, will make sure neuron is rooted to soma if at
                        all possible.
    return_point :      bool, optional
                        If True, will only return treenode ID of the node at
                        which to split the neuron.

    Returns
    -------
    NeuronList
                        Axon, dendrite and primary neurite.

    Examples
    --------
    >>> x = navis.example_neurons()
    >>> split = navis.split_axon_dendrite(x, method='centrifugal',
    ...                                    reroot_soma=True)
    >>> split
    <class 'navis.NeuronList'> of 3 neurons
                          neuron_name skeleton_id  n_nodes  n_connectors
    0  neuron 123457_primary_neurite          16      148             0
    1             neuron 123457_axon          16     9682          1766
    2         neuron 123457_dendrite          16     2892           113
    >>> # For convenience, split_axon_dendrite assigns colors to the resulting
    >>> # fragments: axon = red, dendrites = blue, primary neurite = green
    >>> split.plot3d(color=split.color)

    """

    if isinstance(x, core.NeuronList) and len(x) == 1:
        x = x[0]
    elif isinstance(x, core.NeuronList):
        nl = []
        for n in config.tqdm(x, desc='Splitting', disable=config.pbar_hide,
                             leave=config.pbar_leave):
            nl.append(split_axon_dendrite(n,
                                          method=method,
                                          primary_neurite=primary_neurite,
                                          reroot_soma=reroot_soma,
                                          return_point=return_point))
        return core.NeuronList([n for l in nl for n in l])

    if not isinstance(x, core.TreeNeuron):
        raise TypeError('Can only process TreeNeuron, '
                        'got "{}"'.format(type(x)))

    if method not in ['centrifugal', 'centripetal', 'sum', 'bending']:
        raise ValueError('Unknown parameter for mode: {0}'.format(method))

    if primary_neurite and method != 'bending':
        logger.warning('Primary neurite splits only works well with '
                       'method "bending"')

    if x.soma and x.soma not in x.root and reroot_soma:
        x.reroot(x.soma)

    # Calculate flow centrality if necessary
    try:
        last_method = x.centrality_method
    except BaseException:
        last_method = None

    if last_method != method:
        if method == 'bending':
            _ = bending_flow(x)
        elif method in ['centripetal', 'centrifugal', 'sum']:
            _ = flow_centrality(x, mode=method)
        else:
            raise ValueError('Unknown method "{}"'.format(method))

    # Make copy, so that we don't screw things up
    x = x.copy()

    # Now get the node point with the highest flow centrality.
    cut = x.nodes[x.nodes.flow_centrality ==
                  x.nodes.flow_centrality.max()].node_id.values

    # If there is more than one point we need to get one closest to the soma
    # (root)
    if len(cut) > 1:
        cut = sorted(cut, key=lambda y: graph_utils.dist_between(
            x.graph, y, x.root[0]))[0]
    else:
        cut = cut[0]

    if return_point:
        return cut

    # If cut node is a branch point, we will try cutting off main neurite
    if x.graph.degree(cut) > 2 and primary_neurite:
        # First make sure that there are no other branch points with flow
        # between this one and the soma
        path_to_root = nx.shortest_path(x.graph, cut, x.root[0])

        # Get flow centrality along the path
        flows = x.nodes.set_index('node_id').loc[path_to_root]

        # Subset to those that are branches (exclude mere synapses)
        flows = flows[flows.type == 'branch']

        # Find the first branch point from the soma with no flow (fillna is
        # important!)
        last_with_flow = np.where(flows.flow_centrality.fillna(0).values > 0)[0][-1]

        if method != 'bending':
            last_with_flow += 1

        to_cut = flows.iloc[last_with_flow].name

        # Cut off primary neurite
        rest, primary_neurite = graph_utils.cut_neuron(x, to_cut)

        if method == 'bending':
            # The new cut node has to be a child of the original cut node
            cut = next(x.graph.predecessors(cut))

        # Change name and color
        primary_neurite.neuron_name = x.neuron_name + '_primary_neurite'
        primary_neurite.color = (0, 255, 0)
        primary_neurite.type = 'primary_neurite'
    else:
        rest = x
        primary_neurite = None

    # Next, cut the rest into axon and dendrite
    a, b = graph_utils.cut_neuron(rest, cut)

    # Figure out which one is which by comparing fraction of in- to outputs
    a_inout = a.n_postsynapses/a.n_presynapses if a.n_presynapses else float('inf')
    b_inout = b.n_postsynapses/b.n_presynapses if b.n_presynapses else float('inf')
    if a_inout > b_inout:
        dendrite, axon = a, b
    else:
        dendrite, axon = b, a

    axon.neuron_name = x.neuron_name + '_axon'
    dendrite.neuron_name = x.neuron_name + '_dendrite'

    axon.type = 'axon'
    dendrite.type = 'dendrite'

    # Change colors
    axon.color = (255, 0, 0)
    dendrite.color = (0, 0, 255)

    if primary_neurite:
        return core.NeuronList([primary_neurite, axon, dendrite])
    else:
        return core.NeuronList([axon, dendrite])


def stitch_neurons(*x, method='LEAFS', master='SOMA', tn_to_stitch=None):
    """ Stitch multiple neurons together.

    Uses minimum spanning tree to determine a way to connect all fragments
    while minimizing length (eucledian distance) of the new edges. Nodes
    that have been stitched will be get a "stitched" tag.

    Important
    ---------
    If duplicate node IDs are found across the fragments to stitch they will
    be remapped to new, unique values!

    Parameters
    ----------
    x :                 Neuron | NeuronList | list of either
                        Neurons to stitch (see examples).
    method :            'LEAFS' | 'ALL' | 'NONE', optional
                        Set stitching method:
                            (1) 'LEAFS': Only leaf (including root) nodes will
                                be allowed to make new edges.
                            (2) 'ALL': All treenodes are considered.
                            (3) 'NONE': Node and connector tables will simply
                                be combined without generating any new edges.
                                The resulting neuron will have multiple roots.
    master :            'SOMA' | 'LARGEST' | 'FIRST', optional
                        Sets the master neuron:
                            (1) 'SOMA': The largest fragment with a soma
                                becomes the master neuron. If no neuron with
                                soma, will pick the largest.
                            (2) 'LARGEST': The largest fragment becomes the
                                master neuron.
                            (3) 'FIRST': The first fragment provided becomes
                                the master neuron.
    tn_to_stitch :      List of treenode IDs, optional
                        If provided, these treenodes will be preferentially
                        used to stitch neurons together. Overrides methods
                        ``'ALL'`` or ``'LEAFS'``.

    Returns
    -------
    core.TreeNeuron
                        Stitched neuron.

    Examples
    --------
    Stitching neuronlist by simply combining data tables:

    >>> nl = navis.example_neurons()
    >>> stitched = navis.stitch_neurons(nl, method='NONE')

    Stitching fragmented neurons:
    >>> a = navis.example_neurons(1)
    >>> fragments = navis.cut_neuron(a, 100)
    >>> stitched = navis.stitch_neurons(frag, method='LEAFS')

    """
    method = str(method).upper()
    master = str(master).upper()

    if method not in ['LEAFS', 'ALL', 'NONE']:
        raise ValueError('Unknown method: %s' % str(method))

    if master not in ['SOMA', 'LARGEST', 'FIRST']:
        raise ValueError('Unknown master: %s' % str(master))

    # Compile list of individual neurons
    x = utils.unpack_neurons(x)

    # Use copies of the original neurons!
    x = core.NeuronList(x).copy()

    if len(x) < 2:
        logger.warning('Need at least 2 neurons to stitch, '
                       'found %i' % len(x))
        return x[0]

    # First find master
    if master == 'SOMA':
        has_soma = [n for n in x if not isinstance(n.soma, type(None))]
        if len(has_soma) > 0:
            master = has_soma[0]
        else:
            master = sorted(x.neurons,
                            key=lambda x: x.cable_length,
                            reverse=True)[0]
    elif master == 'LARGEST':
        master = sorted(x.neurons,
                        key=lambda x: x.cable_length,
                        reverse=True)[0]
    else:
        # Simply pick the first neuron
        master = x[0]

    # Check if we need to make any node IDs unique
    if x.nodes.duplicated(subset='node_id').sum() > 0:
        seen_tn = set(master.nodes.node_id)
        for n in [n for n in x if n != master]:
            this_tn = set(n.nodes.node_id)

            # Get duplicate node IDs
            non_unique = seen_tn & this_tn

            # Add this neuron's existing nodes to seen
            seen_tn = seen_tn | this_tn
            if non_unique:
                # Generate new, unique node IDs
                new_tn = np.arange(0, len(non_unique)) + max(seen_tn) + 1

                # Generate new map
                new_map = dict(zip(non_unique, new_tn))

                # Remap node IDs - if no new value, keep the old
                n.nodes.node_id = n.nodes.node_id.map(lambda x: new_map.get(x, x))

                if n.has_connectors:
                    n.connectors.node_id = n.connectors.node_id.map(lambda x: new_map.get(x, x))

                if hasattr(n, 'tags'):
                    n.tags = {new_map.get(k, k): v for k, v in n.tags.items()}

                # Remapping parent IDs requires the root to be temporarily set
                # to -1. Otherwise the node IDs will become floats
                new_map[None] = -1
                n.nodes.parent_id = n.nodes.parent_id.map(lambda x: new_map.get(x, x)).astype(object)
                n.nodes.loc[n.nodes.parent_id == -1, 'parent_id'] = None

                # Add new nodes to seen
                seen_tn = seen_tn | set(new_tn)

                # Make sure the graph is updated
                n._clear_temp_attr()

    # If method is none, we can just merge the data tables
    if method == 'NONE' or method is None:
        master.nodes = pd.concat([n.nodes for n in x],
                                 ignore_index=True)

        if any(x.has_connectors):
            master.connectors = pd.concat([x.connectors for n in x],
                                          ignore_index=True)

        master.tags = {}
        for n in x:
            master.tags.update(getattr(n, 'tags', {}))

        # Reset temporary attributes of our final neuron
        master._clear_temp_attr()

        return master

    # Fix potential problems with tn_to_stitch
    if not isinstance(tn_to_stitch, type(None)):
        if not isinstance(tn_to_stitch, (list, np.ndarray)):
            tn_to_stitch = [tn_to_stitch]

        # Make sure we're working with integers
        tn_to_stitch = [int(tn) for tn in tn_to_stitch]

    # Generate a union of all graphs
    g = nx.union_all([n.graph for n in x]).to_undirected()

    # Set existing edges to zero weight to make sure they remain when
    # calculating the minimum spanning tree
    nx.set_edge_attributes(g, 0, 'weight')

    # If two nodes occupy the same position (e.g. after if fragments are the
    # result of cutting), they will have a distance of 0. Hence, we won't be
    # able to simply filter by distance
    nx.set_edge_attributes(g, False, 'new')

    # Now iterate over every possible combination of fragments
    for a, b in itertools.combinations(x, 2):
        # Collect relevant treenodes
        if not isinstance(tn_to_stitch, type(None)):
            tnA = a.nodes.loc[a.nodes.node_id.isin(tn_to_stitch)]
            tnB = b.nodes.loc[a.nodes.node_id.isin(tn_to_stitch)]
        else:
            tnA = pd.DataFrame([])
            tnB = pd.DataFrame([])

        if tnA.empty:
            if method == 'LEAFS':
                tnA = a.nodes.loc[a.nodes['type'].isin(['end', 'root'])]
            else:
                tnA = a.nodes
        if tnB.empty:
            if method == 'LEAFS':
                tnB = b.nodes.loc[b.nodes['type'].isin(['end', 'root'])]
            else:
                tnB = b.nodes

        # Get distance between treenodes in A and B
        d = scipy.spatial.distance.cdist(tnA[['x', 'y', 'z']].values,
                                         tnB[['x', 'y', 'z']].values,
                                         metric='euclidean')

        # List of edges
        tn_comb = itertools.product(tnA.node_id.values, tnB.node_id.values)

        # Add edges to union graph
        g.add_edges_from([(a, b, {'weight': w, 'new': True}) for (a, b), w in zip(tn_comb, d.ravel())])

    # Get minimum spanning tree
    edges = nx.minimum_spanning_edges(g)

    # Edges that need adding are those that were newly added
    to_add = [e for e in edges if e[2]['new']]

    # Keep track of original master root
    master_root = master.root[0]

    # Generate one big neuron
    master.nodes = x.nodes

    if any(x.has_connectors):
        master.connectors = x.connectors

    if any([hasattr(n, 'tags') for n in x]):
        master.tags = {}
        for n in x:
            master.tags.update(getattr(n, 'tags', {}))

    # Clear temporary attributes
    master._clear_temp_attr()

    for e in to_add:
        # Reroot to one of the nodes in the edge
        master.reroot(e[0], inplace=True)

        # Connect the nodes
        master.nodes.loc[master.nodes.node_id == e[0], 'parent_id'] = e[1]

        # Add node tags
        master.tags = getattr(master, 'tags', {})
        master.tags['stitched'] = master.tags.get('stitched', []) + [e[0], e[1]]

        # We need to regenerate the graph
        master._clear_temp_attr()

    # Reroot to original root
    master.reroot(master_root, inplace=True)

    return master


def average_neurons(x, limit=10, base_neuron=None):
    """ Computes an average from a list of neurons.

    This is a very simple implementation which may give odd results if used
    on complex neurons. Works fine on e.g. backbones or tracts.

    Parameters
    ----------
    x :             NeuronList
                    Neurons to be averaged.
    limit :         int, optional
                    Max distance for nearest neighbour search.
    base_neuron :   skeleton_ID | TreeNeuron, optional
                    Neuron to use as template for averaging. If not provided,
                    the first neuron in the list is used as template!

    Returns
    -------
    TreeNeuron

    Examples
    --------
    >>> # Get a bunch of neurons
    >>> da2 = navis.example_neurons()
    >>> # Prune down to longest neurite
    >>> da2.reroot(da2.soma)
    >>> da2_pr = da2.prune_by_longest_neurite(inplace=False)
    >>> # Make average
    >>> da2_avg = navis.average_neurons(da2_pr)
    >>> # Plot
    >>> da2.plot3d()
    >>> da2_avg.plot3d()

    """

    if not isinstance(x, core.NeuronList):
        raise TypeError('Need NeuronList, got "{0}"'.format(type(x)))

    if len(x) < 2:
        raise ValueError('Need at least 2 neurons to average!')

    # Generate KDTrees for each neuron
    for n in x:
        n.tree = graph.neuron2KDTree(n, tree_type='c', data='treenodes')

    # Set base for average: we will use this neurons treenodes to query
    # the KDTrees
    if isinstance(base_neuron, core.TreeNeuron):
        base_neuron = base_neuron.copy()
    elif isinstance(base_neuron, int):
        base_neuron = x.skid[base_neuron].copy
    elif isinstance(base_neuron, type(None)):
        base_neuron = x[0].copy()
    else:
        raise ValueError('Unable to interpret base_neuron of '
                         'type "{0}"'.format(type(base_neuron)))

    base_nodes = base_neuron.nodes[['x', 'y', 'z']].values
    other_neurons = x[1:]

    # Make sure these stay 2-dimensional arrays -> will add a colum for each
    # "other" neuron
    base_x = base_nodes[:, 0:1]
    base_y = base_nodes[:, 1:2]
    base_z = base_nodes[:, 2:3]

    # For each "other" neuron, collect nearest neighbour coordinates
    for n in other_neurons:
        nn_dist, nn_ix = n.tree.query(
            base_nodes, k=1, distance_upper_bound=limit)

        # Translate indices into coordinates
        # First, make empty array
        this_coords = np.zeros((len(nn_dist), 3))
        # Set coords without a nearest neighbour within distances to "None"
        this_coords[nn_dist == float('inf')] = None
        # Fill in coords of nearest neighbours
        this_coords[nn_dist != float(
            'inf')] = n.tree.data[nn_ix[nn_dist != float('inf')]]
        # Add coords to base coords
        base_x = np.append(base_x, this_coords[:, 0:1], axis=1)
        base_y = np.append(base_y, this_coords[:, 1:2], axis=1)
        base_z = np.append(base_z, this_coords[:, 2:3], axis=1)

    # Calculate means
    mean_x = np.mean(base_x, axis=1)
    mean_y = np.mean(base_y, axis=1)
    mean_z = np.mean(base_z, axis=1)

    # If any of the base coords has NO nearest neighbour within limit
    # whatsoever, the average of that row will be "NaN" -> in this case we
    # will fall back to the base coordinate
    mean_x[np.isnan(mean_x)] = base_nodes[np.isnan(mean_x), 0]
    mean_y[np.isnan(mean_y)] = base_nodes[np.isnan(mean_y), 1]
    mean_z[np.isnan(mean_z)] = base_nodes[np.isnan(mean_z), 2]

    # Change coordinates accordingly
    base_neuron.nodes.loc[:, 'x'] = mean_x
    base_neuron.nodes.loc[:, 'y'] = mean_y
    base_neuron.nodes.loc[:, 'z'] = mean_z

    return base_neuron


def despike_neuron(x, sigma=5, max_spike_length=1, inplace=False,
                   reverse=False):
    """ Removes spikes in neuron traces (e.g. from jumps in image data).

    For each treenode A, the euclidean distance to its next successor (parent)
    B and that node's successor is computed. If
    :math:`\\frac{dist(A,B)}{dist(A,C)}>sigma`, node B is considered a spike
    and realigned between A and C.

    Parameters
    ----------
    x :                 TreeNeuron | NeuronList
                        Neuron(s) to be processed.
    sigma :             float | int, optional
                        Threshold for spike detection. Smaller sigma = more
                        aggressive spike detection.
    max_spike_length :  int, optional
                        Determines how long (# of nodes) a spike can be.
    inplace :           bool, optional
                        If False, a copy of the neuron is returned.
    reverse :           bool, optional
                        If True, will **also** walk the segments from proximal
                        to distal. Use this to catch spikes on e.g. terminal
                        nodes.

    Returns
    -------
    TreeNeuron/List
                Despiked neuron(s). Only if ``inplace=False``.

    """

    # TODO:
    # - flattening all segments first before Spike detection should speed up
    #   quite a lot
    # -> as intermediate step: assign all new positions at once

    if isinstance(x, core.NeuronList):
        if not inplace:
            x = x.copy()

        for n in config.tqdm(x, desc='Despiking', disable=config.pbar_hide,
                             leave=config.pbar_leave):
            despike_neuron(n, sigma=sigma, inplace=True)

        if not inplace:
            return x
        return
    elif not isinstance(x, core.TreeNeuron):
        raise TypeError('Can only process TreeNeuron or NeuronList, '
                        'not "{0}"'.format(type(x)))

    if not inplace:
        x = x.copy()

    # Index treenodes table by treenode ID
    this_treenodes = x.nodes.set_index('node_id')

    segs_to_walk = x.segments

    if reverse:
        segs_to_walk += x.segments[::-1]

    # For each spike length do -> do this in reverse to correct the long
    # spikes first
    for l in list(range(1, max_spike_length + 1))[::-1]:
        # Go over all segments
        for seg in x.segments:
            # Get nodes A, B and C of this segment
            this_A = this_treenodes.loc[seg[:-l - 1]]
            this_B = this_treenodes.loc[seg[l:-1]]
            this_C = this_treenodes.loc[seg[l + 1:]]

            # Get coordinates
            A = this_A[['x', 'y', 'z']].values
            B = this_B[['x', 'y', 'z']].values
            C = this_C[['x', 'y', 'z']].values

            # Calculate euclidian distances A->B and A->C
            dist_AB = np.linalg.norm(A - B, axis=1)
            dist_AC = np.linalg.norm(A - C, axis=1)

            # Get the spikes
            spikes_ix = np.where((dist_AB / dist_AC) > sigma)[0]
            spikes = this_B.iloc[spikes_ix]

            if not spikes.empty:
                # Interpolate new position(s) between A and C
                new_positions = A[spikes_ix] + (C[spikes_ix] - A[spikes_ix]) / 2

                this_treenodes.loc[spikes.index, ['x', 'y', 'z']] = new_positions

    # Reassign treenode table
    x.nodes = this_treenodes.reset_index(drop=False)

    # The weights in the graph have changed, we need to update that
    x._clear_temp_attr(exclude=['segments', 'small_segments',
                                'classify_nodes'])

    if not inplace:
        return x


def guess_radius(x, method='linear', limit=None, smooth=True, inplace=False):
    """ Tries guessing radii for all treenodes.

    Uses distance between connectors and treenodes and interpolate for all
    treenodes. Fills in ``radius`` column in treenode table.

    Parameters
    ----------
    x :             TreeNeuron | NeuronList
                    Neuron(s) to be processed.
    method :        str, optional
                    Method to be used to interpolate unknown radii. See
                    ``pandas.DataFrame.interpolate`` for details.
    limit :         int, optional
                    Maximum number of consecutive missing radii to fill.
                    Must be greater than 0.
    smooth :        bool | int, optional
                    If True, will smooth radii after interpolation using a
                    rolling window. If ``int``, will use to define size of
                    window.
    inplace :       bool, optional
                    If False, will use and return copy of original neuron(s).

    Returns
    -------
    TreeNeuron/List
                    If ``inplace=False``.

    """

    if isinstance(x, core.NeuronList):
        if not inplace:
            x = x.copy()

        for n in config.tqdm(x, desc='Guessing', disable=config.pbar_hide,
                             leave=config.pbar_leave):
            guess_radius(n, method=method, limit=limit, smooth=smooth,
                         inplace=True)

        if not inplace:
            return x
        return

    elif not isinstance(x, core.TreeNeuron):
        raise TypeError('Can only process TreeNeuron or NeuronList, '
                        'not "{0}"'.format(type(x)))

    if not inplace:
        x = x.copy()

    # Set default rolling window size
    if isinstance(smooth, bool) and smooth:
        smooth = 5

    # We will be using the index as distance to interpolate. For this we have
    # to change method 'linear' to 'index'
    method = 'index' if method == 'linear' else method

    # Collect connectors and calc distances
    cn = x.connectors.copy()

    # Prepare nodes (add parent_dist for later, set index)
    metrics.parent_dist(x, root_dist=0)
    nodes = x.nodes.set_index('node_id')

    # For each connector (pre and post), get the X/Y distance to its treenode
    cn_locs = cn[['x', 'y']].values
    tn_locs = nodes.loc[cn.node_id.values,
                        ['x', 'y']].values
    dist = np.sqrt(np.sum((tn_locs - cn_locs) ** 2, axis=1).astype(int))
    cn['dist'] = dist

    # Get max distance per treenode (in case of multiple connectors per
    # treenode)
    cn_grouped = cn.groupby('node_id').max()

    # Set undefined radii to None
    nodes.loc[nodes.radius <= 0, 'radius'] = None

    # Assign radii to treenodes
    nodes.loc[cn_grouped.index, 'radius'] = cn_grouped.dist.values

    # Go over each segment and interpolate radii
    for s in config.tqdm(x.segments, desc='Interp.', disable=config.pbar_hide,
                         leave=config.pbar_leave):

        # Get this segments radii and parent dist
        this_radii = nodes.loc[s, ['radius', 'parent_dist']]
        this_radii['parent_dist_cum'] = this_radii.parent_dist.cumsum()

        # Set cumulative distance as index and drop parent_dist
        this_radii = this_radii.set_index('parent_dist_cum',
                                          drop=True).drop('parent_dist',
                                                          axis=1)

        # Interpolate missing radii
        interp = this_radii.interpolate(method=method, limit_direction='both',
                                        limit=limit)

        if smooth:
            interp = interp.rolling(smooth,
                                    min_periods=1).max()

        nodes.loc[s, 'radius'] = interp.values

    # Set non-interpolated radii back to -1
    nodes.loc[nodes.radius.isnull(), 'radius'] = -1

    # Reassign nodes
    x.nodes = nodes.reset_index(drop=False)

    if not inplace:
        return x


def smooth_neuron(x, window=5, inplace=False):
    """ Smooth neuron using rolling windows.

    Parameters
    ----------
    x :             TreeNeuron | NeuronList
                    Neuron(s) to be processed.
    window :        int, optional
                    Size of the rolling window in number of nodes.
    inplace :       bool, optional
                    If False, will use and return copy of original neuron(s).

    Returns
    -------
    TreeNeuron/List
                    Smoothed neuron(s). If ``inplace=False``.

    """

    if isinstance(x, core.NeuronList):
        if not inplace:
            x = x.copy()

        for n in config.tqdm(x, desc='Smoothing', disable=config.pbar_hide,
                             leave=config.pbar_leave):
            smooth_neuron(n, window=window, inplace=True)

        if not inplace:
            return x
        return

    elif not isinstance(x, core.TreeNeuron):
        raise TypeError('Can only process TreeNeuron or NeuronList, '
                        'not "{0}"'.format(type(x)))

    if not inplace:
        x = x.copy()

    # Prepare nodes (add parent_dist for later, set index)
    metrics.parent_dist(x, root_dist=0)
    nodes = x.nodes.set_index('node_id')

    # Go over each segment and interpolate radii
    for s in config.tqdm(x.segments, desc='Smoothing',
                         disable=config.pbar_hide,
                         leave=config.pbar_leave):

        # Get this segments radii and parent dist
        this_co = nodes.loc[s, ['x', 'y', 'z', 'parent_dist']]
        this_co['parent_dist_cum'] = this_co.parent_dist.cumsum()

        # Set cumulative distance as index and drop parent_dist
        this_co = this_co.set_index('parent_dist_cum',
                                    drop=True).drop('parent_dist', axis=1)

        interp = this_co.rolling(window, min_periods=1).mean()

        nodes.loc[s, ['x', 'y', 'z']] = interp.values

    # Reassign nodes
    x.nodes = nodes.reset_index(drop=False)

    x._clear_temp_attr()

    if not inplace:
        return x


def break_fragments(x):
    """ Break neuron into continuous fragments.

    Neurons can consists of several disconnected fragments. This function
    breaks neuron(s) into disconnected components.

    Parameters
    ----------
    x :         CatmaidNeuron
                Fragmented neuron.

    Returns
    -------
    NeuronList

    See Also
    --------
    :func:`navis.heal_fragmented_neuron`
                Use to heal fragmentation instead of breaking it up.

    """
    if isinstance(x, core.NeuronList) and len(x) == 1:
        x = x[0]

    if not isinstance(x, core.TreeNeuron):
        raise TypeError('Expected Neuron/List, got "{}"'.format(type(x)))

    # Don't do anything if not actually fragmented
    if x.n_skeletons > 1:
        # Get connected components
        comp = list(nx.connected_components(x.graph.to_undirected()))
        # Sort so that the first component is the largest
        comp = sorted(comp, key=len, reverse=True)

        return core.NeuronList([graph.subset_neuron(x,
                                                    list(ss),
                                                    inplace=False)
                                for ss in comp])
    else:
        return core.NeuronList(x.copy())


def heal_fragmented_neuron(x, min_size=0, method='LEAFS', inplace=False):
    """ Heal fragmented neuron(s).

    Tries to heal a fragmented neuron (i.e. a neuron with multiple roots)
    using a minimum spanning tree.

    Parameters
    ----------
    x :         TreeNeuron/List
                Fragmented neuron(s).
    min_size :  int, optional
                Minimum size in nodes for fragments to be reattached.
    method :    'LEAFS' | 'ALL', optional
                Method used to heal fragments:
                        (1) 'LEAFS': Only leaf (including root) nodes will
                            be used to heal gaps.
                        (2) 'ALL': All treenodes can be used to reconnect
                            fragments.
    inplace :   bool, optional
                If False, will perform healing on and return a copy.

    Returns
    -------
    None
                If ``inplace=True``
    CatmaidNeuron/List
                If ``inplace=False``


    See Also
    --------
    :func:`navis.stitch_neurons`
                Function used by ``heal_fragmented_neuron`` to stitch
                fragments.
    :func:`navis.break_fragments`
                Use to break a fragmented neuron into disconnected pieces.
    """

    method = str(method).upper()

    if method not in ['LEAFS', 'ALL']:
        raise ValueError('Unknown method "{}"'.format(method))

    if isinstance(x, core.NeuronList):
        if not inplace:
            x = x.copy()
        healed = [heal_fragmented_neuron(n, min_size=min_size, method=method,
                                         inplace=True)
                                for n in config.tqdm(x,
                                                     desc='Healing',
                                                     disable=config.pbar_hide,
                                                     leave=config.pbar_leave)]
        if not inplace:
            return x
        return

    if not isinstance(x, core.TreeNeuron):
        raise TypeError('Expected CatmaidNeuron/List, got "{}"'.format(type(x)))

    # Don't do anything if not actually fragmented
    if x.n_skeletons > 1:
        frags = break_fragments(x)
        healed = stitch_neurons(*[f for f in frags if f.n_nodes > min_size],
                                method=method)
        if not inplace:
            return healed
        else:
            x.nodes = healed.nodes #update nodes
            x.tags = healed.tags #update tags
            x._clear_temp_attr()
    elif not inplace:
        return x
