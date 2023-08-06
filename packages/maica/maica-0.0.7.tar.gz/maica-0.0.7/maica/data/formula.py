"""
Chemical Formula
----------------
This module includes a basic class ``FormDataset`` to load a dataset containing the chemical formulas.
You can load a dataset containing the chemical formulas to the ``maica.data.formula.FormDataset`` object
by calling ``load_dataset`` function in this module.
"""


import numpy
import copy
import maica.core.env
from tqdm import tqdm
from sklearn.neighbors import LocalOutlierFactor
from maica.core.sys import *
from maica.data.base import read_data_file
from maica.data.util import get_split_idx
from maica.data.util import impute
from maica.chem.base import load_elem_feats
from maica.data.base import Dataset
from maica.chem.formula import form_to_vec
from maica.chem.formula import form_to_sparse_vec
from maica.chem.formula import parse_form


class FormDataset(Dataset):
    """
    It is a dataset class to load datasets based on the chemical formulas.
    To generate this class from your dataset, call ``load_dataset`` with a path of your dataset.
    """

    def __init__(self,
                 data: numpy.ndarray,
                 idx_form: numpy.ndarray,
                 idx_feat: numpy.ndarray,
                 idx_target: int,
                 var_names: numpy.ndarray,
                 forms: numpy.ndarray,
                 idx_data: numpy.ndarray = None):
        """
        :param data: (*numpy.ndarray*) A ``numpy.ndarray`` object containing the actual data.
        :param idx_form: (*numpy.ndarray*) Indices of the chemical formulas in the dataset file.
        :param idx_feat: (*numpy.ndarray*) Indices of the numerical features in the dataset file.
        :param idx_target: (*int*) An index of the target value in the dataset file.
        :param var_names: (*numpy.ndarray*) Names of all variables in the dataset file.
        :param forms: (*numpy.ndarray*) Chemical formulas of each data in the dataset.
        :param idx_data: (*numpy.ndarray*) Numerical indices of the data (*default* = ``None``).
        """

        super(FormDataset, self).__init__(data, idx_feat, idx_target, var_names)

        # Data object.
        self.x = self.data[:, :-1] if self.contain_target else self.data
        self.y = self.data[:, -1].reshape(-1, 1) if self.contain_target else None
        self.n_data = self.data.shape[0]
        self.n_feats = self.x.shape[1]

        # Information of data indexing.
        self.idx_data = numpy.arange(0, self.data.shape[0]) if idx_data is None else copy.deepcopy(idx_data)
        self.idx_form = copy.deepcopy(idx_form)

        # Chemical formulas of the data.
        self.forms = copy.deepcopy(forms.flatten())

        if type(self).__name__ == 'FormDataset':
            self._set_feat_names()
            # self._set_tooltips()

    def _set_feat_names(self):
        """
        Set names and types of the input features.
        """

        for idx in self.idx_form:
            self.feat_names.append(self.var_names[idx])
            self.feat_types.append('form')

        if self.idx_feat is not None:
            for idx in self.idx_feat:
                self.feat_names.append(self.var_names[idx])
                self.feat_types.append('num')

    def _set_tooltips(self):
        """
        Set tooltip for each data to identify it in the data visualization.
        """

        for i in range(0, self.data.shape[0]):
            self.tooltips.append('Data idx: ' + str(self.idx_data[i]) + ' (' + ' '.join(self.forms[i]) + ')')

    def normalize(self):
        """
        Normalize the input data based on the z-score.
        For vector-shaped data :math:`\mathbf{x}`, the z-score is defined by:

        .. math::
            \mathbf{z} = \\frac{\mathbf{x} - \mathbf{\mu}}{\mathbf{\sigma}},

        where :math:`\mathbf{\mu}` is the mean of the data, and :math:`\mathbf{\sigma}` is the standard deviation of the data.
        Note that all mathematical operations are applied dimensional-wise.
        """

        if self.contain_target:
            # For a dataset containing the target properties.
            self.feat_means = numpy.mean(self.data[:, :-1], axis=0)
            self.feat_stds = numpy.std(self.data[:, :-1], axis=0) + 1e-6
            self.data[:, :-1] = (self.data[:, :-1] - self.feat_means) / self.feat_stds
        else:
            # For a dataset without the target properties.
            self.feat_means = numpy.mean(self.data, axis=0)
            self.feat_stds = numpy.std(self.data, axis=0) + 1e-6
            self.data = (self.data - self.feat_means) / self.feat_stds

    def denormalize(self):
        """
        Restore the normalize input data.
        For vector-shaped normalized data :math:`\mathbf{z}`, the denormalized (oroginal) data is calculated by:

        .. math::
            \mathbf{x} = \mathbf{\sigma} \mathbf{z} + \mathbf{\mu},

        where :math:`\mathbf{\mu}` is the mean of the data, and :math:`\mathbf{\sigma}` is the standard deviation of the data.
        Note that all mathematical operations are applied dimensional-wise.
        """

        if self.feat_means is None:
            raise AssertionError(ERR_UNNORMALIZED)

        if self.contain_target:
            # For a dataset containing the target properties.
            self.data[:, :-1] = self.feat_stds * self.data[:, :-1] + self.feat_means
        else:
            # For a dataset without the target properties.
            self.data = self.feat_stds * self.data + self.feat_means

    def to_tensor(self):
        """
        Convert the data objects of numpy.ndarray into the data objects of torch.Tensor.
        """

        self.data = torch.tensor(self.data, dtype=torch.float)
        self.x = self.data[:, :-1] if self.contain_target else self.data
        self.y = self.data[:, -1].reshape(-1, 1) if self.contain_target else None

    def remove_outliers(self):
        """
        Remove outliers in the dataset using Local Outlier Factor (LOF).
        """

        # Remove outliers using local outlier factor (LOF).
        lof = LocalOutlierFactor(n_neighbors=int(numpy.sqrt(self.data.shape[0])))
        ind = lof.fit_predict(self.x())
        self.data = self.data[ind == 1, :]

        # Replace tooltips of the data.
        self.tooltips = [self.tooltips[i] for i in range(0, len(self.data)) if ind[i] == 1]

    def split(self,
              ratio: float):
        """
        Split a dataset into two sub-datasets based on the given ratio.
        Two sub-datasets and the original indices of the data in them are returned.

        :param ratio: (*float*) Ratio between two sub-datasets. The sub-datasets are dived by a ratio of ``ratio`` to ``1 - ratio``.
        :return: (*maica.data.formula.FormDataset, maica.data.formula.FormDataset*) Two sub-datasets and the original indices of the data in them.
        """

        # Randomly sample the dataset.
        idx_dataset1, idx_dataset2 = get_split_idx(self.data.shape[0], ratio)

        # Split dataset into the two subsets.
        dataset1 = FormDataset(self.data[idx_dataset1, :], self.idx_form, self.idx_feat, self.idx_target,
                               self.var_names, self.forms[idx_dataset1], self.idx_data[idx_dataset1])
        dataset2 = FormDataset(self.data[idx_dataset2, :], self.idx_form, self.idx_feat, self.idx_target,
                               self.var_names, self.forms[idx_dataset2], self.idx_data[idx_dataset2])

        return dataset1, dataset2

    def get_sub_datasets(self,
                         k: int):
        """
        Split the dataset into the :math:`k` sub-datasets without repeating the data.
        In the training, :math:`k-1` sub-datasets are used to train the model, and the remaining sub-dataset is used for evaluation.

        :param k: (*int*) The number of subsets.
        :return: (*list*) A list of :math:`k` sub-datasets.
        """

        idx_rand = numpy.random.permutation(self.n_data)
        n_data_subset = int(self.n_data / k)
        sub_datasets = list()

        # Get k-1 sub-datasets with the same size.
        for i in range(0, k-1):
            idx_sub_dataset = idx_rand[i*n_data_subset:(i+1)*n_data_subset]
            sub_dataset = FormDataset(self.data[idx_sub_dataset, :], self.idx_form, self.idx_feat, self.idx_target,
                                      self.var_names, self.forms[idx_sub_dataset], self.idx_data[idx_sub_dataset])
            sub_datasets.append(sub_dataset)

        # Get the last sub-dataset containing the all remaining data.
        idx_sub_dataset = idx_rand[(k-1)*n_data_subset:]
        sub_dataset = FormDataset(self.data[idx_sub_dataset, :], self.idx_form, self.idx_feat, self.idx_target,
                                  self.var_names, self.forms[idx_sub_dataset], self.idx_data[idx_sub_dataset])
        sub_datasets.append(sub_dataset)

        return sub_datasets


