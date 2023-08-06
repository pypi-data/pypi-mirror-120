"""
Molecular Structure
-------------------
This module provides several utilities to handle the datasets containing the molecular structures.
You can load a dataset containing the molecular structures to the ``maica.data.graph.GraphDataset`` object
by calling ``load_dataset`` function in this module.
"""


import numpy
from tqdm import tqdm
from maica.core.env import *
from maica.core.sys import *
from maica.chem.base import load_elem_feats
from maica.data.base import read_data_file
from maica.data.util import impute
from maica.chem.molecule import get_mol_graph
from maica.data.graph import GraphDataset


def load_dataset(path_metadata_file: str,
                 idx_struct: object,
                 idx_target: int,
                 idx_feat: object = None,
                 impute_method: str = IMPUTE_KNN,
                 path_elem_embs: str = None):
    """
    Generate the ``GraphDataset`` object for a dataset of the molecular structures.
    It can be used for machine learning to predict molecular properties from the molecular structures.

    :param path_metadata_file: (*str*) The path of the metadata file of the dataset.
    :param idx_struct: (*object*) Indices of the variables indicating the molecular structures in the dataset file.
    :param idx_target: (*int*) An index of the target variable in the data file.
    :param idx_feat: (*object*) Indices of the input numerical features in the data file (*default* = ``None``).
    :param impute_method: (*str, optional*) A imputation method to fill empty data in the data file (default = ``maica.core.env.IMPUTE_KNN``).
    :param path_elem_embs: (*str, optional*) A path of JSON file storing user-defined elemental embeddings (*default* = ``None``).
    :return: (*miaca.data.graph.GraphDataset*) A dataset object containing the molecular structures.
    """

    if idx_struct is None:
        raise AssertionError(ERR_EMPTY_STRUCT_IDX)

    __idx_struct = numpy.atleast_1d(idx_struct)
    __idx_feat = numpy.atleast_1d(idx_feat) if idx_feat is not None else idx_feat
    elem_feats = load_elem_feats(path_elem_embs)
    metadata_file, metadata = read_data_file(path_metadata_file)
    dataset = list()
    idx_data = list()

    # Read numerical features.
    if idx_feat is not None:
        metadata[:, __idx_feat] = impute(metadata[:, __idx_feat], impute_method)

    # Read molecular structures.
    for i in tqdm(range(0, metadata.shape[0])):
        numeric_feats = None if idx_feat is None else metadata[i, __idx_feat]
        targets = None if idx_target is None else metadata[i, idx_target]
        list_graphs = list()

        # If the data contains multiple molecular structures.
        for j in range(0, __idx_struct.shape[0]):
            smiles = str(metadata[i, __idx_struct[j]])
            mg = get_mol_graph(elem_feats, smiles, numeric_feats, targets, gid=i)

            if mg is not None:
                list_graphs.append(mg)

        if len(list_graphs) == __idx_struct.shape[0]:
            dataset.append(list_graphs)
            idx_data.append(i)

    # Generate a graph dataset containing molecular structures.
    dataset = GraphDataset(dataset, __idx_struct, __idx_feat, idx_target,
                           metadata_file.columns.values, numpy.array(idx_data))

    return dataset
