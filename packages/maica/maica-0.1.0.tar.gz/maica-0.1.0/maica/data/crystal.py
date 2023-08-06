"""
Crystal Structure
-----------------
This module provides several utilities to handle the datasets containing the crystal structures.
You can load a dataset containing the crystal structures to the ``maica.data.graph.GraphDataset`` object
by calling ``load_dataset`` function in this module.
"""


import numpy
from tqdm import tqdm
from maica.core.env import *
from maica.core.sys import *
from maica.chem.base import load_elem_feats
from maica.data.base import read_data_file
from maica.data.util import impute
from maica.chem.crystal import even_samples
from maica.chem.crystal import get_crystal_graph
from maica.data.graph import GraphDataset


def load_dataset(path_dataset: str,
                 path_metadata_file: str,
                 idx_struct: object,
                 idx_target: int,
                 idx_feat: object = None,
                 impute_method: str = IMPUTE_KNN,
                 path_elem_embs: str = None):
    """
    Generate the ``GraphDataset`` object for a dataset of the crystal structures.
    It can be used for machine learning to predict materials properties from the crystal structures.

    :param path_dataset: (*str*) A path of the directory storing the CIF files.
    :param path_metadata_file: (*str*) A path of the metadata file of the dataset.
    :param idx_struct: (*numpy.ndarray*) Indices of the variables indicating the crystal structures in the dataset file.
    :param idx_target: (*object*) An index of the target variable in the data file.
    :param idx_feat: (*object*) Indices of the input numerical features in the data file (*default* = ``None``).
    :param impute_method: (*str, optional*) A imputation method to fill empty data in the data file (default = ``maica.core.env.IMPUTE_KNN``).
    :param path_elem_embs: (*str, optional*) A path of JSON file storing user-defined elemental embeddings (*default* = ``None``).
    :return: (*miaca.data.graph.GraphDataset*) A dataset object containing the crystal structures.
    """

    if idx_struct is None:
        raise AssertionError(ERR_EMPTY_STRUCT_IDX)

    __idx_struct = numpy.atleast_1d(idx_struct)
    __idx_feat = numpy.atleast_1d(idx_feat) if idx_feat is not None else idx_feat
    elem_feats = load_elem_feats(path_elem_embs)
    rbf_means = even_samples(min_val=0, max_val=3, n_samples=64)
    metadata_file, metadata = read_data_file(path_metadata_file)
    dataset = list()
    idx_data = list()

    # Read numerical features.
    if idx_feat is not None:
        metadata[:, __idx_feat] = impute(metadata[:, __idx_feat], impute_method)

    # Read crystal structures.
    for i in tqdm(range(0, metadata.shape[0])):
        numeric_feats = None if idx_feat is None else metadata[i, __idx_feat]
        targets = None if idx_target is None else metadata[i, idx_target]
        list_graphs = list()

        # If the data contains multiple crystal structures.
        for j in range(0, __idx_struct.shape[0]):
            path_cif = path_dataset + '/' + str(metadata[i, __idx_struct[j]]) + '.cif'
            mg = get_crystal_graph(elem_feats, path_cif, numeric_feats, rbf_means, targets, gid=i)

            if mg is not None:
                list_graphs.append(mg)

        if len(list_graphs) == __idx_struct.shape[0]:
            dataset.append(list_graphs)
            idx_data.append(i)

    # Generate a graph dataset containing the crystal structures.
    dataset = GraphDataset(dataset, __idx_struct, __idx_feat, idx_target,
                           metadata_file.columns.values, numpy.array(idx_data))

    return dataset