def load_dataset(path_data_file: str,
                 idx_form: object,
                 idx_feat: object,
                 idx_target: int,
                 impute_method: str = maica.core.env.IMPUTE_KNN,
                 path_elem_embs: str = None,
                 rep_type: str = 'compact'):
    """
    This is a wrapper function to load a dataset containing the chemical formulas.
    It loads a dataset object from a given dataset file in ``maica.data.vector.VectorDataset``.
    A representation method for the chemical formulas can be selected according to a given ``rep_type``.

    :param path_data_file: (*str*) The path of the data file.
    :param idx_form: (*object*) Indices of the chemical formulas in the data file.
    :param idx_feat: (*object*) Indices of the input numerical features in the data file.
    :param idx_target: (*int*) An index of the target variable in the data file.
    :param impute_method: (*str, optional*) A imputation method to fill empty data in the data file (*default* = ``maica.core.env.IMPUTE_KNN``).
    :param path_elem_embs: (*str, optional*) A path of JSON file storing user-defined elemental embeddings (*default* = ``None``).
    :param rep_type: (*str, optional*) A representation way to describe the chemical formulas (*default* = ``compact``).
    :return: (*maica.data.formula.FormDataset) A dataset object containing the chemical formulas.
    """

    if idx_form is None:
        raise AssertionError(ERR_EMPTY_FORM_IDX)

    __idx_form = numpy.atleast_1d(idx_form)
    __idx_feat = numpy.atleast_1d(idx_feat) if idx_feat is not None else idx_feat

    if rep_type == 'compact':
        return __load_dataset_compact(path_data_file, __idx_form, __idx_feat, idx_target, impute_method, path_elem_embs)
    elif rep_type == 'sparse':
        return __load_dataset_sparse(path_data_file, __idx_form, __idx_feat, idx_target, impute_method, path_elem_embs)


