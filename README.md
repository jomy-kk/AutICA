## AutICA

Signal Processing in Bioengineering Course Project @ IST Lisbon 

### Requirements
- MATLAB v2016 or superior
- MATLAB Statistical and Signal Processing toolboxes
- Python 3.6 or superior
- Up-to-date Python packages scipy, numpy, matplotlib

### To Run Automatic ICA Analysis
Alter subject, session numbers and ICA algorithm to run in `eeglab2021.0/analysis_protocol.m`. Run it on MATLAB. An EEGLAB session will start analysing the dataset of that subject-session pair and it will save some images and datasets on the device. So, be sure to have at least 300 Mb free of storage per subject-session pair. The analysis will stop to ask you which independent components to remove. Answer in the command line with an array, e.g. `[2 5 7]`. Results will be saved under the directory `results/SBJXX/SYY/algorithm` according to subject, session, and ICA algorithm selected.

### To Run Automatic P300 Detection
Alter subject, session numbers in `p300/p300_plot.py` and run the script with the command `python3 p300_plot.py`. Results will be saved under the directory `results/SBJXX/SYY` according to subject and session selected.

##### Authorship
(C) 2021 João Saraiva -- joaomiguelsaraiva@tecnico.ulisboa.pt
