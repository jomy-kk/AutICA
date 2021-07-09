####################################
#
#  PDSB Project 2021
#
#  Module: Plotting P300
#  File: P300 grand-average plotting by session
#
#  Created on June 1, 2021
#
#  Code rights reserved to João Saraiva
#
####################################

from scipy.stats import zscore

from load_dataset import load_dataset
import numpy as np
from matplotlib import pyplot as plt

plt.style.use('ggplot')
non_p300_color = '#cccccc'
p300_color_beforeICA = '#c9b97d'
p300_color_afterICA = '#6aa56e'
p300_timestamp_color = '#999999'

channels_num = {'C3': 0, 'Cz': 1, 'C4': 2, 'CPz': 3, 'P3': 4, 'Pz': 5, 'P4': 6, 'POz': 7}

def plot_average_p300(p300_data, not_p300_data, p300_data_beforeICA, channels=None, normalize=False, title=None, show=False):
    # Compute averages along epochs
    p300_data = np.mean(p300_data, axis=2)
    not_p300_data = np.mean(not_p300_data, axis=2)
    p300_data_beforeICA = np.mean(p300_data_beforeICA, axis=2)

    if channels is None:
        channels = channels_num.keys()
    else:
        # Filter channels
        p300_data = p300_data[[channels_num.get(c) for c in channels], :]
        not_p300_data = not_p300_data[[channels_num.get(c) for c in channels], :]
        p300_data_beforeICA = p300_data_beforeICA[[channels_num.get(c) for c in channels], :]


    # Find P300 timestamps only in [200, 550] ms interval
    p300_onsets_afterICA = p300_data[:, 50:138].argmax(axis=1) + 50
    new_latency = p300_onsets_afterICA / 250 * 1000
    p300_onsets_beforeICA = p300_data_beforeICA[:, 100:188].argmax(axis=1) + 100
    old_latency = p300_onsets_beforeICA / 250 * 1000 - 200
    new_amplitude = p300_data[:, 50:138].max(axis=1)
    old_amplitude = p300_data_beforeICA[:, 100:188].max(axis=1)

    # Normalize if requested
    if normalize:
        p300_data = zscore(p300_data, axis=1)
        not_p300_data = zscore(not_p300_data, axis=1)
        p300_data_beforeICA = zscore(p300_data_beforeICA, axis=1)

    # Vertical stack
    vspace = p300_data_beforeICA.max().max() + 5
    bases = vspace * np.arange(len(channels))
    p300_data = p300_data.T + bases
    not_p300_data = not_p300_data.T + bases
    p300_data_beforeICA = p300_data_beforeICA.T + bases

    # Plot signal against time
    t_afterICA = np.linspace(0, 1000, 250)  # milliseconds
    t_beforeICA = np.linspace(-200, 1200, 350)  # milliseconds
    plt.plot(t_afterICA, not_p300_data, non_p300_color,
             t_beforeICA, p300_data_beforeICA, p300_color_beforeICA,
             t_afterICA, p300_data, p300_color_afterICA)
    plt.xlim((0, 1000))
    #plt.ylim((-2.1, 2.1))
    plt.xlabel('Time (ms)', fontsize='small')
    plt.ylabel('Amplitude (uV)', fontsize='small')
    plt.xticks(range(0, 1001, 200))
    #plt.gca().yaxis.set_ticks(bases)
    #plt.gca().yaxis.set_ticklabels(channels)

    # Plot P300 timestamps
    # Note: Don't forget data matrices were transposed
    for i in range(0, len(channels)):
        # mark the old timestamp
        old_amplitude_normalized = p300_data_beforeICA[p300_onsets_beforeICA[i], i]
        plt.plot(old_latency[i], old_amplitude_normalized, 'o', color=p300_color_beforeICA)
        # mark the new timestamp
        new_amplitude_normalized = p300_data[p300_onsets_afterICA[i], i]
        label = str(int(new_latency[i])) + ' ms | ' + "%.2f" % new_amplitude[i] + ' uV'
        plt.annotate(text=label, xy=(new_latency[i], new_amplitude_normalized), xytext=(new_latency[i] + 6, new_amplitude_normalized + 0.1), fontsize='small')
        plt.plot(new_latency[i], new_amplitude_normalized, 'o', color=p300_color_afterICA)

    if title:
        plt.title(title, fontsize='medium')
    plt.tight_layout()
    if show:
        plt.show()





plt.figure(figsize=(16, 8))
channel = 'Cz'

for session in range(2, 8):

    p300_data, not_p300_data, p300_data_beforeICA = None, None, None

    #for subject in (6, 7, 8, 9, 11, 13, 14, 15):
    for subject in (1, 2, 3, 4, 5, 10, 12):
        if subject < 10:
            subject_code = 'SBJ0' + str(subject)
        else:
            subject_code = 'SBJ' + str(subject)

        if subject == 3 and session == 4:  # bad ICA exception
            continue

        if p300_data is None:
            # dataset testX shape: (channels, timeseries, trials)
            p300_data, not_p300_data = load_dataset(subject_code, "S0" + str(session), "picard")
            p300_data_beforeICA, _ = load_dataset(subject_code, "S0" + str(session))
        else:
            __p300_data, __not_p300_data = load_dataset(subject_code, "S0" + str(session), "picard")
            __p300_data_beforeICA, _ = load_dataset(subject_code, "S0" + str(session))

            p300_data = np.concatenate((p300_data, __p300_data), 2)
            not_p300_data = np.concatenate((not_p300_data, __not_p300_data), 2)
            p300_data_beforeICA = np.concatenate((p300_data_beforeICA, __p300_data_beforeICA), 2)

    plt.subplot(2, 3, session-1)
    plot_average_p300(p300_data, not_p300_data, p300_data_beforeICA, channels=(channel, ), title="Session " + str(session)
                      , normalize=False, show=False)



#plt.suptitle("        SUBJECT " + str(subject), y=1, fontsize=10, fontweight='bold')
#plt.subplots_adjust(top=0.975)
plt.savefig("../results/averageERP-" + channel + "-bySession_GroupB_notNormalized.pdf", bbox_inches='tight')