def __load_dataset_compact(path_data_file: str,
                           idx_form: numpy.ndarray,
                           idx_feat: numpy.ndarray,
                           idx_target: int,
                           impute_method: str,
                           path_elem_embs: str):
    """
    Load a dataset object from a dataset file in ``path_data_file`` containing the chemical formulas.
    All chemical formulas are represented as feature vectors with the same dimension based on the statistics of atomic features.
    A details description of the compact feature vector is given in the API reference of ``maica.chem.formula.form_to_vec``.

    :param path_data_file: (*str*) The path of the data file.
    :param idx_form: (*numpy.ndarray*) Indices of the chemical formulas in the data file.
    :param idx_feat: (*numpy.ndarray*) Indices of the input numerical features in the data file.
    :param idx_target: (*int*) An index of the target variable in the data file.
    :param impute_method: (*str, optional*) A imputation method to fill empty data in the data file (*default* = ``maica.core.env.IMPUTE_KNN``).
    :param path_elem_embs: (*str, optional*) A path of JSON file storing user-defined elemental embeddings (*default* = ``None``).
    :return: (*maica.data.formula.FormDataset) A dataset object containing the chemical formulas.
    """

    elem_feats = load_elem_feats(path_elem_embs)
    data_file, data = read_data_file(path_data_file)
    dataset = list()

    # Convert chemical formulas into numeric vectors based on the elemental embeddings.
    # Iterate idx_form and data.shape[0] to convert multiple formulas in a data row.
    form_vecs = list()
    for i in tqdm(range(0, data.shape[0])):
        form_feats = list()

        for idx in idx_form:
            form_feats.append(form_to_vec(str(parse_form(data[i, idx])), elem_feats))
        form_vecs.append(numpy.hstack(form_feats))
    dataset.append(numpy.vstack(form_vecs))

    # Check existence of numeric features.
    if idx_feat is not None:
        dataset.append(impute(data[:, idx_feat], impute_method))

    # Check existence of target property.
    if idx_target is not None:
        dataset.append(data[:, idx_target].reshape(-1, 1))

    # Create FormDataset object.
    dataset = numpy.hstack(dataset).astype(numpy.float)
    form_dataset = FormDataset(dataset, idx_form, idx_feat, idx_target, data_file.columns.values, data[:, idx_form])

    return form_dataset


def __load_dataset_sparse(path_data_file: str,
                          idx_form: numpy.ndarray,
                          idx_feat: numpy.ndarray,
                          idx_target: int,
                          impute_method: str,
                          path_elem_embs: str):
    """
    Load a dataset object from a dataset file in ``path_data_file`` containing the chemical formulas.
    The chemical formulas are represented as feature vectors with different dimensions based on the number elements in them.
    A details description of the compact feature vector is given in the API reference of ``maica.chem.formula.form_to_sparse_vec``.

    :param path_data_file: (*str*) The path of the data file.
    :param idx_form: (*numpy.ndarray*) Indices of the chemical formulas in the data file.
    :param idx_feat: (*numpy.ndarray*) Indices of the input numerical features in the data file.
    :param idx_target: (*int*) An index of the target variable in the data file.
    :param impute_method: (*str, optional*) A imputation method to fill empty data in the data file (*default* = ``maica.core.env.IMPUTE_KNN``).
    :param path_elem_embs: (*str, optional*) A path of JSON file storing user-defined elemental embeddings (*default* = ``None``).
    :return: (*maica.data.formula.FormDataset) A dataset object containing the chemical formulas.
    """

    elem_feats = load_elem_feats(path_elem_embs)
    data_file, data = read_data_file(path_data_file)
    formulas = list()
    dataset = list()

    # Find maximum number of elements in the chemical formulas.
    for i in range(0, data.shape[0]):
        formulas.append(list())

        for idx in idx_form:
            formulas[i].append(parse_form(data[i, idx]))
    max_elems = numpy.max([len(x.keys()) for d in formulas for x in d])

    form_vecs = list()
    for i in tqdm(range(0, data.shape[0])):
        form_feats = list()

        for formula in formulas[i]:
            form_feats.append(form_to_sparse_vec(str(formula), elem_feats, max_elems))
        form_vecs.append(numpy.hstack(form_feats))
    dataset.append(numpy.vstack(form_vecs))

    # Check existence of numeric features.
    if idx_feat is not None:
        dataset.append(impute(data[:, idx_feat], impute_method))

    # Check existence of target property.
    if idx_target is not None:
        dataset.append(data[:, idx_target].reshape(-1, 1))

    # Create FormDataset object.
    dataset = numpy.hstack(dataset).astype(numpy.float)
    form_dataset = FormDataset(dataset, idx_form, idx_feat, idx_target, data_file.columns.values, data[:, idx_form])

    return form_dataset
