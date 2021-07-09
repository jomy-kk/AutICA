####################################
#
#  PDSB Project 2021
#
#  Module: Classification with Convolutional Neural Networks (CNN)
#  File: load_dataset
#
#  Created on May 30, 2021
#
#  Code rights reserved to João Saraiva
#
####################################

from scipy.io import loadmat
import numpy as np
from scipy.signal import resample as rs
from scipy.stats import zscore
from glob import glob
import matplotlib.pyplot as plt

data_path = "/Users/jomy/OneDrive - Universidade de Lisboa/10º Semestre/PSB - Processamento de Sinal/Projeto/AutICA/data"


def prepare_dataset(subject, session,
                    ica_algorithm_pruned=None,
                    channels='all', epochs='all', epoch_segment='complete', resample=None, objects=False):

    print("Loading dataset...", end=' ')

    trainX, trainY, testX, testY = None, None, None, None

    def load_session_data(_session):

        # Load train data
        if ica_algorithm_pruned == None:
            _trainX = loadmat(data_path + "/" + subject + "/" + _session + "/Train/trainData.mat")['trainData']
        else:
            file_name = glob(
                data_path + "/" + subject + "/" + _session + "/Train/" + "*-" + ica_algorithm_pruned + "-pruned-*.mat")[
                0]
            _trainX = loadmat(file_name)['trainData']
        _trainY = np.loadtxt(data_path + "/" + subject + "/" + _session + "/Train/trainTargets.txt", dtype=int)

        # Load test data
        if ica_algorithm_pruned == None:
            _testX = loadmat(data_path + "/" + subject + "/" + _session + "/Test/testData.mat")['testData']
        else:
            file_name = glob(
                data_path + "/" + subject + "/" + _session + "/Test/" + "*-" + ica_algorithm_pruned + "-pruned-*.mat")[
                0]
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

    # prepared dataset = (trials, height, width, 1) ~= eg. (400, 8, 140, 1)
    trainX = np.reshape(trainX, (trainX.shape[2], trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[2], testX.shape[0], testX.shape[1], 1))

    print("DONE\n")

    print("\nTrain input shape:", trainX.shape)
    print("Train target shape:", trainY.shape)
    print("Test input shape:", testX.shape)
    print("Test target shape:", testY.shape)

    if objects:
        event_objects = get_event_objects(subject, session)
        taget_objects = get_target_objects(subject, session)
        return trainX, trainY, testX, testY, (trainX.shape[1], trainX.shape[2], 1), event_objects, taget_objects

    return trainX, trainY, testX, testY, (trainX.shape[1], trainX.shape[2], 1)
    # input shape of one sample = (height, width, 1) ~= eg. (8, 140, 1)
    # each sample corresponds to one epoch of the experiments


def get_event_objects(subject, session):

    def load_event_objects(_session):
        file = open(data_path + "/" + subject + "/" + _session + "/Test/testEvents.txt", 'r')
        values = file.read().split('\n')
        _temp = []
        for x in values:
            if x != '':
                _temp.append(int(x))
        return np.array(_temp)

    if isinstance(session, str):  # single-session (intra-session)
        return load_event_objects(session)

    elif isinstance(session, tuple):  # multi-session (inter-session)
        event_objects = load_event_objects(session[0])
        for s in range(1, len(session)):
            _event_objects = load_event_objects(session[s])
            event_objects = np.concatenate((event_objects, _event_objects))
        return event_objects


def get_target_objects(subject, session):

    def load_target_objects(_session):
        file = open(data_path + "/" + subject + "/" + _session + "/Test/testLabels.txt", 'r')
        values = file.read().split('\n')
        _temp = []
        for x in values:
            if x != '':
                _temp.append(int(x))
        return np.array(_temp)

    if isinstance(session, str):  # single-session (intra-session)
        return load_target_objects(session)

    elif isinstance(session, tuple):  # multi-session (inter-session)
        target_objects = load_target_objects(session[0])
        for s in range(1, len(session)):
            _target_objects = load_target_objects(session[s])
            target_objects = np.concatenate((target_objects, _target_objects))
        return target_objects

