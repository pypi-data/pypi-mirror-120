"""
Machine Learning Utilities
--------------------------
The ``maica.ml.util`` module provides essential functions for training configuration and model reuse.
Most deep learning algorithms in MAICA are based on this module.
"""

import numpy
import copy
import torch
import pandas
import os
import graphviz
import xgboost
import maica.ml.base
import maica.data.base
import torch.utils.data as tdata
import torch_geometric.data as tgdata
import maica.core.sys as sys
import maica.core.env as env
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
from maica.core.env import *
from sklearn.tree import export_graphviz
from maica.ml.base import SKLearnModel
from maica.data.base import Dataset
from maica.data.vector import VectorDataset
from maica.data.formula import FormDataset
from maica.data.graph import GraphDataset


class KFoldGenerator:
    def __init__(self,
                 dataset: Dataset,
                 k: int):
        self.sub_datasets = dataset.get_sub_datasets(k=k)

    def get(self,
            idx_fold: int):
        """
        Get training and test datasets for a given ``idx_fold``.

        :param idx_fold: (*int*) An index of the k-fold dataset.
        :return: Training and test datasets.
        """

        list_train_datasets = [self.sub_datasets[i] for i in range(0, len(self.sub_datasets)) if i != idx_fold]
        train_dataset = merge_datasets(list_train_datasets)
        test_dataset = self.sub_datasets[idx_fold]

        return train_dataset, test_dataset


class Metric:
    def __init__(self,
                 mae: float,
                 rmse: float,
                 mape: float,
                 r2: float):
        """
        A data class to store evaluation metrics.

        :param mae: (*float*) Mean absolute error.
        :param rmse: (*float*) Root mean square error.
        :param mape: (*float*) Mean absolute percentage error.
        :param r2: (*float*) The coefficient of determination (R2 score).
        """

        self.mae = mae
        self.rmse = rmse
        self.mape = mape
        self.r2 = r2

    def print(self):
        print('#####################################################')
        print('# Evaluation Metrics of the Prediction Results')
        print('#####################################################')
        print('# Mean Absolute Error (MAE): {:.4f}'.format(self.mae))
        print('# Root Mean Square Error (RMSE): {:.4f}'.format(self.rmse))
        print('# Mean Absolute Percentage Error (MAPE): {:.4f}'.format(self.mape))
        print('# R2 Score: {:.4f}'.format(self.r2))
        print('#####################################################')


def merge_datasets(list_datasets: list):
    """
    Generate a dataset object from a list of datasets in ``list_datasets``.

    :param list_datasets: (*list*) A list of datasets.
    :return: Dataset object.
    """

    data = numpy.vstack([dataset.data for dataset in list_datasets])
    idx_data = numpy.hstack([dataset.idx_data for dataset in list_datasets])

    if isinstance(list_datasets[0], VectorDataset):
        dataset = VectorDataset(data, list_datasets[0].idx_feat, list_datasets[0].idx_target,
                                list_datasets[0].var_names, idx_data)
    elif isinstance(list_datasets[0], FormDataset):
        dataset = FormDataset(data, list_datasets[0].idx_form, list_datasets[0].idx_feat, list_datasets[0].idx_target,
                              list_datasets[0].var_names, idx_data)
    elif isinstance(list_datasets[0], GraphDataset):
        dataset = GraphDataset(data, list_datasets[0].idx_struct, list_datasets[0].idx_feat,
                               list_datasets[0].idx_target, list_datasets[0].var_names, idx_data)
    else:
        raise AssertionError('Unknown dataset type: {}.'.format(type(list_datasets[0])))

    return dataset


def evaluate(targets: numpy.ndarray,
             preds: numpy.ndarray):
    """
    Calculate evaluation metrics for given target values ``targets`` and predicted values ``preds``.
    Four evaluation metrics are calculated:

    - Mean absolute error (MAE).
    - Root mean square error (RMSE).
    - Mean absolute percentage error (MAPE).
    - The coefficient of determination (R2 score).

    Definitions of the evaluation metrics are given in
    `Scikit-learn Regression Metrics <https://mendeleev.readthedocs.io/en/stable/>`_.

    :param targets: (*numpy.ndarray*) Target values of the prediction task.
    :param preds: (*numpy.ndarray*) Predicted values of the machine learning model.
    :return: (*maica.ml.util.Metric*) A data class to store the evaluation metrics.
    """

    mae = mean_absolute_error(targets, preds)
    rmse = numpy.sqrt(mean_squared_error(targets, preds))
    mape = mean_absolute_percentage_error(targets, preds)
    r2 = r2_score(targets, preds)

    return Metric(mae, rmse, mape, r2)


