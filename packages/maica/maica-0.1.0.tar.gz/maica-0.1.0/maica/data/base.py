"""
Base Module
-----------
This module contains an abstract class of the dataset objects.
All dataset objects in MAICA inherits the abstract class of this module.
"""


import numpy
import pandas
import warnings
import copy
from abc import ABC
from abc import abstractmethod
from maica.core.sys import *


# Ignore unnecessary warnings from third party packages.
warnings.filterwarnings(action='ignore', category=UserWarning)


class Dataset(ABC):
    """
    An abstract class of Dataset classes in MAICA.
    The dataset objects in MAICA must inherit this class.
    """

    @abstractmethod
    def __init__(self,
                 data: object,
                 idx_feat: object,
                 idx_target: int,
                 var_names: numpy.ndarray):
        """
        :param data: (*object*) A data object.
        :param idx_feat: (*object*) (*numpy.ndarray*) Indices of the numerical features in the dataset file.
        :param idx_target: (*int*) An index of the target value in the dataset file.
        :param var_names: (*numpy.ndarray*) (*numpy.ndarray*) Names of all variables in the dataset file.
        """

        # Metadata of the input features and the target.
        self.idx_feat = copy.deepcopy(idx_feat)
        self.idx_target = copy.deepcopy(idx_target)
        self.contain_target = False if self.idx_target is None else True
        self.var_names = copy.deepcopy(var_names)
        self.feat_names = list()
        self.feat_types = list()
        self.target_name = None if self.idx_target is None else self.var_names[idx_target]

        # Data object.
        self.data = data

        # Tooltips for data visualization.
        self.tooltips = list()

        # Data statistics for normalization.
        self.feat_means = None
        self.feat_stds = None

    @abstractmethod
    def _set_feat_names(self):
        pass

    @abstractmethod
    def _set_tooltips(self):
        pass


def read_data_file(path_data_file: str):
    """
    Read data file form a given path of ``path_data_file``.
    Only the :obj:`.xlsx` and :obj:`.csv` extensions are available as the data file.

    :param path_data_file: (*str*) A path of the data file.
    :return: (*pandas.DataFrame, numpy.ndarray*) Data frame containing metadata and pure data object.
    """

    # Get the file extension of the data file.
    ext = path_data_file.split('.')[-1]

    # Read dataset file according to the file extension.
    if ext == 'xlsx':
        data_file = pandas.read_excel(path_data_file)
        data_obj = numpy.array(data_file)
    elif ext == 'csv':
        data_file = pandas.read_csv(path_data_file)
        data_obj = numpy.array(data_file)
    else:
        raise AssertionError(ERR_DATA_FILE_EXT.format(ext))

    return data_file, data_obj
