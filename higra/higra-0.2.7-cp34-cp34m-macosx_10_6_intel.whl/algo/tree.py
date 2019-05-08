############################################################################
# Copyright ESIEE Paris (2018)                                             #
#                                                                          #
# Contributor(s) : Benjamin Perret                                         #
#                                                                          #
# Distributed under the terms of the CECILL-B License.                     #
#                                                                          #
# The full license is in the file LICENSE, distributed with this software. #
############################################################################

import higra as hg


@hg.argument_helper(hg.CptValuedHierarchy)
def reconstruct_leaf_data(altitudes, deleted_nodes, tree):
    """
    Each leaf of the tree takes the altitude of its closest non deleted ancestor.

    :param altitudes: node altitudes of the input tree (Concept :class:`~higra.CptValuedHierarchy`
    :param deleted_nodes: binary node weights indicating which nodes are deleted
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :return: Leaf weights (Concept :class:`~higra.CptVertexWeightedGraph` if tree satisfies :class:`~higra.CptHierarchy`)
    """
    reconstruction = hg.propagate_sequential(altitudes,
                                             deleted_nodes,
                                             tree)
    leaf_weights = reconstruction[0:tree.num_leaves(), ...]

    if hg.CptHierarchy.validate(tree):
        leaf_graph = hg.CptHierarchy.construct(tree)["leaf_graph"]
        leaf_weights = hg.delinearize_vertex_weights(leaf_weights, leaf_graph)
        hg.CptVertexWeightedGraph.link(leaf_weights, leaf_graph)

    return leaf_weights


@hg.argument_helper(hg.CptValuedHierarchy)
def labelisation_horizontal_cut_from_threshold(altitudes, threshold, tree):
    """
    Labelize tree leaves according to an horizontal cut in the tree.

    Two leaves are in the same region (ie. have the same label) if
    the altitude of their lowest common ancestor is strictly greater
    than the specified threshold.

    :param altitudes: node altitudes of the input tree (Concept :class:`~higra.CptValuedHierarchy`
    :param threshold: a threshold level
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :return: Leaf labels (Concept :class:`~higra.CptVertexWeightedGraph` if tree satisfies :class:`~higra.CptHierarchy`)
    """

    leaf_labels = hg.cpp._labelisation_horizontal_cut_from_threshold(tree, float(threshold), altitudes)

    if hg.CptHierarchy.validate(tree):
        leaf_graph = hg.CptHierarchy.construct(tree)["leaf_graph"]
        leaf_labels = hg.delinearize_vertex_weights(leaf_labels, leaf_graph)
        hg.CptVertexLabeledGraph.link(leaf_labels, leaf_graph)

    return leaf_labels


@hg.argument_helper(hg.CptValuedHierarchy)
def labelisation_hierarchy_supervertices(altitudes, tree, leaf_graph=None, handle_rag=True):
    """
    Labelize the tree leaves into supervertices.

    Two leaves are in the same supervertex if they have a common ancestor of altitude 0.

    This functions guaranties that the labels are in the range [0, num_supervertices-1].

    :param altitudes: node altitudes of the input tree (Concept :class:`~higra.CptValuedHierarchy`
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :param leaf_graph: optional, graph on the leaves of the input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :param handle_rag: if True and the provided tree has been built on a region adjacency graph, then the labelisation corresponding to the rag regions is returned.
    :return: Leaf labels (Concept :class:`~higra.CptVertexWeightedGraph` if tree satisfies :class:`~higra.CptHierarchy`)

    """

    if hg.CptRegionAdjacencyGraph.validate(leaf_graph) and handle_rag:
        return hg.CptRegionAdjacencyGraph.construct(leaf_graph)["vertex_map"]

    leaf_labels = hg.cpp._labelisation_hierarchy_supervertices(tree, altitudes)

    if leaf_graph is not None:
        leaf_labels = hg.delinearize_vertex_weights(leaf_labels, leaf_graph)
        hg.CptVertexLabeledGraph.link(leaf_labels, leaf_graph)

    return leaf_labels


