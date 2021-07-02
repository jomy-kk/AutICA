####################################
#
#  PDSB Project 2021
#
#  Module: -
#  File: p300_trials
#
#  Created on May 20, 2021
#  Last modified on May 20, 2021
#
#  Code rights reserved to João Saraiva
#
####################################

import numpy as np

data_path = "data"

def get_p300_epochs(subject, session, test_train):

    def load_targets(_session):
        file = open(data_path + "/" + subject + "/" + _session + "/" + test_train + "/" + test_train.lower() + "Targets.txt", 'r')
        values = file.read().split('\n')
        targets = []
        for x in values:
            if x != '':
                targets.append(int(x))
        return np.array(targets)

    targets = load_targets(session)
    indices_p300 = np.argwhere(targets) + 1  # these are to be used in MATLAB, where indices start at 1
    np.savetxt(data_path + "/" + subject + "/" + session + "/" + test_train + "/p300_indices.txt", indices_p300,
               fmt='%i', delimiter=' ', newline=' ')

def get_not_p300_epochs(subject, session, test_train):

    def load_targets(_session):
        file = open(data_path + "/" + subject + "/" + _session + "/" + test_train + "/" + test_train.lower() + "Targets.txt", 'r')
        values = file.read().split('\n')
        targets = []
        for x in values:
            if x != '':
                targets.append(int(x))
        return np.array(targets)

    targets = load_targets(session)
    indices_not_p300 = np.array(np.where(targets == 0)) + 1  # these are to be used in MATLAB, where indices start at 1
    np.savetxt(data_path + "/" + subject + "/" + session + "/" + test_train + "/not_p300_indices.txt", indices_not_p300,
               fmt='%i', delimiter=' ', newline=' ')


for subject in range(1, 16):
    for session in range(1, 8):
        if subject < 10:
            get_p300_epochs('SBJ0'+str(subject), 'S0'+str(session), 'Train')
            get_not_p300_epochs('SBJ0'+str(subject), 'S0'+str(session), 'Train')
        else:
            get_p300_epochs('SBJ' + str(subject), 'S0' + str(session), 'Train')
            get_not_p300_epochs('SBJ' + str(subject), 'S0' + str(session), 'Train')

    print('Done for subject', subject)