def k_fold_cross_val(dataset: maica.data.base.Dataset,
                     model: maica.ml.base.Model,
                     k: int):
    """
    Train and evaluate machine learning model based on k-fold cross validation.
    After the training and evaluation, means and standard deviations are printed in the standard I/O device.

    :param dataset: (*maica.data.base.Dataset*) A dataset to train machine learning model.
    :param model: (*maica.ml.base.Model*) Machine learning model.
    :param k: (*int*) The number of sub-datasets that will be used for k-fold cross validation.
    """

    k_fold = KFoldGenerator(dataset, k=k)
    metrics = list()

    print('#################################################')
    print('\u0007 Model Training with K-Fold Cross Validation')
    print('#################################################')
    for i in range(0, k):
        # Get train and test dataset form the k-fold generator.
        dataset_train, dataset_test = k_fold.get(idx_fold=i)

        # Copy initial model.
        __model = copy.deepcopy(model)

        # Train the model.
        if __model.alg_name in ALGS_SKLEARN:
            __model.fit(dataset_train.x, dataset_train.y)
            preds_test = __model.predict(dataset_test.x)

        # Evaluate the trained model.
        metric = evaluate(dataset_test.y, preds_test)
        metrics.append(metric)

        print('Fold [{}/{}]\tTest MAE: {:.4f}\tTest R2: {:.4f}'.format(i + 1, k, metric.mae, metric.r2))

    # Collect evaluation metrics.
    list_mae = [m.mae for m in metrics]
    list_rmse = [m.rmse for m in metrics]
    list_mape = [m.mape for m in metrics]
    list_r2 = [m.r2 for m in metrics]

    print('#################################################')
    print('\u0007 Results of K-Fold Cross Validation')
    print('#################################################')
    print('# Average MAE: {:.4f}\u00B1{:.4f}'.format(numpy.mean(list_mae), numpy.std(list_mae)))
    print('# Average RMSE: {:.4f}\u00B1{:.4f}'.format(numpy.mean(list_rmse), numpy.std(list_rmse)))
    print('# Average MAPE: {:.4f}\u00B1{:.4f}'.format(numpy.mean(list_mape), numpy.std(list_mape)))
    print('# Average R2 Score: {:.4f}\u00B1{:.4f}'.format(numpy.mean(list_r2), numpy.std(list_r2)))
    print('#################################################')


def get_model(alg_name: str,
              **kwargs):
    """
    Get a machine learning model for given algorithm name and model hyperparameters.
    The names of the algorithms are defined in ``maica_old.core.env``.

    :param alg_name: (*str*) A name of the machine learning algorithm (defined in ``maica_old.core.env``).
    :param kwargs: (*optional*) A dictionary containing model hyperparameters.
    :return: (*maica.ml.base.Model*) A machine learning model.
    """

    if alg_name in env.ALGS_SKLEARN:
        # Scikit-learn Algorithms
        return SKLearnModel(alg_name, **kwargs)
    elif alg_name in env.ALGS_PYTORCH:
        return None
        # Pytorch Algorithms
        # if alg_name == env.ALG_FCNN:
        #     model = FCNN(dim_in=kwargs['dim_in'], dim_out=kwargs['dim_out'])
        # elif alg_name == env.ALG_ATE:
        #     model = Autoencoder(dim_in=kwargs['dim_in'], dim_latent=kwargs['dim_latent'])
        # elif alg_name == env.ALG_GCN:
        #     readout = kwargs['readout'] if 'readout' in kwargs.keys() else 'mean'
        #     n_graphs = kwargs['n_graphs'] if 'n_graphs' in kwargs.keys() else 1
        #     model = GCN(n_node_feats=kwargs['n_node_feats'], dim_out=kwargs['dim_out'], n_graphs=n_graphs,
        #                 readout=readout)
        # elif alg_name == env.ALG_GAT:
        #     readout = kwargs['readout'] if 'readout' in kwargs.keys() else 'mean'
        #     n_graphs = kwargs['n_graphs'] if 'n_graphs' in kwargs.keys() else 1
        #     model = GAT(n_node_feats=kwargs['n_node_feats'], dim_out=kwargs['dim_out'], n_graphs=n_graphs,
        #                 readout=readout)
        # elif alg_name == env.ALG_GIN:
        #     readout = kwargs['readout'] if 'readout' in kwargs.keys() else 'mean'
        #     n_graphs = kwargs['n_graphs'] if 'n_graphs' in kwargs.keys() else 1
        #     model = GIN(n_node_feats=kwargs['n_node_feats'], dim_out=kwargs['dim_out'], n_graphs=n_graphs,
        #                 readout=readout)
        # elif alg_name == env.ALG_CGCNN:
        #     readout = kwargs['readout'] if 'readout' in kwargs.keys() else 'mean'
        #     n_graphs = kwargs['n_graphs'] if 'n_graphs' in kwargs.keys() else 1
        #     model = CGCNN(n_node_feats=kwargs['n_node_feats'], n_edge_feats=kwargs['n_edge_feats'],
        #                   dim_out=kwargs['dim_out'], n_graphs=n_graphs, readout=readout)
        # else:
        #     raise AssertionError('Invalid request received with unknown algorithm name: {}.'.format(alg_name))

        # Move model parameters from CPU to GPU when sys.run_gpu is enabled.
        if sys.run_gpu:
            model.gpu()

        return model