@hg.argument_helper(hg.CptValuedHierarchy, ("tree", hg.CptBinaryHierarchy))
def filter_binary_partition_tree(altitudes, deleted_frontier_nodes, tree, mst):
    """
    Filter the given binary partition tree according to the given list of frontiers to remove.

    In a binary a tree, each inner node (non leaf node) is associated to the frontier separating its two children.
    If this node frontier is marked for deletion then the corresponding frontier is removed
    effectively merging its two children.

    :param altitudes: node altitudes of the input tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param deleted_frontier_nodes: a boolean array indicating for each node of the tree is its children must be merged (True) or not (False)
    :param tree: input binary partition tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :param mst: minimum spanning tree associated to the given binary partition tree (deduced from :class:`~higra.CptBinaryPartitionHierarchy` on the parameter `tree`)
    :return: a binary partition tree (Concept :class:`~higra.CptBinaryHierarchy`) and its node altitudes (Concept :class:`~higra.CptValuedHierarchy`)
    """

    mst_edge_weights = altitudes[tree.num_leaves():]
    mst_edge_weights[deleted_frontier_nodes[tree.num_leaves():]] = 0
    return hg.bpt_canonical(mst_edge_weights, mst)


@hg.argument_helper(hg.CptHierarchy)
def binary_labelisation_from_markers(tree, object_marker, background_marker, leaf_graph=None):
    """
    Given two binary markers o (object) and b (background) (given by their indicator functions)
    on the leaves of a tree t, the corresponding binary labelization of the leaves of t is defined as
    the union of all the nodes intersecting o but not b.

    final_object = union {R in T | R cap o neq emptyset and R cap b = emptyset}

    :param tree: input tree (Concept :class:`~higra.CptHierarchy`)
    :param object_marker: indicator function of the object marker: 1d array of size tree.num_leaves() where non zero values correspond to the object marker
    :param background_marker: indicator function of the background marker: 1d array of size tree.num_leaves() where non zero values correspond to the background marker
    :param leaf_graph: optional, graph on the leaves of the input tree (deduced from :class:`~higra.CptHierarchy`)
    :return: Leaf labels (Concept :class:`~higra.CptVertexWeightedGraph` if `leaf_graph` is not `None`)
    """

    if leaf_graph is not None:
        object_marker = hg.linearize_vertex_weights(object_marker, leaf_graph)
        background_marker = hg.linearize_vertex_weights(background_marker, leaf_graph)

    object_marker, background_marker = hg.cast_to_common_type(object_marker, background_marker)
    labels = hg.cpp._binary_labelisation_from_markers(tree, object_marker, background_marker)

    if leaf_graph is not None:
        labels = hg.delinearize_vertex_weights(labels, leaf_graph)
        hg.CptVertexLabeledGraph.link(labels, leaf_graph)

    return labels


@hg.argument_helper(hg.CptValuedHierarchy)
def sort_hierarchy_with_altitudes(altitudes, tree):
    """
    Sort the nodes of a tree according to their altitudes.
    The altitudes must be increasing, i.e. for any nodes :math:`i, j` such that :math:`j` is an ancestor of :math:`i`, then :math:`altitudes[i] <= altitudes[j]`.

    The result is a new tree and a node map, isomorph to the input tree such that for any nodes :math:`i` and :math:`j`, :math:`i<j \Rightarrow altitudes[node\_map[i]] \leq altitudes[node\_map[j]]`

    The latter condition is stronger than the original condition on the altitudes as :math:`j` is an ancestor of :math:`i` implies :math:`i<j` while the converse is not true.

    The returned "node_map" is an array that maps any node index :math:`i` of the new tree,
    to the index of this node in the original tree.

    :param altitudes: node altitudes of the input tree (Concept :class:`~higra.CptValuedHierarchy`)
    :param tree: input tree (deduced from :class:`~higra.CptValuedHierarchy`)
    :return: the sorted tree (Concept :class:`~higra.CptHierarchy`), its node altitudes (Concept :class:`~higra.CptValuedHierarchy`), and the node map
    """
    new_tree, node_map = hg.cpp._sort_hierarchy_with_altitudes(tree, altitudes)
    new_altitudes = altitudes[node_map]
    hg.CptValuedHierarchy.link(new_altitudes, new_tree)

    return new_tree, new_altitudes, node_map
