####################################
#
#  PDSB Project 2021
#
#  Module: Plotting P300
#  File: load_dataset
#
#  Created on May 30, 2021
#
#  Code rights reserved to João Saraiva
#
####################################

from scipy.io import loadmat
import numpy as np
from glob import glob

data_path = "../data"

def load_dataset(subject, session, ica_algorithm_pruned=None, epoch_segment='complete'):

    print("Loading dataset...", end=' ')

    trainX, trainY, testX, testY = None, None, None, None

    def load_session_data(_session):

        # Load train data
        if ica_algorithm_pruned == None:
            _trainX = loadmat(data_path + "/" + subject + "/" + _session + "/Train/trainData.mat")['trainData']
        else:
            file_name = glob(data_path + "/" + subject + "/" + _session + "/Train/" + "*-" + ica_algorithm_pruned + "-pruned-*.mat")[0]
            _trainX = loadmat(file_name)['trainData']
        _trainY = np.loadtxt(data_path + "/" + subject + "/" + _session + "/Train/trainTargets.txt", dtype=int)

        # Load test data
        if ica_algorithm_pruned == None:
            _testX = loadmat(data_path + "/" + subject + "/" + _session + "/Test/testData.mat")['testData']
        else:
            file_name = glob(data_path + "/" + subject + "/" + _session + "/Test/" + "*-" + ica_algorithm_pruned + "-pruned-*.mat")[0]
            _testX = loadmat(file_name)['testData']
        _testY = np.loadtxt(data_path + "/" + subject + "/" + _session + "/Test/testTargets.txt", dtype=int)

        return _trainX, _trainY, _testX, _testY

    if isinstance(session, str):  # single-session (intra-session)
        trainX, trainY, testX, testY = load_session_data(session)

    elif isinstance(session, tuple):  # multi-session (inter-session)
        trainX, trainY, testX, testY = load_session_data(session[0])
        for s in range(1, len(session)):
            _trainX, _trainY, _testX, _testY = load_session_data(session[s])
            trainX = np.concatenate((trainX, _trainX), 2)
            testX = np.concatenate((testX, _testX), 2)
            trainY = np.concatenate((trainY, _trainY), 0)
            testY = np.concatenate((testY, _testY), 0)

    # Join train and test sets
    X = np.concatenate((trainX, testX), 2)
    Y = np.concatenate((trainY, testY), 0)

    p300_indices = np.where(Y == 1)[0]
    not_p300_indices = np.where(Y == 0)[0]

    print("DONE\n")

    return X[:, :, p300_indices], X[:, :, not_p300_indices]
    # dataset shape: (channels, timeseries, trials)
