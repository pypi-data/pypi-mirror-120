"""
Data Utilities
--------------
This module contains useful classes and functions for data pre-processing.
It can be used to convert user datasets into new dataset suitable for machine learning.
"""


import math
import numpy
import pandas
from sklearn.impute import KNNImputer
from rdkit import Chem
from pymatgen.core.structure import Structure
from maica.core.env import *
from maica.core.sys import *
from maica.chem.base import atom_nums
from maica.chem.base import atom_syms
from maica.chem.formula import parse_form


def impute(data: numpy.ndarray,
           method: str):
    """
    Fill empty values in the given ``data``.
    It is useful for machine learning with the experimental data containing missing values.
    Three imputation methods are provided:

    - Mean-based imputation method.
    - Zero-based imputation method.
    - KNN-based imputation method.

    Possible values of ``method`` selecting the imputation method are given in ``maica.core.env``.

    :param data: (*numpy.ndarray*) Data object.
    :param method: (*str*) A key of the imputation method.
    :return: (*numpy.ndarray*) Data object.
    """

    if method == IMPUTE_MEAN:
        # Fill empty values by mean values.
        means = numpy.nanmean(data, axis=0)
        for i in range(0, data.shape[0]):
            for j in range(0, data.shape[1]):
                if math.isnan(float(data[i, j])):
                    data[i, j] = means[j]
    elif method == IMPUTE_ZERO:
        # Fill empty values by zero.
        for i in range(0, data.shape[0]):
            for j in range(0, data.shape[1]):
                if math.isnan(float(data[i, j])):
                    data[i, j] = 0
    elif method == IMPUTE_KNN:
        # Fill empty values using the values of k-nearest neighbor data.
        imputer = KNNImputer(n_neighbors=3)
        data = imputer.fit_transform(data)
    else:
        raise AssertionError(ERR_UNKNOWN_IMPUTE.format(method))

    return data


def get_split_idx(n_data: int,
                  ratio: float):
    """
    Get indices that randomly split a set of {0, 1, ..., ``n_data``}.
    The set is divided into two subsets at a ratio of ``ratio`` to ``1 - ratio``.

    :param n_data: (*int*) The number of data in your data object.
    :param ratio: (*float*) The ratio for division.
    :return: (*numpy.ndarray, numpy.ndarray*) Data indices of the two subsets.
    """

    if ratio >= 1 or ratio <= 0:
        raise AssertionError(ERR_INVALID_SPLIT_RATIO.format(ratio))

    n_dataset1 = int(ratio * n_data)
    idx_rand = numpy.random.permutation(n_data)

    return idx_rand[:n_dataset1], idx_rand[n_dataset1:]


def get_one_hot_feat(categories: list,
                     hot_category: object):
    """
    Generate one-hot encoding for the argument ``hot_category`` in the categories of ``categories``.

    :param categories: (*list*) A list of categories for the one-hot encoding.
    :param hot_category: (*object*) An emerged class in the one-hot encoding.
    :return: (*numpy.ndarray*) The one-hot encoding feature.
    """

    one_hot_feat = dict()

    for cat in categories:
        one_hot_feat[cat] = 0

    if hot_category in categories:
        one_hot_feat[hot_category] = 1

    return numpy.array(list(one_hot_feat.values()))


def get_elem_dist(path_metadata_file: str,
                  idx_chem_code: int,
                  data_type: str,
                  path_cif_files: str = None):
    """
    Calculate elemental distribution in a dataset.
    For given metadata in ``path_metadata_file`` and data type in ``data_type``,
    it calculate the frequency for each element in the chemical compounds in the dataset.
    A dictionary object containing the frequency for each element is returned.

    :param path_metadata_file: (*str*) A path of the metadata file of the dataset.
    :param idx_chem_code: (*int*) An index of the chemical compound.
    :param data_type: (*str*) A data type of the chemical compound, which is available in {``DATA_TYPE_FORM``, ``DATA_TYPE_SMILES``, ``DATA_TYPE_CIF``}.
    :param path_cif_files: (*str, optional*) A path of the cif files for a data type of ``DATA_TYPE_CIF``.
    :return: (*dict*) The frequency for each element.
    """

    metadata = numpy.array(pandas.read_excel(path_metadata_file))
    elems = atom_nums.keys()
    elem_dist = dict()

    # Initialize a dictionary storing the elemental distribution.
    for e in elems:
        elem_dist[e] = 0

    if data_type == DATA_TYPE_FORM:
        # For chemical formulas.
        for i in range(0, metadata.shape[0]):
            form = parse_form(metadata[i, idx_chem_code])
            for e in form.keys():
                elem_dist[e] += 1
    elif data_type == DATA_TYPE_SMILES:
        # For molecular structures in SMILES.
        for i in range(0, metadata.shape[0]):
            mol = Chem.MolFromSmiles(metadata[i, idx_chem_code])
            atom_syms_mol = numpy.unique([atom_syms[atom.GetAtomicNum()] for atom in mol.GetAtoms()])
            for e in atom_syms_mol:
                elem_dist[e] += 1
    elif data_type == DATA_TYPE_CIF:
        # For crystal structures in CIF files.
        if path_cif_files is None:
            raise AssertionError('Path of the CIF files must be provided by path_cif_file'
                                 ' for a data type of DATA_TYPE_CIF.')

        for i in range(0, metadata.shape[0]):
            crystal = Structure.from_file(path_cif_files + '/' + metadata[i, idx_chem_code] + '.cif')
            atom_syms_crystal = numpy.unique([atom_syms[atom_num] for atom_num in crystal.atomic_numbers])
            for e in atom_syms_crystal:
                elem_dist[e] += 1
    else:
        raise AssertionError('Unknown data type {} was given'.format(data_type))

    return elem_dist
